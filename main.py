import cloudscraper
import time
import chat
import asyncio

def esta_en_directo(nombre_canal):
    scraper = cloudscraper.create_scraper()
    url = f"https://kick.com/api/v1/channels/{nombre_canal}"
    try:
        response = scraper.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("livestream"):
            print(f"✅ El canal '{nombre_canal}' está EN DIRECTO.")
            return True
        else:
            print(f"❌ El canal '{nombre_canal}' NO está en directo.")
            return False
    except Exception as e:
        print(f"⚠️ Error al consultar el canal: {e}")
        return False

if __name__ == "__main__":
    canal = input("¿Qué canal quieres stremear? ").strip()
    intervalo = 1  # segundos entre comprobaciones

    while True:
        if esta_en_directo(canal):
            print(f"¡El canal '{canal}' ya está en directo! Puedes comenzar a streamear.")
            
            # Obtiene chatroom_id y luego escucha el chat con asyncio.run
            chatroom_id = chat.obtener_chatroom_id(canal)
            if chatroom_id:
                asyncio.run(chat.escuchar_chat(chatroom_id))
            else:
                print(f"❌ No se pudo obtener el chatroom ID para el canal '{canal}'.")
                
            break
        else:
            print(f"Volver a comprobar el canal '{canal}' en {intervalo} segundos...\n")
            time.sleep(intervalo)
