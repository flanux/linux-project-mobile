#!/usr/bin/env python3
import httpx
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def scrape_lfx_mentorship():
    """Fetch LFX Mentorship programs via public REST API (avoids SPA rendering issues)"""
    print("Scraping LFX Mentorship...")
    internships = []
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            # LFX exposes a public REST API — no JS rendering needed
            response = client.get(
                'https://api2.mentorship.lfx.linuxfoundation.org/v2/project',
                params={'status': 'active', '$limit': 20}
            )
            response.raise_for_status()
            projects = response.json().get('Data', [])
            for p in projects:
                slug = p.get('Slug', '')
                internships.append({
                    'title': p.get('Name', 'Mentorship Opportunity'),
                    'organization': p.get('Industry', 'Linux Foundation'),
                    'description': (p.get('Description', '') or '')[:200],
                    'link': f'https://mentorship.lfx.linuxfoundation.org/project/{slug}' if slug else 'https://mentorship.lfx.linuxfoundation.org/projects',
                    'type': 'mentorship'
                })
    except Exception as e:
        print(f"Error scraping LFX: {e}")

    return internships


def scrape_linux_foundation_jobs():
    """Fetch Linux Foundation jobs via Greenhouse JSON API"""
    print("Scraping Linux Foundation Jobs...")
    jobs = []
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            # LF uses Greenhouse; this endpoint returns all open positions as JSON
            response = client.get('https://boards-api.greenhouse.io/v1/boards/linuxfoundation/jobs?content=true')
            response.raise_for_status()
            postings = response.json().get('jobs', [])
            for job in postings[:15]:
                location = job.get('location', {}).get('name', 'Remote')
                jobs.append({
                    'title': job.get('title', 'Position Available'),
                    'company': 'Linux Foundation',
                    'location': location,
                    'link': job.get('absolute_url', 'https://www.linuxfoundation.org/about/careers')
                })
    except Exception as e:
        print(f"Error scraping LF jobs: {e}")

    return jobs


def scrape_lwn_news():
    """Scrape LWN.net front page headlines"""
    print("Scraping LWN News...")
    news = []
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://lwn.net/')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Front page: each story headline is in div.Headline > a
            headlines = soup.select('div.Headline a')
            for a in headlines[:15]:
                title = a.get_text(strip=True)
                href = a.get('href', '')
                if not title or not href:
                    continue
                full_link = href if href.startswith('http') else 'https://lwn.net' + href
                news.append({
                    'title': title,
                    'source': 'LWN.net',
                    'link': full_link,
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
    except Exception as e:
        print(f"Error scraping LWN: {e}")

    return news


def scrape_linux_projects():
    """Fetch Linux Foundation projects from their projects page"""
    print("Scraping Linux Foundation Projects...")
    projects = []
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://www.linuxfoundation.org/projects')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Target: <article> or section/div cards with a heading and a link
            cards = soup.select('article, section.project, div.project-card')
            for card in cards[:20]:
                title_elem = card.find(['h2', 'h3', 'h4'])
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                desc_elem = card.find('p')
                description = desc_elem.get_text(strip=True)[:150] if desc_elem else ''
                link_elem = card.find('a', href=True)
                link = link_elem['href'] if link_elem else ''
                if link and not link.startswith('http'):
                    link = 'https://www.linuxfoundation.org' + link
                if title:
                    projects.append({
                        'name': title,
                        'description': description,
                        'link': link,
                        'category': 'Linux Foundation'
                    })

            # If the page is a SPA shell with no articles, try __NEXT_DATA__
            if not projects:
                next_data_tag = soup.find('script', id='__NEXT_DATA__')
                if next_data_tag:
                    next_data = json.loads(next_data_tag.string or '{}')
                    items = (
                        next_data.get('props', {})
                        .get('pageProps', {})
                        .get('projects', [])
                    )
                    for item in items[:20]:
                        projects.append({
                            'name': item.get('name', ''),
                            'description': (item.get('description', '') or '')[:150],
                            'link': item.get('url', 'https://www.linuxfoundation.org/projects'),
                            'category': item.get('category', 'Linux Foundation')
                        })

    except Exception as e:
        print(f"Error scraping projects: {e}")

    return projects


def scrape_kernel_newbies():
    """Scrape Kernel Newbies Documents page for real tutorial links"""
    print("Scraping Kernel Newbies...")
    resources = []
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://kernelnewbies.org/Documents')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Documents page is a MoinMoin wiki; content links are inside
            # div#content li > a, pointing to /KernelNewbies paths
            content_div = soup.find('div', id='content') or soup
            for a in content_div.select('li > a[href]'):
                href = a['href']
                text = a.get_text(strip=True)
                # Skip empty, nav, edit, and external noise links
                if not text or len(text) < 4:
                    continue
                if any(skip in href for skip in ['action=', 'mailto:', '#', 'RecentChanges', 'UserPreferences']):
                    continue
                full_link = href if href.startswith('http') else 'https://kernelnewbies.org' + href
                resources.append({
                    'title': text,
                    'type': 'Tutorial',
                    'link': full_link,
                    'source': 'Kernel Newbies'
                })
                if len(resources) >= 20:
                    break

    except Exception as e:
        print(f"Error scraping Kernel Newbies: {e}")

    return resources


def main():
    print("Starting Linux Project data scraping...")
    print("=" * 50)

    os.makedirs('scrapers/output', exist_ok=True)

    data = {
        'internships': scrape_lfx_mentorship(),
        'jobs': scrape_linux_foundation_jobs(),
        'news': scrape_lwn_news(),
        'projects': scrape_linux_projects(),
        'learning': scrape_kernel_newbies(),
        'last_updated': datetime.now().isoformat(),
        'version': '1.0'
    }

    # Save to JSON
    output_file = 'scrapers/output/data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("=" * 50)
    print("Scraping completed!")
    print(f"Internships: {len(data['internships'])}")
    print(f"Jobs: {len(data['jobs'])}")
    print(f"News: {len(data['news'])}")
    print(f"Projects: {len(data['projects'])}")
    print(f"Learning Resources: {len(data['learning'])}")
    print(f"Data saved to: {output_file}")


if __name__ == '__main__':
    main()
