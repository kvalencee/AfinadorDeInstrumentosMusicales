# � Desplegar en Firebase

## Opción Recomendada: Render (Más Fácil para Flask)

Firebase Hosting es para sitios estáticos. Para Flask necesitas un servidor, así que **Render es mejor**.

### Pasos Rápidos:

1. **Crear cuenta en Render**: https://render.com (gratis con GitHub)

2. **Nuevo Web Service**:
   - Click "New +" → "Web Service"
   - Conecta tu repo: `https://github.com/kvalencee/AfinadorDeInstrumentosMusicales`
   - **Root Directory**: `web`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

3. **Deploy**:
   - Click "Create Web Service"
   - Espera 2-3 minutos
   - ¡Listo! Te da una URL como: `https://afinador-musical.onrender.com`

---

## Alternativa: Railway

1. **Crear cuenta**: https://railway.app
2. **Deploy**: Click "New Project" → "Deploy from GitHub"
3. Selecciona tu repo
4. Railway detecta Flask automáticamente
5. ¡Listo! URL: `https://afinador-musical.up.railway.app`

---

## ⚠️ Nota sobre Firebase

Firebase Hosting solo sirve para HTML/CSS/JS estáticos. Para Flask necesitas:
- Firebase Cloud Functions (más complicado)
- O mejor usa Render/Railway (gratis y más fácil)

---

## ✅ Recomendación Final

**Usa Render.com** - Es gratis, fácil, y perfecto para Flask.

Tu profesora solo abrirá el link y funcionará en cualquier dispositivo.
