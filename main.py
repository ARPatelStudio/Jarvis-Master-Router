
# ==============================================================================
# ⚡ JARVIS-MASTER-ROUTER (Phase 1 - Cloud Gateway & WSS Nervous System)
# Developed By: AR PATEL STUDIO (Amit Patel)
# ==============================================================================

import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

# 🚀 Logger Setup for Production
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] [%(name)s] %(message)s")
logger = logging.getLogger("Jarvis-Master-Router")

# 🚀 FastAPI Initialization
app = FastAPI(
    title="Jarvis-Master-Router",
    description="Universal Cloud Brain for AR PATEL STUDIO Ecosystem",
    version="2026.1.0"
)

# CORS Setup (To allow connections from any device/frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# 🧠 DEVICE REGISTRY & CONNECTION MANAGER (Multi-Device Support)
# ==============================================================================
class ConnectionManager:
    def __init__(self):
        # Dictionary to store active devices (e.g., {"PHONE-001": <WebSocket object>})
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, device_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[device_id] = websocket
        logger.info(f"🟢 Device Connected: {device_id} | Total Active: {len(self.active_connections)}")

    def disconnect(self, device_id: str):
        if device_id in self.active_connections:
            del self.active_connections[device_id]
            logger.warning(f"🔴 Device Disconnected: {device_id} | Total Active: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, device_id: str):
        if device_id in self.active_connections:
            websocket = self.active_connections[device_id]
            await websocket.send_json(message)

manager = ConnectionManager()

# ==============================================================================
# 🌐 REST API ENDPOINTS (Health Checks & Webhooks)
# ==============================================================================
@app.get("/")
async def root():
    return {
        "status": "Online",
        "system": "Jarvis-Master-Router",
        "developer": "AR PATEL STUDIO",
        "message": "Cloud Brain is Active and Listening."
    }

# ==============================================================================
# ⚡ WEBSOCKET ENDPOINT (The Real-Time Nervous System)
# ==============================================================================
@app.websocket("/ws/jarvis/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await manager.connect(device_id, websocket)
    try:
        while True:
            # Wait for incoming messages from Android/PC
            raw_data = await websocket.receive_text()
            payload = json.loads(raw_data)
            
            logger.info(f"📩 Received from {device_id}: {payload}")

            action_type = payload.get("action_type", "UNKNOWN")

            # 🧠 MASTER ROUTING LOGIC (Blueprint for next phases)
            if action_type == "PROCESS_WHATSAPP":
                # FUTURE: Here we will call Groq API
                sender = payload.get("sender_name", "Unknown")
                msg = payload.get("message", "")
                
                logger.info(f"Routing WhatsApp message from {sender} to LLM Engine...")
                
                # Mock Response (Until Groq is integrated in Phase 2)
                response_payload = {
                    "status": "SUCCESS",
                    "action": "SEND_WHATSAPP_REPLY",
                    "target_app": "com.whatsapp",
                    "contact_name": sender,
                    "reply_text": f"Boss, {sender} ka message cloud par aagaya hai. (API integration pending)"
                }
                await manager.send_personal_message(response_payload, device_id)

            elif action_type == "GENERATE_IMAGE":
                # FUTURE: Here we will trigger n8n webhook
                pass

            else:
                logger.warning(f"Unknown action type received: {action_type}")

    except WebSocketDisconnect:
        manager.disconnect(device_id)
    except Exception as e:
        logger.error(f"Error in WebSocket: {e}")
        manager.disconnect(device_id)
