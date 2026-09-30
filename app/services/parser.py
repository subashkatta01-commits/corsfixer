import re
from typing import Dict, List

class ConfigParserService:
    """Parses raw gateway/server configurations (Nginx, Express, FastAPI) for CORS headers."""

    @staticmethod
    def parse_config(config_text: str) -> Dict[str, List[str]]:
        parsed_rules = {
            "allowed_origins": [],
            "allowed_methods": [],
            "allowed_headers": [],
            "allow_credentials": "false"
        }

        if not config_text:
            return parsed_rules

        # Extract Nginx / Apache Access-Control-Allow-Origin
        origins = re.findall(r'Access-Control-Allow-Origin[\s\'"]+([^\'";]+)', config_text, re.IGNORECASE)
        if origins:
            parsed_rules["allowed_origins"] = [o.strip() for o in origins]

        # Extract Express / FastAPI origin arrays or strings
        express_origins = re.findall(r'origin:\ [\'"]([^\'"]+)[\'"]', config_text)
        if express_origins:
            parsed_rules["allowed_origins"].extend([o.strip() for o in express_origins])

        # Extract Access-Control-Allow-Credentials
        credentials = re.findall(r'Access-Control-Allow-Credentials[\s\'"]+([^\'";]+)', config_text, re.IGNORECASE)
        if credentials or "credentials: true" in config_text.lower():
            parsed_rules["allow_credentials"] = "true"

        return parsed_rules