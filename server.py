from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
import json
import requests

app = FastAPI()
BASE_URL = "https://aria-audit-api.onrender.com"

# Handshake inicial MCP (POST requerido por ChatGPT)
@app.post("/sse")
async def handshake():
    return JSONResponse({
        "type": "mcp/handshake",
        "version": "2024-01-01",
        "capabilities": ["tools"]
    })

# Mantener GET también para debug en navegador
@app.get("/sse")
async def sse_debug():
    async def event_generator():
        yield {
            "event": "message",
            "data": json.dumps({
                "type": "mcp/handshake",
                "version": "2024-01-01",
                "capabilities": ["tools"]
            })
        }
    return EventSourceResponse(sse_debug())

# Herramientas MCP simuladas
@app.get("/mcp/get_reports")
def get_reports(limit: int = 10):
    r = requests.get(f"{BASE_URL}/reports?limit={limit}")
    return r.json()

@app.get("/mcp/get_report/{report_id}")
def get_report(report_id: str):
    r = requests.get(f"{BASE_URL}/report/{report_id}")
    return r.json()
