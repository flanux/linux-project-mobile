# Linux Project Mobile

A native Android app that aggregates Linux Foundation internships, jobs, news, projects, and learning resources. All scraping and APK building happens automatically on GitHub Actions - zero local building required.

## Features

- Daily automated scraping of Linux Foundation resources
- Internships and mentorship programs from LFX platform
- Job listings from Linux Foundation and partners
- Latest Linux news from LWN.net
- Linux Foundation projects catalog
- Learning resources from Kernel Newbies
- Pull-to-refresh for latest data
- Clean, minimal UI with easy navigation

## Architecture

```
GitHub Actions (Daily Scraper)
    |
    v
scrapers/output/data.json (committed to repo)
    |
    v
Android App (fetches JSON from GitHub raw URL)
    |
    v
Display in RecyclerView
```

## Setup Instructions

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/linux-project-mobile.git
cd linux-project-mobile
```

### 2. Update GitHub URL

Edit `app/src/main/java/com/linuxproject/MainActivity.kt` and replace:

```kotlin
val url = "https://raw.githubusercontent.com/YOUR_USERNAME/linux-project-mobile/main/scrapers/output/data.json"
```

With your actual GitHub username.

### 3. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 4. Enable GitHub Actions

- Go to your repository on GitHub
- Click "Actions" tab
- Enable workflows if prompted
- Both workflows (daily-scraper.yml and build-apk.yml) will run automatically

### 5. Download APK

- Wait 3-5 minutes for the build to complete
- Go to "Releases" section in your repository
- Download the latest APK file
- Install on your Android device (enable "Install from unknown sources")

## Development Workflow

All development happens through git - no local Android Studio or Gradle required:

```bash
# Edit code locally
nano app/src/main/java/com/linuxproject/MainActivity.kt

# Commit and push
git add .
git commit -m "Updated UI layout"
git push

# GitHub Actions automatically:
# - Builds APK
# - Creates new release
# - Uploads APK

# Download APK from Releases and install
```

## Scraper Details

The scraper runs daily at midnight UTC and fetches:

- LFX Mentorship programs
- Linux Foundation job postings
- LWN.net latest news
- Linux Foundation projects
- Kernel Newbies learning resources

Data is saved to `scrapers/output/data.json` and committed automatically.

## Manual Scraper Run

Trigger manually via GitHub Actions:

1. Go to "Actions" tab
2. Select "Daily Scraper" workflow
3. Click "Run workflow"
4. Data will update in ~2 minutes

## Customization

### Add More Scrapers

Edit `scrapers/scraper.py` to add new sources:

```python
def scrape_new_source():
    # Your scraping logic
    return data

# Add to main()
data['new_category'] = scrape_new_source()
```

### Modify UI

Edit layout files in `app/src/main/res/layout/`:

- `activity_main.xml` - Main screen
- `item_internship.xml` - Internship cards
- `item_job.xml` - Job cards
- `item_news.xml` - News cards
- `item_project.xml` - Project cards
- `item_learning.xml` - Learning resource cards

Push changes to trigger automatic rebuild.

## Troubleshooting

### Build Fails

Check GitHub Actions logs:
1. Go to "Actions" tab
2. Click on failed workflow
3. Review error logs
4. Fix issues and push again

### No Data in App

1. Check if scraper ran successfully
2. Verify `scrapers/output/data.json` exists in repo
3. Confirm GitHub URL in MainActivity.kt is correct
4. Pull-to-refresh in the app

### App Crashes

1. Check Logcat if using USB debugging
2. Verify JSON structure matches expected format
3. Review MainActivity.kt parsing logic

## Requirements

- Android 7.0 (API 24) or higher
- Internet connection
- GitHub account (free tier includes Actions)

## Technologies

- Kotlin for Android app
- Python 3.11 for web scraping
- OkHttp for networking
- RecyclerView for lists
- SwipeRefreshLayout for pull-to-refresh
- GitHub Actions for CI/CD
- BeautifulSoup4 for HTML parsing

## License

Open source - use freely for learning and development.

## Contributing

Contributions welcome:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Push and create Pull Request

## Data Sources

- Linux Foundation Mentorship: https://mentorship.lfx.linuxfoundation.org
- Linux Foundation Jobs: https://www.linuxfoundation.org/about/careers
- LWN News: https://lwn.net
- Linux Foundation Projects: https://www.linuxfoundation.org/projects
- Kernel Newbies: https://kernelnewbies.org

All data is publicly available and scraped respectfully with appropriate delays.
