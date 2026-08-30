# 🎙️ Servidor TTS Salomé para Netlify

Este paquete contiene todo lo necesario para desplegar tu API de voz de Salomé en **Netlify** de forma 100% gratuita.

---

## 🚀 Método 1: Despliegue con 1 clic (Vía GitHub)

1. Sube el contenido de esta carpeta (`servidor_netlify`) a un repositorio nuevo en tu cuenta de **GitHub**.
2. Entra a [https://app.netlify.com](https://app.netlify.com).
3. Haz clic en **"Add new site"** -> **"Import an existing project"** -> Selecciona tu repositorio de GitHub.
4. Netlify detectará automáticamente el archivo `netlify.toml` y `requirements.txt`.
5. Haz clic en **"Deploy site"**.
6. ¡Listo! Te dará una URL como: `https://tu-proyecto.netlify.app`.

---

## 🚀 Método 2: Despliegue rápido con Netlify CLI

Si tienes Node.js instalado, puedes ejecutar en esta carpeta:
```bash
npm install -g netlify-cli
netlify deploy --prod
```

---

## 📱 ¿Cómo usar la URL en tu app de Android (YapeTV)?

Una vez desplegado en Netlify, abre tu proyecto en Android Studio y en `SalomeVoiceManager.kt` coloca tu enlace de Netlify:

```kotlin
var ttsServerUrl: String = "https://tu-proyecto.netlify.app/tts"
```

¡Y tu app funcionará desde cualquier lugar del mundo las 24 horas del día sin necesidad de tu PC!
