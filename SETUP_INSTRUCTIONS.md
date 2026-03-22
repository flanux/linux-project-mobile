# Setup Instructions

## Quick Start (Recommended - Zero Local Build)

1. Fork this repository on GitHub
2. Clone your fork locally
3. Edit `app/src/main/java/com/linuxproject/MainActivity.kt` line 37:
   - Replace `YOUR_USERNAME` with your GitHub username
4. Commit and push:
   ```bash
   git add .
   git commit -m "Update GitHub username"
   git push origin main
   ```
5. Wait 3-5 minutes for GitHub Actions to build
6. Download APK from Releases section
7. Install on your Android phone

## Important: Update GitHub Username

Before pushing, you MUST update the data URL in MainActivity.kt:

```kotlin
// Find this line (around line 37):
val url = "https://raw.githubusercontent.com/YOUR_USERNAME/linux-project-mobile/main/scrapers/output/data.json"

// Change YOUR_USERNAME to your actual GitHub username:
val url = "https://raw.githubusercontent.com/yourusername/linux-project-mobile/main/scrapers/output/data.json"
```

## First Time Setup Checklist

- [ ] Fork repository
- [ ] Clone to local machine
- [ ] Update GitHub username in MainActivity.kt
- [ ] Commit and push changes
- [ ] Wait for GitHub Actions to complete
- [ ] Download APK from Releases
- [ ] Enable "Install from unknown sources" on phone
- [ ] Install APK

## Workflows Explained

### Daily Scraper (runs daily at midnight UTC)
- Scrapes Linux Foundation data
- Saves to `scrapers/output/data.json`
- Commits to repository automatically

### Build APK (runs on every push)
- Builds debug APK
- Creates GitHub Release
- Uploads APK for download

## Manual Workflow Triggers

### Run Scraper Manually
1. Go to your repo on GitHub
2. Click "Actions" tab
3. Select "Daily Scraper"
4. Click "Run workflow"
5. Select "main" branch
6. Click green "Run workflow" button

### Build APK Manually
1. Go to "Actions" tab
2. Select "Build APK"
3. Click "Run workflow"
4. Wait for completion
5. Download from Releases

## Troubleshooting

### Build fails with "SDK not found"
- This is normal - GitHub Actions handles SDK installation
- Just push again if first build fails

### No data in app
- Check if scraper ran: look for `scrapers/output/data.json` in repo
- Verify you updated the GitHub username in MainActivity.kt
- Pull to refresh in the app

### APK not in Releases
- Check Actions tab for build status
- Make sure workflows are enabled
- Check if there are any error messages

### App crashes on launch
- Make sure you're running Android 7.0 or higher
- Check if you have internet connection
- Verify the GitHub URL is correct in MainActivity.kt

## Optional: Local Development (Advanced)

If you want to build locally (NOT REQUIRED):

1. Install Android Studio
2. Install JDK 17
3. Open project in Android Studio
4. Wait for Gradle sync
5. Run on emulator or device

Note: Local building is optional. The recommended workflow is git push and download APK.
