import asyncio
import io
import os
import sys
from aiohttp import web
import edge_tts

# Puerto asignado por Render / Koyeb / Cloud o 8000 por defecto
PORT = int(os.environ.get("PORT", 8000))

async def handle_tts(request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        voice = data.get("voice", "es-CO-SalomeNeural")
        rate = data.get("rate", "+0%")
        pitch = data.get("pitch", "+0Hz")

        if not text:
            return web.json_response({"error": "Texto vacio"}, status=400)

        print(f"[TTS] Peticion recibida: '{text}' con voz '{voice}'")
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        
        audio_stream = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.extend(chunk["data"])

        print(f"[TTS] OK Generado audio exitosamente ({len(audio_stream)} bytes)")
        return web.Response(
            body=bytes(audio_stream),
            content_type="audio/mpeg",
            headers={"Access-Control-Allow-Origin": "*"}
        )

    except Exception as e:
        print(f"[TTS] Error: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def handle_index(request):
    html_file = os.path.join(os.path.dirname(__file__), "public", "index.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        return web.Response(text=content, content_type="text/html")
    return web.Response(text="Servidor TTS Salome Cloud Activo", content_type="text/plain")

async def init_app():
    app = web.Application()
    app.router.add_post("/tts", handle_tts)
    app.router.add_get("/tts", handle_tts)
    app.router.add_get("/", handle_index)
    return app

if __name__ == "__main__":
    print(f"Servidor TTS Salome Cloud activo en puerto {PORT}")
    web.run_app(init_app(), host="0.0.0.0", port=PORT)
