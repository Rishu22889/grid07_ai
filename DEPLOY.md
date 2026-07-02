# 🚀 Vercel Deployment Guide

## Quick Deploy

### 1. Deploy to Vercel
```bash
vercel
```

**When prompted:**
- Pull development environment variables? → **No** (press Enter)
- Set up and deploy? → **Yes**
- Which scope? → Select your account
- Link to existing project? → **No**
- Project name? → `grid07-ai` (or your choice)
- Directory? → `.` (press Enter)
- Override settings? → **No** (press Enter)

### 2. Add Environment Variables in Vercel Dashboard

After deployment completes:

1. Go to: https://vercel.com/dashboard
2. Click on your project (`grid07-ai`)
3. Go to **Settings** → **Environment Variables**
4. Add these variables:

```
GROQ_API_KEY = your_groq_api_key_here
GOOGLE_API_KEY = your_google_api_key_here
GROQ_MODEL = llama-3.1-8b-instant
EMBEDDING_MODEL = models/gemini-embedding-001
ROUTING_THRESHOLD = 0.5
```

### 3. Redeploy with Environment Variables
```bash
vercel --prod
```

## ✅ Done!

Your chatbot will be live at: `https://grid07-ai-xxxxx.vercel.app`

## 📝 Notes

- `.env` file stays local (never push to GitHub)
- Environment variables are set in Vercel Dashboard
- Redeploy after adding env vars for them to take effect

---

**Your project structure:**
- `index.html` - Frontend chatbot
- `app/web_api.py` - Backend API
- `vercel.json` - Vercel configuration
