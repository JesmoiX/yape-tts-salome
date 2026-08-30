import json
import base64
import asyncio
import edge_tts

def handler(event, context):
    http_method = event.get("httpMethod", "GET")

    if http_method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
            },
            "body": ""
        }

    if http_method == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"status": "ok", "service": "TTS Salome Netlify", "ready": True})
        }

    if http_method != "POST":
        return {
            "statusCode": 405,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Method Not Allowed. Use POST."})
        }

    try:
        body_str = event.get("body", "{}")
        if event.get("isBase64Encoded", False):
            body_str = base64.b64decode(body_str).decode("utf-8")
        
        data = json.loads(body_str) if body_str else {}
        text = data.get("text", "").strip()
        voice = data.get("voice", "es-CO-SalomeNeural")
        rate = data.get("rate", "+0%")
        pitch = data.get("pitch", "+0Hz")

        if not text:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "El campo 'text' es obligatorio"})
            }

        async def generate_audio():
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            stream = bytearray()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    stream.extend(chunk["data"])
            return bytes(stream)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            audio_bytes = loop.run_until_complete(generate_audio())
        finally:
            loop.close()

        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "audio/mpeg",
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "public, max-age=86400"
            },
            "body": b64_audio,
            "isBase64Encoded": True
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
