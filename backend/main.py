import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from recon import run_recon

app = FastAPI(title="Recon SaaS", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "recon-saas"}

@app.websocket("/ws/recon/{domain}")
async def recon_ws(websocket: WebSocket, domain: str):
    await websocket.accept()
    try:
        async for event in run_recon(domain):
            await websocket.send_text(json.dumps(event))
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_text(json.dumps({"type": "error", "data": {"message": str(e)}}))
    finally:
        await websocket.close()

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
