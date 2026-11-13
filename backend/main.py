import os
from collections import deque
from datetime import datetime, timezone
from threading import Lock
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Agricultural Rover API",
    version="1.0.0",
    description="Command bridge between the Streamlit dashboard and the ESP32 rover.",
)

# Configure these as Render environment variables.
DASHBOARD_API_KEY = os.getenv("DASHBOARD_API_KEY", "")
DEVICE_API_KEY = os.getenv("DEVICE_API_KEY", "")

ALLOWED_COMMANDS = {
    "F", "B", "L", "R", "S",
    "G", "g", "W", "w", "C", "c",
    "U", "D", "X",
}

command_queue = deque()
queue_lock = Lock()
latest_status = {
    "device_connected": False,
    "last_seen": None,
    "last_command": None,
    "last_command_at": None,
}


class CommandRequest(BaseModel):
    command: str = Field(min_length=1, max_length=1)


class HeartbeatRequest(BaseModel):
    status: str = "online"


def check_dashboard_key(key: Optional[str]):
    if not DASHBOARD_API_KEY or key != DASHBOARD_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid dashboard API key")


def check_device_key(key: Optional[str]):
    if not DEVICE_API_KEY or key != DEVICE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid ESP32 device API key")


@app.get("/")
def root():
    return {"service": "Agricultural Rover API", "ok": True}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/status")
def get_status(x_dashboard_key: Optional[str] = Header(default=None)):
    check_dashboard_key(x_dashboard_key)

    last_seen = latest_status["last_seen"]
    connected = False
    if last_seen:
        try:
            seen = datetime.fromisoformat(last_seen)
            connected = (datetime.now(timezone.utc) - seen).total_seconds() < 20
        except ValueError:
            connected = False

    return {
        "device_connected": connected,
        "last_seen": last_seen,
        "last_command": latest_status["last_command"],
        "last_command_at": latest_status["last_command_at"],
        "queued_commands": len(command_queue),
    }


@app.post("/api/command")
def send_command(
    body: CommandRequest,
    x_dashboard_key: Optional[str] = Header(default=None),
):
    check_dashboard_key(x_dashboard_key)
    command = body.command

    if command not in ALLOWED_COMMANDS:
        raise HTTPException(status_code=400, detail="Unsupported rover command")

    with queue_lock:
        # Emergency stop takes priority: discard queued motion/function commands.
        if command == "X":
            command_queue.clear()
            command_queue.append("X")
        else:
            # Keep the queue bounded if the ESP32 is temporarily offline.
            if len(command_queue) >= 30:
                raise HTTPException(status_code=429, detail="Command queue is full")
            command_queue.append(command)

    return {"accepted": True, "command": command}


@app.get("/api/device/next")
def device_next(x_device_key: Optional[str] = Header(default=None)):
    check_device_key(x_device_key)

    with queue_lock:
        command = command_queue.popleft() if command_queue else None

    latest_status["last_seen"] = datetime.now(timezone.utc).isoformat()
    latest_status["device_connected"] = True

    if command:
        latest_status["last_command"] = command
        latest_status["last_command_at"] = datetime.now(timezone.utc).isoformat()

    return {"command": command}


@app.post("/api/device/heartbeat")
def device_heartbeat(
    body: HeartbeatRequest,
    x_device_key: Optional[str] = Header(default=None),
):
    check_device_key(x_device_key)
    latest_status["last_seen"] = datetime.now(timezone.utc).isoformat()
    latest_status["device_connected"] = True
    return {"ok": True, "status": body.status}
