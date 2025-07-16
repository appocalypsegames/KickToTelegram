import time
import cloudscraper
import asyncio
import config
import chat
import stream_kick_to_telegram
import multiprocessing
import random

from telethon.sync import TelegramClient
from telethon.tl.functions.phone import CreateGroupCallRequest, DiscardGroupCallRequest, JoinGroupCallRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerChannel, InputChannel, DataJSON

# Configuración Telegram (usa cuenta personal, no bot)
API_ID = config.TG_API_ID
API_HASH = config.TG_API_HASH
SESSION_NAME = "telegram_session"
GROUP_ID = config.TG_GROUP_ID 
GROUP_ACCESS_HASH = config.TG_ACCESS_HASH

call = None  # llamada activa (estado global)

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

def verificar_canal_telegram():
    """Verifica que el canal de Telegram existe y es accesible"""
    try:
        with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
            input_channel = InputPeerChannel(GROUP_ID, GROUP_ACCESS_HASH)
            full_channel = client(GetFullChannelRequest(input_channel))
            
            # Obtener información del canal de manera más segura
            if hasattr(full_channel, 'full_chat') and hasattr(full_channel.full_chat, 'title'):
                print(f"✅ Canal de Telegram verificado: {full_channel.full_chat.title}")
            elif hasattr(full_channel, 'chats') and full_channel.chats:
                chat = full_channel.chats[0]
                if hasattr(chat, 'title'):
                    print(f"✅ Canal de Telegram verificado: {chat.title}")
                else:
                    print(f"✅ Canal de Telegram verificado (ID: {chat.id})")
            else:
                print("✅ Canal de Telegram verificado")
            
            return True
    except Exception as e:
        print(f"❌ Error al verificar canal de Telegram: {e}")
        return False

def iniciar_llamada():
    global call
    with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        try:
            # Obtener información del canal primero
            print(f"🔍 Verificando canal con ID: {GROUP_ID}")
            print(f"🔍 Access Hash: {GROUP_ACCESS_HASH}")
            
            # Crear el objeto InputPeerChannel
            input_channel = InputPeerChannel(GROUP_ID, GROUP_ACCESS_HASH)
            print(f"✅ InputPeerChannel creado: {input_channel}")
            
            # Verificar que el canal existe y obtener información completa
            full_channel = client(GetFullChannelRequest(input_channel))
            
            # Obtener información del canal de manera más segura
            if hasattr(full_channel, 'full_chat') and hasattr(full_channel.full_chat, 'title'):
                print(f"✅ Canal encontrado: {full_channel.full_chat.title}")
                print(f"✅ Tipo de canal: {type(full_channel.full_chat)}")
            elif hasattr(full_channel, 'chats') and full_channel.chats:
                chat = full_channel.chats[0]
                if hasattr(chat, 'title'):
                    print(f"✅ Canal encontrado: {chat.title}")
                else:
                    print(f"✅ Canal encontrado (ID: {chat.id})")
                print(f"✅ Tipo de canal: {type(chat)}")
            else:
                print("✅ Canal encontrado")
                print("✅ Tipo de canal: ChannelFull")
            
            # Crear la llamada grupal
            random_id = random.randint(-2147483648, 2147483647)
            print(f"🎲 Random ID para la llamada: {random_id}")
            
            # Crear llamada de video grupal
            result = client(CreateGroupCallRequest(
                peer=input_channel,
                random_id=random_id,
                title="Stream desde Kick",  # Título de la llamada
                schedule_date=None,  # Inmediata
                rtmp_stream=True  # Habilitar streaming RTMP
            ))
            
            print(f"🔍 Tipo de resultado: {type(result)}")
            print(f"🔍 Atributos del resultado: {dir(result)}")
            
            # Obtener la información de la llamada de manera más segura
            if hasattr(result, 'call'):
                call = result.call
                print("📹 Llamada de video iniciada en el grupo.")
                print(f"📹 ID de la llamada: {call.id}")
            elif hasattr(result, 'updates') and result.updates:
                print(f"🔍 Número de updates: {len(result.updates)}")
                # Buscar la actualización de la llamada en las updates
                for i, update in enumerate(result.updates):
                    print(f"🔍 Update {i}: {type(update)} - {dir(update)}")
                    if hasattr(update, 'call'):
                        call = update.call
                        print("📹 Llamada de video iniciada en el grupo.")
                        print(f"📹 ID de la llamada: {call.id}")
                        break
                else:
                    print("⚠️ Llamada de video iniciada pero no se pudo obtener el ID")
                    call = None
            else:
                print("⚠️ Llamada de video iniciada pero no se pudo obtener información detallada")
                call = None
            
            # Unirse a la llamada como participante
            if call:
                try:
                    join_result = client(JoinGroupCallRequest(
                        call=call,
                        join_as=input_channel,
                        params=DataJSON(data='{"ufrag":"","pwd":"","hash":"","setup":"","fingerprint":"","source":""}'),
                        muted=False,
                        video_stopped=False,
                        stream_type=None
                    ))
                    print("✅ Te has unido a la llamada de video como participante.")
                except Exception as e:
                    print(f"⚠️ No se pudo unir a la llamada: {e}")
            
        except Exception as e:
            print(f"❌ Error al iniciar llamada: {e}")
            print(f"❌ Tipo de error: {type(e)}")
            raise

def cerrar_llamada():
    global call
    if not call:
        print("ℹ️ No hay llamada activa para cerrar.")
        return

    with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        client(DiscardGroupCallRequest(call))
        print("📴 Llamada finalizada.")
        call = None

def proceso_chat(canal):
    chatroom_id = chat.obtener_chatroom_id(canal)
    if chatroom_id:
        asyncio.run(chat.escuchar_chat(chatroom_id))
    else:
        print(f"❌ No se pudo obtener el chatroom ID para el canal '{canal}'.")

def proceso_stream(canal):
    stream_kick_to_telegram.stream_kick_canal_con_streamlink(canal)

if __name__ == "__main__":
    canal = config.KICK_CHANNEL
    intervalo = 10  # segundos

    llamada_activa = False

    # Verificar canal de Telegram al inicio
    print("🔍 Verificando configuración de Telegram...")
    if not verificar_canal_telegram():
        print("❌ No se pudo verificar el canal de Telegram. Verifica la configuración.")
        exit(1)
    
    print("✅ Configuración de Telegram verificada correctamente.")

    while True:
        if esta_en_directo(canal):
            if not llamada_activa:
                print("📹 Intentando iniciar llamada de video grupal...")
                iniciar_llamada()
                llamada_activa = True

            print(f"🎥 Iniciando retransmisión del canal '{canal}'...")

            while esta_en_directo(canal):
                p_chat = multiprocessing.Process(target=proceso_chat, args=(canal,))
                p_stream = multiprocessing.Process(target=proceso_stream, args=(canal,))

                p_chat.start()
                p_stream.start()

                p_chat.join()
                p_stream.join()

                print("🔁 Procesos finalizados. Reiniciando en 5 segundos...")
                time.sleep(5)

            print("📴 El canal dejó de estar en directo.")
            if llamada_activa:
                cerrar_llamada()
                llamada_activa = False

        else:
            print(f"🔄 Canal '{canal}' no está en vivo. Reintentando en {intervalo} segundos...\n")

        time.sleep(intervalo)
