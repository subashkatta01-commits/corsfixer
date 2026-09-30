# corsfixer

A FastAPI-based CORS diagnostic and simulation service that helps validate browser CORS policies, detect unsafe configurations, and generate safe server-side snippets for Nginx, Express, and FastAPI.

## Features

- CORS request simulation
- Security audit for common OWASP misconfigurations
- Origin policy validation
- Safe config snippet generation
- Browser-based dashboard for testing requests

## Project Structure

```text
app/
  __init__.py
  main.py
  schemas.py
  services/
    generator.py
    parser.py
    security_audit.py
    simulator.py

tests/
  test_main.py
```

## Run locally

```bash
cd c:\y24cd055\corsfixer
set PYTHONPATH=.
py -m uvicorn app.main:app --host localhost --port 8000 --reload
```

Then open:

- http://localhost:8000/
- http://localhost:8000/docs

## API Example

```bash
curl -X POST http://localhost:8000/api/v1/simulate-preflight \
  -H "Content-Type: application/json" \
  -d '{
    "request_origin": "https://app.example.com",
    "target_url": "https://api.example.com/v1/data",
    "request_method": "POST",
    "request_headers": ["Content-Type", "Authorization"],
    "with_credentials": true
  }'
```

## Testing

```bash
cd c:\y24cd055\corsfixer
py -m pytest -q tests/test_main.py
```

## Notes

This project is intended as a diagnostic and educational tool for understanding CORS behavior and secure configuration patterns.
