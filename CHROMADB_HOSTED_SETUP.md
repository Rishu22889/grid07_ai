# Setting Up Hosted ChromaDB for Vercel Deployment

## Why Use Hosted ChromaDB?

Local ChromaDB **cannot run on Vercel** because serverless functions have:
- ❌ No persistent filesystem
- ❌ Read-only environment
- ❌ Fresh container on each request

Hosted ChromaDB solves this by providing a **remote vector database** accessible via HTTP API.

## Option 1: Chroma Cloud (Official Hosted Service)

### Step 1: Sign Up
1. Go to https://www.trychroma.com/
2. Click "Get Started" or "Sign Up"
3. Create an account

### Step 2: Create a Collection
1. After login, create a new workspace
2. Create a collection named `grid07_bots`
3. Set dimension to `768` (Google Gemini embedding size)
4. Set distance metric to `cosine`

### Step 3: Get API Credentials
1. Go to Settings → API Keys
2. Copy your:
   - **Host**: e.g., `api.trychroma.com` or `your-workspace.trychroma.com`
   - **API Key**: Your authentication token

### Step 4: Add to Vercel Environment
```bash
# In Vercel dashboard or CLI:
vercel env add CHROMA_HOST
# Enter: your-workspace.trychroma.com

vercel env add CHROMA_API_KEY
# Enter: your-api-key-here
```

### Step 5: Deploy
```bash
git add .
git commit -m "Add hosted ChromaDB support"
git push origin main
```

## Option 2: Self-Hosted ChromaDB Server

If you prefer to host your own ChromaDB server:

### Requirements
- Docker
- A server with persistent storage (AWS EC2, DigitalOcean, etc.)

### Deploy ChromaDB Server

```bash
# On your server
docker run -d \
  --name chromadb \
  -p 8000:8000 \
  -v chromadb-data:/chroma/chroma \
  -e CHROMA_SERVER_AUTH_CREDENTIALS="admin:your-secure-password" \
  -e CHROMA_SERVER_AUTH_PROVIDER="chromadb.auth.token_authn.TokenAuthenticationServerProvider" \
  chromadb/chroma:latest
```

### Configure Application

Add to Vercel environment:
```bash
CHROMA_HOST=your-server-ip:8000
CHROMA_API_KEY=your-secure-password
```

## Testing the Connection

### Test Locally First

```bash
# Add to .env
CHROMA_HOST=your-instance.trychroma.com
CHROMA_API_KEY=your-api-key

# Restart backend
pkill -f web_api
rm -rf chroma_db/*  # Clear local cache
python app/web_api.py
```

### Check Logs

Look for this message:
```
[ChromaDB] Connecting to hosted instance: your-instance.trychroma.com
[ChromaDB] Using API key authentication
[ChromaDB] Built vector store with 3 bot personas.
```

### Test Routing

```bash
curl -X POST http://localhost:5001/api/route \
  -H "Content-Type: application/json" \
  -d '{"post": "Bitcoin trading strategies", "threshold": 0.25}'
```

Expected response should include:
```json
{
  "method": "semantic_embeddings_chromadb",
  "model": "Google Gemini embeddings + ChromaDB vector store",
  ...
}
```

## Environment Variable Summary

### For Local Development (No hosted ChromaDB)
```env
# .env
GOOGLE_API_KEY=your-google-key
GROQ_API_KEY=your-groq-key
# CHROMA_HOST not set → uses local ./chroma_db/
```

### For Vercel Deployment (With hosted ChromaDB)
```env
# Vercel Environment Variables
GOOGLE_API_KEY=your-google-key
GROQ_API_KEY=your-groq-key
CHROMA_HOST=your-instance.trychroma.com
CHROMA_API_KEY=your-chroma-api-key
```

## Fallback Behavior

The system has automatic fallback:

```
1. Try ChromaDB (hosted or local)
   ↓ fails
2. Try Serverless Semantic Routing (Google Gemini on-demand)
   ↓ fails
3. Use Keyword-Based Routing (pure logic)
   ↓ always works
```

So even if ChromaDB fails, the application continues working!

## Cost Considerations

### Chroma Cloud Pricing (as of 2024)
- **Free Tier**: Limited vectors and queries
- **Paid Tiers**: Based on storage and query volume
- Check https://www.trychroma.com/pricing for current pricing

### Self-Hosted Costs
- **Server**: $5-20/month (DigitalOcean, AWS t2.micro, etc.)
- **Storage**: Minimal (~100MB for 3 bots)
- **Bandwidth**: Minimal

### Alternative: No Vector DB
If cost is a concern, the system works fine with:
- **Serverless Semantic Routing** (Google API calls only)
- **Keyword-Based Routing** (zero cost)

## Troubleshooting

### Error: Connection refused

**Cause**: ChromaDB host not reachable

**Fix**:
1. Check `CHROMA_HOST` value (no `https://` prefix, just domain)
2. Verify ChromaDB server is running
3. Check firewall rules

### Error: Unauthorized

**Cause**: Invalid API key

**Fix**:
1. Verify `CHROMA_API_KEY` is correct
2. Check if key has expired
3. Generate new key from ChromaDB dashboard

### Error: Collection not found

**Cause**: Collection needs to be created

**Fix**: The application automatically creates the collection on first run. If it fails:
1. Check API key has write permissions
2. Manually create collection `grid07_bots` in ChromaDB dashboard
3. Set dimension=768, metric=cosine

### Routing Falls Back to Keywords

**Cause**: ChromaDB connection failed

**Fix**:
1. Check Vercel logs: `vercel logs`
2. Verify environment variables are set: `vercel env ls`
3. Test connection locally first
4. Check ChromaDB service status

## Verification Checklist

Before deploying to Vercel:

- [ ] Signed up for Chroma Cloud or deployed self-hosted server
- [ ] Got CHROMA_HOST and CHROMA_API_KEY
- [ ] Tested connection locally
- [ ] Saw "Connecting to hosted instance" in logs
- [ ] Routing returned `semantic_embeddings_chromadb` method
- [ ] Added environment variables to Vercel
- [ ] Deployed to Vercel
- [ ] Checked Vercel logs for ChromaDB connection
- [ ] Tested routing in production

## Support

- **Chroma Documentation**: https://docs.trychroma.com/
- **Chroma Discord**: https://discord.gg/MMeYNTmh3x
- **GitHub Issues**: https://github.com/chroma-core/chroma

## Summary

✅ **Hosted ChromaDB enables real semantic routing on Vercel**  
✅ **Automatic fallback ensures the app always works**  
✅ **Local development still uses fast local ChromaDB**  
✅ **One line change: Set CHROMA_HOST and CHROMA_API_KEY in Vercel**
