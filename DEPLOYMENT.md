# Deployment Guide

## Recommended Platform: Railway

Railway is recommended for its simplicity and free tier. Alternative: Render.

## Prerequisites

1. GitHub account (code should be pushed to GitHub)
2. Railway account (sign up at https://railway.app)
3. OpenAI API key

## Deployment Steps

### Option 1: Railway (Recommended)

1. **Sign up/Login to Railway**
   - Go to https://railway.app
   - Sign up with GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `WesleyJohnson0423/InterrogatableAI`

3. **Configure Environment Variables**
   - Go to project settings → Variables
   - Add the following:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     LLM_BASE_URL=https://api.openai.com/v1
     PORT=8501
     ```

4. **Deploy**
   - Railway will automatically detect `Procfile` and start deployment
   - Wait for build to complete (may take 10-15 minutes due to large dependencies)
   - Once deployed, Railway will provide a public URL

5. **Access Your App**
   - Click on the generated URL
   - Your Streamlit app should be accessible

### Option 2: Render

1. **Sign up/Login to Render**
   - Go to https://render.com
   - Sign up with GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select repository: `WesleyJohnson0423/InterrogatableAI`

3. **Configure Settings**
   - **Name**: interrogatable-ai (or any name)
   - **Region**: Choose closest region
   - **Branch**: master
   - **Root Directory**: (leave empty)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

4. **Add Environment Variables**
   - Scroll down to "Environment Variables"
   - Add:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     LLM_BASE_URL=https://api.openai.com/v1
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (10-15 minutes)
   - Access via provided URL

## Important Notes

### PDF Files Handling

**Option A: Include PDFs in Git (for small number of PDFs)**
- PDFs are already in the repository
- They will be deployed automatically
- Note: Large number of PDFs may slow down deployment

**Option B: Use Git LFS (for many/large PDFs)**
```bash
git lfs install
git lfs track "*.pdf"
git add .gitattributes
git add *.pdf
git commit -m "Add PDFs with LFS"
git push
```

**Option C: Upload PDFs after deployment**
- Use file upload feature in Streamlit (requires code modification)

### First Run

- The app will automatically build the knowledge base on first run
- This may take several minutes depending on number of PDFs
- Users will see "Initializing system..." message

### Troubleshooting

1. **Build fails due to memory**
   - Railway/Render free tier has memory limits
   - Consider reducing number of PDFs or using smaller embedding model

2. **App crashes on startup**
   - Check logs in Railway/Render dashboard
   - Verify environment variables are set correctly
   - Ensure OpenAI API key is valid

3. **Slow response**
   - First query may be slow (building knowledge base)
   - Consider pre-building knowledge base locally and committing vector_db

4. **Port issues**
   - Ensure `Procfile` uses `$PORT` environment variable
   - Railway/Render will set this automatically

## Cost Considerations

- **Railway**: $5/month free credit, then pay-as-you-go
- **Render**: Free tier available, but may sleep after inactivity
- **OpenAI API**: Pay per use (very affordable for small projects)

## Alternative: Streamlit Cloud (Simplest)

If you want the simplest deployment:

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Add secrets (environment variables):
   ```
   OPENAI_API_KEY=your_key_here
   ```
7. Deploy!

**Note**: Streamlit Cloud has limitations on file size and may not work well with many PDFs.

