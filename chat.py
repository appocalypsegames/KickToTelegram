import asyncio
import json
import websockets
import requests
import cloudscraper
from collections import deque

def obtener_chatroom_id(username):
    scraper = cloudscraper.create_scraper()
    url = f"https://kick.com/api/v1/channels/{username}"

    try:
        response = scraper.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            chatroom = data.get("chatroom")
            if chatroom:
                return chatroom.get("id")
            else:
                print("El canal no tiene chatroom disponible.")
        else:
            print(f"Error {response.status_code}: no se pudo acceder al canal '{username}'.")
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

async def escuchar_chat(chatroom_id):
    ws_url = "wss://ws-us2.pusher.com/app/32cbd69e4b950bf97679?protocol=7&client=js&version=7.6.0"
    mensajes = deque(maxlen=5)  # Guardará los últimos 5 mensajes

    async with websockets.connect(ws_url) as websocket:
        join_payload = {
            "event": "pusher:subscribe",
            "data": {
                "auth": "",
                "channel": f"chatrooms.{chatroom_id}.v2"
            }
        }
        await websocket.send(json.dumps(join_payload))
        print(f"🟢 Escuchando chatroom ID {chatroom_id}...\n")

        while True:
            try:
                msg = await websocket.recv()
                payload = json.loads(msg)

                if payload.get("event") == "App\\Events\\ChatMessageEvent":
                    message_data = json.loads(payload["data"])
                    username = message_data["sender"]["username"]
                    message = message_data["content"]
                    mensaje_formateado = f"{username}: {message}"

                    mensajes.append(mensaje_formateado)

                    # Escribir todos los mensajes en chat.txt
                    with open("chat.txt", "w", encoding="utf-8") as f:
                        f.write("\n".join(mensajes))

            except Exception as e:
                print(f"⚠️ Error en websocket: {e}")
                break
