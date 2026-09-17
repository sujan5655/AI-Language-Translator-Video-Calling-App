import asyncio
import websocket

import websocket


url = "ws://127.0.0.1:8000/ws/test/demo-room"

print(f"Connecting to: {url}")

try:
    ws = websocket.create_connection(url)

    print("✅ WEBSOCKET CONNECTED")

    ws.send("hello")

    response = ws.recv()

    print(f"📩 SERVER RESPONSE: {response}")

    ws.close()

except Exception as error:
    print(f"❌ WEBSOCKET TEST FAILED: {error}")