from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

app = FastAPI()
BASE_URL = "https://aria-audit-api.onrender.com"

# Handshake inicial MCP (ChatGPT hace POST aquí)
@app.post("/sse")
async def handshake():
    return JSONResponse({
        "type": "mcp/handshake",
        "version": "2024-01-01",
        "capabilities": ["tools"]
    })

# Debug manual desde navegador (opcional)
@app.get("/sse")
async def handshake_debug():
    return {
        "type": "mcp/handshake",
        "version": "2024-01-01",
        "capabilities": ["tools"]
    }

# Herramientas MCP simuladas
@app.get("/mcp/get_reports")
def get_reports(limit: int = 10):
    r = requests.get(f"{BASE_URL}/reports?limit={limit}")
    return r.json()

@app.get("/mcp/get_report/{report_id}")
def get_report(report_id: str):
    r = requests.get(f"{BASE_URL}/report/{report_id}")
    return r.json()
