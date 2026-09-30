from typing import Dict, List

class CodeGeneratorService:
    """Generates production-safe gateway configuration snippets."""

    @staticmethod
    def generate_snippets(allowed_origin: str, credentials: bool) -> Dict[str, str]:
        cred_str = "true" if credentials else "false"
        safe_origin = allowed_origin if allowed_origin else "https://yourdomain.com"

        nginx = f"""# Production-Safe Nginx CORS Configuration
location /api/ {{
    if ($http_origin ~* "^({safe_origin})$") {{
        add_header 'Access-Control-Allow-Origin' '$http_origin' always;
        add_header 'Access-Control-Allow-Credentials' '{cred_str}' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization' always;
    }}
    if ($request_method = 'OPTIONS') {{
        add_header 'Access-Control-Max-Age' 1728000;
        add_header 'Content-Type' 'text/plain charset=UTF-8';
        add_header 'Content-Length' 0;
        return 204;
    }}
}}"""

        express = f"""// Production-Safe Express CORS Configuration
const cors = require('cors');

const corsOptions = {{
  origin: '{safe_origin}',
  credentials: {cred_str},
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}};

app.use(cors(corsOptions));"""

        fastapi = f"""# Production-Safe FastAPI CORS Middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["{safe_origin}"],
    allow_credentials={credentials},
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)"""

        return {
            "nginx": nginx,
            "express": express,
            "fastapi": fastapi
        }