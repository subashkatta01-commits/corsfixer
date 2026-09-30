from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.schemas import SimulationRequest, AnalysisResponse
from app.services.simulator import SimulatorEngine

app = FastAPI(
    title="CORSFixer Diagnostic API Engine",
    description="Low-latency CORS diagnostic proxy, preflight simulator, and security audit tool",
    version="1.0.0"
)

# Enable CORS for frontend dashboard interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>CORSFixer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                background: #1f1f24;
                color: #f5f5f5;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .panel {
                width: min(760px, 90vw);
                background: #2b2b31;
                border-radius: 16px;
                padding: 28px;
                box-shadow: 0 18px 45px rgba(0,0,0,.3);
            }
            h1 { margin-top: 0; }
            label { display: block; margin-top: 12px; }
            input, select, button {
                width: 100%;
                padding: 10px 12px;
                margin-top: 6px;
                border-radius: 8px;
                border: 1px solid #4a4a52;
                background: #1d1d22;
                color: #f5f5f5;
                box-sizing: border-box;
            }
            button {
                margin-top: 18px;
                background: #5a8cff;
                border: none;
                cursor: pointer;
                font-weight: bold;
            }
            pre {
                margin-top: 18px;
                background: #121216;
                padding: 14px;
                border-radius: 10px;
                overflow-x: auto;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <div class="panel">
            <h1>CORSFixer</h1>
            <p>Test a request origin against a CORS policy and generate safe fixes.</p>

            <form id="cors-form">
                <label>
                    Request Origin
                    <input id="request_origin" value="https://app.example.com" required />
                </label>
                <label>
                    Target URL
                    <input id="target_url" value="https://api.example.com/v1/data" required />
                </label>
                <label>
                    Method
                    <select id="request_method">
                        <option>GET</option>
                        <option selected>POST</option>
                        <option>PUT</option>
                        <option>DELETE</option>
                        <option>OPTIONS</option>
                    </select>
                </label>
                <label>
                    Headers
                    <input id="request_headers" value="Content-Type, Authorization" />
                </label>
                <label>
                    With Credentials
                    <select id="with_credentials">
                        <option value="false">False</option>
                        <option value="true">True</option>
                    </select>
                </label>
                <button type="submit">Run simulation</button>
            </form>

            <pre id="result">Waiting for analysis...</pre>
        </div>

        <script>
            document.getElementById('cors-form').addEventListener('submit', async function (event) {
                event.preventDefault();
                const payload = {
                    request_origin: document.getElementById('request_origin').value,
                    target_url: document.getElementById('target_url').value,
                    request_method: document.getElementById('request_method').value,
                    request_headers: document.getElementById('request_headers').value
                        ? document.getElementById('request_headers').value.split(',').map(h => h.trim()).filter(Boolean)
                        : [],
                    with_credentials: document.getElementById('with_credentials').value === 'true'
                };

                const resultBox = document.getElementById('result');
                resultBox.textContent = 'Running simulation...';

                try {
                    const response = await fetch('/api/v1/simulate-preflight', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                    const data = await response.json();
                    resultBox.textContent = JSON.stringify(data, null, 2);
                } catch (error) {
                    resultBox.textContent = 'Request failed: ' + error.message;
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "CORSFixer Core Engine"}

@app.post("/api/v1/simulate-preflight", response_model=AnalysisResponse)
async def simulate_preflight(payload: SimulationRequest):
    try:
        return SimulatorEngine.run_simulation(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)