from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

app = FastAPI()
BASE_URL = "https://aria-audit-api.onrender.com"

# 🔹 Handshake inicial MCP (ChatGPT usa este POST)
@app.post("/sse")
async def handshake():
    return JSONResponse({
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
    })

# 🔹 Debug manual (GET para navegador)
@app.get("/sse")
async def handshake_debug():
    return {
        "type": "mcp/handshake",
        "version": "2024-01-01",
        "capabilities": ["tools"],
        "note": "Este es solo debug. El POST /sse es el que usa ChatGPT y devuelve las tools."
    }

# 🔹 Herramienta 1: Listar reportes
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
