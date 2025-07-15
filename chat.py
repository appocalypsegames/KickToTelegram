import asyncio
import json
import websockets
import requests
import cloudscraper

def obtener_chatroom_id(username):
    scraper = cloudscraper.create_scraper()  # Simula navegador con cookies y JS
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
    
#Escucha el chat de un chatroom y lo pinta en consola
async def escuchar_chat(chatroom_id):
    ws_url = "wss://ws-us2.pusher.com/app/32cbd69e4b950bf97679?protocol=7&client=js&version=7.6.0"
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
                    print(f"{username}: {message}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
                break