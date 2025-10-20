# Deployment Guide - Streamlit Community Cloud

## Step-by-Step Deployment Instructions

### Step 1: Push Your Code to GitHub

1. **Create a new GitHub repository:**
   - Go to https://github.com/new
   - Name it something like `elevator-inspection-analyzer`
   - Make it **Public** (required for Streamlit Community Cloud free tier)
   - DO NOT initialize with README (we already have one)

2. **Initialize Git in your project folder:**
   ```bash
   cd "C:\Users\Amr\Desktop\defects classification"
   git init
   git add .
   git commit -m "Initial commit: Elevator Inspection Analyzer"
   ```

3. **Connect to your GitHub repository:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/elevator-inspection-analyzer.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Community Cloud

1. **Sign up/Login to Streamlit Community Cloud:**
   - Go to https://share.streamlit.io/
   - Click "Sign in" and use your GitHub account

2. **Create a new app:**
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/elevator-inspection-analyzer`
   - Branch: `main`
   - Main file path: `streamlit_analyzer.py`
   - Click "Deploy!"

3. **Configure Secrets (IMPORTANT):**
   - After deployment starts, click on "Advanced settings" or "⚙️" icon
   - Go to "Secrets" section
   - Add your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "your-actual-openai-api-key-here"
   ```
   - Click "Save"

4. **Wait for deployment:**
   - Streamlit will install dependencies from `requirements.txt`
   - This may take 2-5 minutes
   - Once done, you'll get a public URL like: `https://your-app-name.streamlit.app`

### Step 3: Share Your App

Your app will be available at a public URL that looks like:
```
https://elevator-inspection-analyzer.streamlit.app
```

You can share this URL with anyone! They can:
- Upload PDF inspection reports
- Get AI-powered defect classifications
- Export results to Excel

## Important Notes

### API Key Security
- ✅ The API key is stored securely in Streamlit Secrets
- ✅ It's never exposed in the code or to users
- ✅ Each user will NOT need their own API key (they'll use yours)

### Costs
- Streamlit hosting is **FREE**
- You only pay for OpenAI API usage when people use your app
- Monitor your usage at: https://platform.openai.com/usage
- Set spending limits at: https://platform.openai.com/account/billing/limits

### Usage Limits
- Streamlit Community Cloud free tier has:
  - Unlimited public apps
  - 1GB of resources per app
  - Always-on apps (auto-wake on visit)

## Troubleshooting

### If deployment fails:
1. Check the deployment logs in Streamlit Cloud
2. Verify `requirements.txt` has all dependencies
3. Make sure the API key is correctly added to Secrets

### If the app works but analysis fails:
1. Check your OpenAI API key is valid
2. Verify you have API credits: https://platform.openai.com/account/billing
3. Make sure the API key has GPT-4 access

## Alternative: Share Without GitHub (Local Network Only)

If you want to share ONLY with people on your local network:

1. Run Streamlit with the network URL:
   ```bash
   streamlit run streamlit_analyzer.py --server.address 0.0.0.0
   ```

2. Share the Network URL shown (e.g., `http://192.168.1.100:8501`)

3. People on the same network can access it

⚠️ **Note:** This only works while your computer is running and on the same network!

## Recommended: Deploy on Streamlit Cloud

For permanent, public access, deploying on Streamlit Community Cloud is the best option.
