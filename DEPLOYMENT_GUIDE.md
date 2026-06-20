# 🚀 MyNetShield: Simple Deployment Guide

Follow these 3 simple steps to get your app running and accessible from anywhere.

## Step 1: Start the App (The "Engine")
1. Open your project folder: `c:\Users\DELL\Documents\MyNetShield`
2. Look for the file named **`start_netshield.bat`**.
3. **Right-click** it and select **"Run as administrator"**.
   - *This starts your app on your computer. Keep this window open!*

## Step 2: Open it Locally
- Open your browser and go to: `http://localhost:5173`

- You should see your MyNetShield dashboard.

## Step 3: Put it "On the Web" (Access from anywhere)
To see your app from your phone or another computer anywhere in the world:
1. Download **ngrok** from [ngrok.com](https://ngrok.com/download).
2. Open a new terminal (unrelated to the one above).
3. Type this command and press Enter:
   ```bash
   ngrok http 5173

   ```
4. ngrok will give you a link that looks like `https://a1b2-c3d4.ngrok-free.app`.
   - **This is your public link!** Use it to access your app from the world.

---
> [!IMPORTANT]
> **Don't close the windows!** If you close the terminal running the app or ngrok, the website will stop working.
