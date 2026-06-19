import os
import socket
import time
from fastapi import FastAPI

app = FastAPI()

APP_VERSION = os.getenv("APP_VERSION", "local")
HOSTNAME = socket.gethostname()


@app.get("/")
def root():
    return {
        "message": "hello from eks autoscaling project",
        "version": APP_VERSION,
        "hostname": HOSTNAME,
    }


@app.get("/healthz/live")
def live():
    return {"status": "live"}


@app.get("/healthz/ready")
def ready():
    return {"status": "ready"}


@app.get("/cpu")
def cpu_work(seconds: int = 1):
    end = time.time() + seconds
    result = 0

    while time.time() < end:
        result += 1

    return {
        "status": "done",
        "seconds": seconds,
        "hostname": HOSTNAME,
        "result": result,
    }