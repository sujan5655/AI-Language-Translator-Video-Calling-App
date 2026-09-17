from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter()


rooms: dict[str, list[WebSocket]] = {}


@router.websocket("/ws/signaling/{room_id}")
async def signaling_socket(
    websocket: WebSocket,
    room_id: str,
):
    await websocket.accept()

    print(
        f"🟢 WebRTC user joined room: {room_id}"
    )

    if room_id not in rooms:
        rooms[room_id] = []

    room = rooms[room_id]

    # Only support 2 participants for the MVP.
    if len(room) >= 2:
        print(
            f"⚠️ Room {room_id} is already full"
        )

        await websocket.send_json(
            {
                "type": "room-full",
            }
        )

        await websocket.close()

        return

    room.append(websocket)

    participant_number = len(room)

    print(
        f"👥 Users in room {room_id}: "
        f"{participant_number}"
    )

    # Tell the participant whether they are
    # the caller or callee.
    if participant_number == 1:
        await websocket.send_json(
            {
                "type": "role",
                "role": "caller",
            }
        )

        print(
            f"📞 User in {room_id} assigned role: caller"
        )

    else:
        await websocket.send_json(
            {
                "type": "role",
                "role": "callee",
            }
        )

        print(
            f"📞 User in {room_id} assigned role: callee"
        )

        # Tell the first participant that
        # another user has joined.
        try:
            await room[0].send_json(
                {
                    "type": "peer-joined",
                }
            )

            print(
                f"📢 Notified caller that "
                f"peer joined room {room_id}"
            )

        except Exception as error:
            print(
                "❌ Failed to notify caller:",
                error,
            )

    try:
        while True:
            message = await websocket.receive_text()

            print(
                f"📩 Signaling message in "
                f"{room_id}: {message}"
            )

            for client in room:
                if client is websocket:
                    continue

                try:
                    await client.send_text(message)

                    print(
                        f"📤 Forwarded signaling "
                        f"message to peer in {room_id}"
                    )

                except Exception as error:
                    print(
                        "❌ Failed to forward "
                        "signaling message:",
                        error,
                    )

    except WebSocketDisconnect:
        print(
            f"🔴 WebRTC user left room: {room_id}"
        )

        if room_id in rooms:
            room = rooms[room_id]

            if websocket in room:
                room.remove(websocket)

            print(
                f"👥 Users remaining in "
                f"{room_id}: {len(room)}"
            )

            if not room:
                del rooms[room_id]

                print(
                    f"🗑️ Room deleted: {room_id}"
                )