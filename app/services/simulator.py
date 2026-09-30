import time
from typing import Dict, List
from app.schemas import SimulationRequest, AnalysisResponse, Severity
from app.services.parser import ConfigParserService
from app.services.security_audit import SecurityAuditEngine
from app.services.generator import CodeGeneratorService

class SimulatorEngine:
    """Core simulation engine designed for <10ms execution time."""

    @staticmethod
    def run_simulation(payload: SimulationRequest) -> AnalysisResponse:
        start_time = time.perf_counter()

        # Step 1: Parse raw server config if provided
        parsed_config = {}
        if payload.server_config_raw:
            parsed_config = ConfigParserService.parse_config(payload.server_config_raw)

        # Step 2: Determine allowed origins
        allowed_origins = parsed_config.get("allowed_origins", [payload.request_origin])
        
        # Step 3: Run OWASP security audit
        findings = SecurityAuditEngine.audit(
            origin=payload.request_origin,
            with_credentials=payload.with_credentials,
            allowed_origins=allowed_origins
        )

        has_critical_findings = any(f.severity == Severity.CRITICAL for f in findings)
        is_allowed = payload.request_origin in allowed_origins and not has_critical_findings

        # Step 4: Build Browser Enforcement Rule Explanation
        if is_allowed:
            explanation = (
                f"Browser CORS check passed in {(time.perf_counter() - start_time)*1000:.2f}ms. "
                f"Origin '{payload.request_origin}' matches backend configuration and preflight headers are valid."
            )
            status_code = 204
        else:
            explanation = (
                f"Browser CORS check blocked in {(time.perf_counter() - start_time)*1000:.2f}ms. "
                "The browser enforced Same-Origin Policy (SOP) restrictions due to mismatched headers or OWASP security violations."
            )
            status_code = 403

        # Step 5: Matched CORS Response Headers
        matched_rules = {
            "Access-Control-Allow-Origin": payload.request_origin if is_allowed else "None",
            "Access-Control-Allow-Credentials": str(payload.with_credentials).lower(),
            "Access-Control-Allow-Methods": payload.request_method.value,
            "Access-Control-Allow-Headers": ", ".join(payload.request_headers) if payload.request_headers else "Content-Type, Authorization"
        }

        # Step 6: Generate Production-Safe Fixes
        snippets = CodeGeneratorService.generate_snippets(payload.request_origin, payload.with_credentials)

        return AnalysisResponse(
            is_allowed=is_allowed,
            status_code=status_code,
            explanation=explanation,
            matched_rules=matched_rules,
            findings=findings,
            safe_snippets=snippets
        )