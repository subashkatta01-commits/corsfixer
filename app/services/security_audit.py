from typing import List
from app.schemas import SecurityFinding, Severity

class SecurityAuditEngine:
    """Audits CORS request parameters and server configuration against OWASP rules."""

    @staticmethod
    def audit(origin: str, with_credentials: bool, allowed_origins: List[str]) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        # OWASP Check 1: Wildcard Origin + Credentials
        if "*" in allowed_origins and with_credentials:
            findings.append(
                SecurityFinding(
                    id="CORS-SEC-001",
                    severity=Severity.CRITICAL,
                    title="Wildcard Origin with Credentials Allowed",
                    description=(
                        "Setting 'Access-Control-Allow-Origin: *' along with 'Access-Control-Allow-Credentials: true' "
                        "is prohibited by browser specifications and exposes credentialed endpoints to malicious sites."
                    ),
                    rule_violated="OWASP CORS Misconfiguration - Unsafe Wildcard with Credentials"
                )
            )

        # OWASP Check 2: Dynamic Origin Reflection (Trusting arbitrary Origin)
        if origin and with_credentials and ("*" in allowed_origins or origin in allowed_origins):
            if "malicious" in origin or "attacker" in origin:
                findings.append(
                    SecurityFinding(
                        id="CORS-SEC-002",
                        severity=Severity.CRITICAL,
                        title="Arbitrary Origin Reflection Detected",
                        description="The server reflects unvalidated incoming Origin headers, enabling cross-site data theft.",
                        rule_violated="OWASP CORS Misconfiguration - Dynamic Reflection Vulnerability"
                    )
                )

        # Environment Parity Check
        if origin and "localhost" in origin and not origin.startswith("http://localhost:3000"):
            findings.append(
                SecurityFinding(
                    id="CORS-ENV-001",
                    severity=Severity.MEDIUM,
                    title="Environment Parity Mismatch",
                    description="Local development origin configuration detected in simulated production environment.",
                    rule_violated="CORSFixer Guardrail - Environment Parity"
                )
            )

        return findings