# Render Deployment Guide

## Step-by-Step Instructions

### 1. Sign Up / Login
- Go to https://render.com
- Click "Get Started for Free"
- Sign up with your **GitHub account** (recommended)

### 2. Create New Web Service
- Click **"New +"** button (top right)
- Select **"Web Service"**
- Click **"Connect account"** if not already connected to GitHub
- Select your repository: **`WesleyJohnson0423/InterrogatableAI`**

### 3. Configure Service Settings

**Basic Settings:**
- **Name**: `interrogatable-ai` (or any name you prefer)
- **Region**: Choose closest to you (e.g., `Oregon (US West)` or `Singapore (Asia Pacific)`)
- **Branch**: `master`
- **Root Directory**: (leave empty)

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

**Advanced Settings (Optional):**
- **Auto-Deploy**: `Yes` (automatically deploy on git push)
- **Health Check Path**: `/` (optional)

### 4. Add Environment Variables

Scroll down to **"Environment Variables"** section:

Click **"Add Environment Variable"** and add:

1. **OPENAI_API_KEY**
   - Key: `OPENAI_API_KEY`
   - Value: `your_openai_api_key_here` (use your actual API key)

2. **LLM_BASE_URL** (optional, has default)
   - Key: `LLM_BASE_URL`
   - Value: `https://api.openai.com/v1`

### 5. Deploy

- Click **"Create Web Service"** button (bottom)
- Render will start building your application
- **First build may take 15-20 minutes** (installing dependencies)
- You can watch the build logs in real-time

### 6. Access Your App

- Once deployment is complete, Render will provide a URL like:
  `https://interrogatable-ai.onrender.com`
- Click the URL to access your application
- **Note**: Free tier apps may take 30-60 seconds to "wake up" if idle

## Important Notes

### First Run
- The app will automatically build the knowledge base on first access
- This may take 2-5 minutes depending on number of PDFs
- Users will see "Initializing system..." message

### Free Tier Limitations
- **Sleep after inactivity**: Free tier apps sleep after 15 minutes of inactivity
- **Wake time**: Takes 30-60 seconds to wake up
- **Build time**: May be slower on free tier
- **Monthly hours**: 750 free hours/month

### Troubleshooting

**Build fails:**
- Check build logs for errors
- Ensure all dependencies in requirements.txt are correct
- Verify Python version compatibility

**App crashes:**
- Check runtime logs
- Verify environment variables are set correctly
- Ensure OpenAI API key is valid

**Slow response:**
- First query builds knowledge base (takes time)
- Free tier has resource limits
- Consider upgrading for better performance

**Memory issues:**
- If build fails due to memory, consider reducing PDF count
- Or upgrade to paid plan ($7/month)

## Alternative: Using render.yaml (Optional)

If you prefer configuration file approach:

1. The `render.yaml` file is already in the repository
2. In Render dashboard, you can import from `render.yaml`
3. Or manually configure as described above

## Cost

- **Free Tier**: 750 hours/month (enough for demo)
- **Starter Plan**: $7/month (no sleep, better performance)
- **OpenAI API**: Pay per use (very affordable)

## Next Steps After Deployment

1. Test the application with a simple question
2. Share the URL with your teacher
3. Monitor logs if any issues occur

