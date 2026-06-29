"""FastAPI + WebSocket server for the dashboard."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from opendbc.simulation.engine import SimulationEngine
from opendbc.simulation.profiles import PROFILES


engine = SimulationEngine()
ws_clients: set[WebSocket] = set()


async def _broadcast_async(msg: dict) -> None:
  dead: list[WebSocket] = []
  for ws in list(ws_clients):
    try:
      await ws.send_json(msg)
    except Exception:
      dead.append(ws)
  for ws in dead:
    ws_clients.discard(ws)


def _broadcast(msg: dict) -> None:
  try:
    loop = asyncio.get_running_loop()
    loop.create_task(_broadcast_async(msg))
  except RuntimeError:
    pass


engine.on_broadcast(_broadcast)


@asynccontextmanager
async def lifespan(app: FastAPI):
  task = asyncio.create_task(engine.run_loop(0.45))
  yield
  task.cancel()


app = FastAPI(title="Vehicle Cybersecurity Gateway API", lifespan=lifespan)
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


class ProfileBody(BaseModel):
  profile_id: str


class OperationBody(BaseModel):
  operation: str


class SettingsBody(BaseModel):
  presentation_mode: bool | None = None
  privacy_mode: bool | None = None


class IgnitionBody(BaseModel):
  on: bool


class DoorsBody(BaseModel):
  open: bool


class EcuBody(BaseModel):
  ecu: str


@app.get("/api/state")
def get_state() -> dict[str, Any]:
  return engine.get_state()


@app.get("/api/profiles")
def list_profiles() -> list[dict]:
  return [{"id": p.id, "label": p.label, "dbc": p.dbc} for p in PROFILES.values()]


@app.post("/api/profile")
def set_profile(body: ProfileBody) -> dict:
  ok = engine.set_profile(body.profile_id)
  return {"ok": ok}


@app.post("/api/auth/connect")
def auth_connect() -> dict:
  return engine.connect_device()


@app.post("/api/auth/challenge")
def auth_challenge() -> dict:
  return engine.request_challenge()


@app.post("/api/auth/sign")
def auth_sign() -> dict:
  return engine.sign_challenge()


@app.post("/api/auth/disconnect")
def auth_disconnect() -> dict:
  return engine.disconnect()


@app.post("/api/auth/revoke")
def auth_revoke() -> dict:
  return engine.revoke_session()


@app.post("/api/controls/enable")
def enable_controls() -> dict:
  return engine.enable_controls()


@app.post("/api/request")
def process_request(body: OperationBody) -> dict:
  return engine.process_request(body.operation)


@app.post("/api/attack/{attack_type}")
def run_attack(attack_type: str) -> dict:
  return engine.run_attack(attack_type)


@app.post("/api/vehicle/ignition")
def set_ignition(body: IgnitionBody) -> dict:
  engine.set_ignition(body.on)
  return {"ok": True}


@app.post("/api/vehicle/doors")
def set_doors(body: DoorsBody) -> dict:
  engine.set_doors(body.open)
  return {"ok": True}


@app.post("/api/vehicle/ecu-offline")
def ecu_offline(body: EcuBody) -> dict:
  engine.disconnect_ecu(body.ecu)
  return {"ok": True}


@app.post("/api/vehicle/battery-drop")
def battery_drop() -> dict:
  engine.simulate_battery_drop()
  return {"ok": True}


@app.post("/api/settings")
def update_settings(body: SettingsBody) -> dict:
  if body.presentation_mode is not None:
    engine._presentation_mode = body.presentation_mode  # noqa: SLF001
  if body.privacy_mode is not None:
    engine._privacy_mode = body.privacy_mode  # noqa: SLF001
  return {"ok": True}


@app.post("/api/demo/run")
async def demo_run() -> dict:
  asyncio.create_task(engine.run_full_demo())
  return {"ok": True, "started": True}


@app.post("/api/demo/reset")
def demo_reset() -> dict:
  engine.reset()
  return {"ok": True}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket) -> None:
  await ws.accept()
  ws_clients.add(ws)
  await ws.send_json({"type": "state", "payload": engine.get_state()})
  try:
    while True:
      data = await ws.receive_json()
      action = data.get("action")
      if action == "ping":
        await ws.send_json({"type": "pong", "payload": {}})
      elif action == "get_state":
        await ws.send_json({"type": "state", "payload": engine.get_state()})
  except WebSocketDisconnect:
    ws_clients.discard(ws)


def main() -> None:
  import uvicorn
  uvicorn.run("opendbc.simulation.server:app", host="0.0.0.0", port=8080, reload=False)


if __name__ == "__main__":
  main()
