const { MsEdgeTTS, OUTPUT_FORMAT } = require('msedge-tts');

exports.handler = async (event, context) => {
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            body: ''
        };
    }

    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Method Not Allowed. Use POST.' })
        };
    }

    try {
        let body = {};
        if (event.body) {
            const rawBody = event.isBase64Encoded ? Buffer.from(event.body, 'base64').toString('utf8') : event.body;
            body = JSON.parse(rawBody);
        }

        const text = (body.text || '').trim();
        const voice = body.voice || 'es-CO-SalomeNeural';
        const rate = body.rate || '+0%';
        const pitch = body.pitch || '+0Hz';

        if (!text) {
            return {
                statusCode: 400,
                headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
                body: JSON.stringify({ error: "El campo 'text' es obligatorio" })
            };
        }

        const tts = new MsEdgeTTS();
        await tts.setMetadata(voice, OUTPUT_FORMAT.AUDIO_24KHZ_48KBITRATE_MONO_MP3);
        
        const readable = tts.toStream(text, {
            rate: rate,
            pitch: pitch
        });

        const chunks = [];
        for await (const chunk of readable) {
            chunks.push(chunk);
        }
        const audioBuffer = Buffer.concat(chunks);

        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'audio/mpeg',
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'public, max-age=86400'
            },
            body: audioBuffer.toString('base64'),
            isBase64Encoded: true
        };

    } catch (err) {
        console.error('Error generando TTS:', err);
        return {
            statusCode: 500,
            headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: err.message || 'Internal Server Error' })
        };
    }
};
