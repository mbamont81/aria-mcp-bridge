from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import requests
import json
import asyncio

app = FastAPI()
BASE_URL = "https://aria-audit-api.onrender.com"

# 🔹 Handshake inicial MCP (SSE Stream)
@app.get("/sse")
async def mcp_handshake():
    def generate_sse():
        # Enviar handshake inicial
        handshake = {
            "type": "mcp/handshake",
            "version": "2024-01-01",
            "capabilities": ["tools"],
            "tools": [
                {
                    "name": "get_reports",
                    "description": "Listar los reportes históricos guardados en Render",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Número máximo de reportes a devolver"
                            }
                        },
                        "required": []
                    }
                },
                {
                    "name": "get_report",
                    "description": "Obtener un reporte específico por ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "report_id": {
                                "type": "string",
                                "description": "El ID único del reporte"
                            }
                        },
                        "required": ["report_id"]
                    }
                }
            ],
            "resources": [],
            "instructions": "Conector MCP para consultar reportes y auditorías de Aria Audit API en Render"
        }
        
        yield f"data: {json.dumps(handshake)}\n\n"
        
        # Mantener la conexión viva con pings
        while True:
            yield f"data: {json.dumps({'type': 'ping', 'timestamp': '2024-01-01T00:00:00Z'})}\n\n"
            yield from asyncio.sleep(30)  # Ping cada 30 segundos
    
    return StreamingResponse(
        generate_sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )

# �� Herramienta 1: Listar reportes
@app.get("/mcp/get_reports")
def get_reports(limit: int = 10):
    try:
        r = requests.get(f"{BASE_URL}/reports?limit={limit}", timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# 🔹 Herramienta 2: Obtener un reporte por ID
@app.get("/mcp/get_report/{report_id}")
def get_report(report_id: str):
    try:
        r = requests.get(f"{BASE_URL}/report/{report_id}", timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
