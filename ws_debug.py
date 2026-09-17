from fastapi import FastAPI, WebSocket
import uvicorn

print("🔥 LOADED MY WS_DEBUG.PY")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "WS debug server"}


@app.websocket("/ws/test/{room_id}")
async def websocket_test(
    websocket: WebSocket,
    room_id: str,
):
    print(f"🔥 HANDLER REACHED: {room_id}")

    await websocket.accept()

    print("✅ WEBSOCKET ACCEPTED")

    message = await websocket.receive_text()

    print(f"📩 RECEIVED: {message}")

    await websocket.send_text(
        f"Server received: {message}"
    )


print("🔥 REGISTERED DEBUG ROUTES:")

for route in app.routes:
    print(
        "PATH:",
        getattr(route, "path", None),
        "NAME:",
        getattr(route, "name", None),
        "TYPE:",
        type(route),
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
    )