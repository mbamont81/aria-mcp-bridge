from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
import requests

app = FastAPI()

BASE_URL = "https://aria-audit-api.onrender.com"

# Evento MCP básico (simula el protocolo MCP)
@app.get("/sse")
async def sse_endpoint():
    async def event_generator():
        yield {"event": "message", "data": "✅ MCP connector activo"}
    return EventSourceResponse(event_generator())

# Herramienta 1: Listar reportes
@app.get("/mcp/get_reports")
def get_reports(limit: int = 10):
    r = requests.get(f"{BASE_URL}/reports?limit={limit}")
    return JSONResponse(r.json())

# Herramienta 2: Obtener reporte por ID
@app.get("/mcp/get_report/{report_id}")
def get_report(report_id: str):
    r = requests.get(f"{BASE_URL}/report/{report_id}")
    return JSONResponse(r.json())

# Herramienta 3: Estadísticas de la base de datos
@app.get("/mcp/database_stats")
def get_db_stats():
    r = requests.get(f"{BASE_URL}/database-stats")
    return JSONResponse(r.json())
