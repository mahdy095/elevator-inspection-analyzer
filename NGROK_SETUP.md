# Public URL Setup with Ngrok

This guide shows you how to create a public URL that anyone can use to access your Streamlit app, even if your PC is on.

## What is Ngrok?

Ngrok creates a secure tunnel from a public URL to your local computer. When someone visits the public URL, it forwards the request to your local Streamlit app.

## Setup Instructions

### Step 1: Install Ngrok

1. **Download Ngrok:**
   - Go to: https://ngrok.com/download
   - Download the Windows version
   - Extract the `ngrok.exe` file to a folder (e.g., `C:\ngrok\`)

2. **Add to PATH (optional but recommended):**
   - Right-click "This PC" → Properties → Advanced System Settings
   - Click "Environment Variables"
   - Under "System Variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\ngrok\` (or wherever you extracted it)
   - Click OK on all windows

### Step 2: Sign Up for Ngrok (Free)

1. **Create Account:**
   - Go to: https://dashboard.ngrok.com/signup
   - Sign up with Google/GitHub or email (it's free!)

2. **Get Your Auth Token:**
   - After signup, you'll see your auth token on: https://dashboard.ngrok.com/get-started/your-authtoken
   - Copy the command shown (looks like: `ngrok config add-authtoken YOUR_TOKEN`)

3. **Configure Ngrok:**
   - Open Command Prompt or PowerShell
   - Paste and run the auth token command:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

### Step 3: Start Your Streamlit App

1. **Open Command Prompt/PowerShell**
2. **Navigate to your project:**
   ```bash
   cd "C:\Users\Amr\Desktop\defects classification"
   ```

3. **Start Streamlit:**
   ```bash
   streamlit run streamlit_analyzer.py
   ```

   Keep this window open!

### Step 4: Start Ngrok Tunnel

1. **Open a NEW Command Prompt/PowerShell window**
2. **Start the tunnel:**
   ```bash
   ngrok http 8501
   ```

3. **Get your public URL:**
   - Ngrok will show something like:
   ```
   Forwarding    https://abc123xyz.ngrok-free.app -> http://localhost:8501
   ```
   - The URL `https://abc123xyz.ngrok-free.app` is your public URL!

4. **Share this URL with anyone:**
   - Send them: `https://abc123xyz.ngrok-free.app`
   - They can access it from anywhere in the world!
   - They'll be using YOUR OpenAI API key (that you configured)

## Important Notes

### ✅ Advantages:
- Works immediately - no GitHub needed
- Free tier available
- Anyone worldwide can access
- HTTPS encryption included
- No router configuration needed

### ⚠️ Things to Know:

1. **Your PC must stay on:**
   - The URL only works while your PC is on and running both Streamlit and Ngrok
   - If you close either program, the URL stops working

2. **Free tier limits:**
   - URL changes each time you restart ngrok (unless you pay for a static domain)
   - 40 connections/minute limit
   - Session time limit (2 hours on free tier - will auto-reconnect)

3. **API Costs:**
   - Everyone using the app uses YOUR OpenAI API key
   - Monitor usage at: https://platform.openai.com/usage
   - Set spending limits: https://platform.openai.com/account/billing/limits

4. **URL Warning Page:**
   - First-time visitors see an ngrok warning page
   - They just click "Visit Site" to continue
   - This is normal for free ngrok URLs

## Quick Start Commands

**Terminal 1 - Streamlit:**
```bash
cd "C:\Users\Amr\Desktop\defects classification"
streamlit run streamlit_analyzer.py
```

**Terminal 2 - Ngrok:**
```bash
ngrok http 8501
```

Then share the `https://....ngrok-free.app` URL with anyone!

## Upgrading to Paid Ngrok (Optional)

If you want:
- A permanent URL that doesn't change (custom domain)
- No connection limits
- No warning page for visitors

Ngrok paid plans start at $8/month: https://ngrok.com/pricing

## Alternative: Streamlit Community Cloud (Recommended for Production)

If you want a permanent solution that doesn't require your PC to be on:
1. Follow the `DEPLOYMENT.md` guide
2. Deploy to Streamlit Community Cloud (free!)
3. Get a permanent URL like `https://your-app.streamlit.app`
4. No need to keep your PC on

## Troubleshooting

### Ngrok shows "command not found":
- Make sure you added ngrok to PATH
- Or use full path: `C:\ngrok\ngrok.exe http 8501`

### URL doesn't work:
- Make sure both Streamlit AND ngrok are running
- Check the port is 8501 in both
- Verify your firewall isn't blocking it

### People can't access:
- Make sure you shared the HTTPS URL (https://..., not http://localhost...)
- The URL changes each time you restart ngrok (free tier)

## Pro Tip: Keep It Running

To keep your app running 24/7 without your PC:
→ Deploy to Streamlit Community Cloud (see DEPLOYMENT.md)

To keep it running on your PC:
→ Prevent your PC from sleeping (Power Settings → Never sleep)
