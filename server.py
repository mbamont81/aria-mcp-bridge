from fastapi import FastAPI, Request
from fastapi.responses import EventSourceResponse
import json
import requests

app = FastAPI()
BASE_URL = "https://aria-audit-api.onrender.com"

@app.get("/sse")
async def sse_endpoint(request: Request):
    async def event_generator():
        # Handshake inicial requerido por MCP
        yield {
            "event": "message",
            "data": json.dumps({
                "type": "mcp/handshake",
                "version": "2024-01-01",
                "capabilities": ["tools"]
            })
        }
    return EventSourceResponse(event_generator())

@app.get("/mcp/get_reports")
def get_reports(limit: int = 10):
    r = requests.get(f"{BASE_URL}/reports?limit={limit}")
    return r.json()

@app.get("/mcp/get_report/{report_id}")
def get_report(report_id: str):
    r = requests.get(f"{BASE_URL}/report/{report_id}")
    return r.json()
