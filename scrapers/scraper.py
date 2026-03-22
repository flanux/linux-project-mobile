#!/usr/bin/env python3
import httpx
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def scrape_lfx_mentorship():
    """Scrape LFX Mentorship page directly"""
    print("Scraping LFX Mentorship...")
    internships = []
    
    # Fallback data in case scraping fails
    fallback = [
        {
            'title': 'Linux Kernel Mentorship Program',
            'organization': 'Linux Foundation',
            'description': 'Participate in hands-on kernel development under experienced mentors. Applications open seasonally.',
            'link': 'https://mentorship.lfx.linuxfoundation.org/projects',
            'type': 'mentorship'
        },
        {
            'title': 'CNCF Mentoring',
            'organization': 'Cloud Native Computing Foundation',
            'description': 'Work on cloud-native projects like Kubernetes, Prometheus, and more. Multiple terms per year.',
            'link': 'https://mentorship.lfx.linuxfoundation.org/projects',
            'type': 'mentorship'
        }
    ]
    
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://mentorship.lfx.linuxfoundation.org/projects')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Try to find project cards
                cards = soup.find_all(['div', 'article'], class_=['project', 'card'])
                for card in cards[:10]:
                    title_elem = card.find(['h1', 'h2', 'h3', 'h4'])
                    if title_elem:
                        internships.append({
                            'title': title_elem.get_text(strip=True),
                            'organization': 'Linux Foundation',
                            'description': 'Check the LFX platform for details and application deadlines.',
                            'link': 'https://mentorship.lfx.linuxfoundation.org/projects',
                            'type': 'mentorship'
                        })
    except Exception as e:
        print(f"Error scraping LFX: {e}")
    
    return internships if internships else fallback


def scrape_linux_foundation_jobs():
    """Scrape Linux Foundation careers page"""
    print("Scraping Linux Foundation Jobs...")
    jobs = []
    
    fallback = [
        {
            'title': 'View Open Positions',
            'company': 'Linux Foundation',
            'location': 'Remote/Global',
            'link': 'https://www.linuxfoundation.org/about/careers'
        }
    ]
    
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://www.linuxfoundation.org/about/careers')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Look for job listings
                job_links = soup.find_all('a', href=True)
                for link in job_links:
                    text = link.get_text(strip=True)
                    if len(text) > 10 and ('engineer' in text.lower() or 'developer' in text.lower() or 'manager' in text.lower()):
                        jobs.append({
                            'title': text,
                            'company': 'Linux Foundation',
                            'location': 'Remote',
                            'link': link['href'] if link['href'].startswith('http') else 'https://www.linuxfoundation.org' + link['href']
                        })
                        if len(jobs) >= 10:
                            break
    except Exception as e:
        print(f"Error scraping LF jobs: {e}")
    
    return jobs if jobs else fallback


def scrape_lwn_news():
    """Scrape LWN.net front page"""
    print("Scraping LWN News...")
    news = []
    
    fallback = [
        {
            'title': 'Visit LWN.net for Latest Linux News',
            'source': 'LWN.net',
            'link': 'https://lwn.net/',
            'date': datetime.now().strftime('%Y-%m-%d')
        }
    ]
    
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://lwn.net/')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # LWN headlines
                headlines = soup.select('div.Headline a, div.HeadlineText a, p.Headline a')
                for a in headlines[:15]:
                    title = a.get_text(strip=True)
                    href = a.get('href', '')
                    if title and href:
                        full_link = href if href.startswith('http') else 'https://lwn.net' + href
                        news.append({
                            'title': title,
                            'source': 'LWN.net',
                            'link': full_link,
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
    except Exception as e:
        print(f"Error scraping LWN: {e}")
    
    return news if news else fallback


def scrape_linux_projects():
    """Get Linux Foundation projects"""
    print("Scraping Linux Foundation Projects...")
    
    # Use known projects as fallback/primary data
    projects = [
        {
            'name': 'Linux Kernel',
            'description': 'The core of the Linux operating system. Contributions welcome via mailing lists and patch submissions.',
            'link': 'https://www.kernel.org/',
            'category': 'Core'
        },
        {
            'name': 'Kubernetes',
            'description': 'Container orchestration platform. Part of CNCF, actively seeking contributors.',
            'link': 'https://kubernetes.io/',
            'category': 'CNCF'
        },
        {
            'name': 'Prometheus',
            'description': 'Monitoring and alerting toolkit. CNCF graduated project.',
            'link': 'https://prometheus.io/',
            'category': 'CNCF'
        },
        {
            'name': 'Node.js',
            'description': 'JavaScript runtime built on Chrome V8 engine. Part of OpenJS Foundation.',
            'link': 'https://nodejs.org/',
            'category': 'OpenJS'
        },
        {
            'name': 'Hyperledger Fabric',
            'description': 'Enterprise blockchain framework. Part of Hyperledger.',
            'link': 'https://www.hyperledger.org/projects/fabric',
            'category': 'Hyperledger'
        }
    ]
    
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://www.linuxfoundation.org/projects')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                cards = soup.find_all(['article', 'div'], class_=['project', 'card'])
                
                additional = []
                for card in cards[:5]:
                    title_elem = card.find(['h2', 'h3', 'h4'])
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        desc_elem = card.find('p')
                        additional.append({
                            'name': title,
                            'description': desc_elem.get_text(strip=True)[:150] if desc_elem else '',
                            'link': 'https://www.linuxfoundation.org/projects',
                            'category': 'Linux Foundation'
                        })
                
                if additional:
                    projects.extend(additional)
    except Exception as e:
        print(f"Error scraping projects: {e}")
    
    return projects


def scrape_kernel_newbies():
    """Scrape Kernel Newbies resources"""
    print("Scraping Kernel Newbies...")
    
    fallback = [
        {
            'title': 'Kernel Newbies Main Page',
            'type': 'Learning',
            'link': 'https://kernelnewbies.org/',
            'source': 'Kernel Newbies'
        },
        {
            'title': 'First Kernel Patch Tutorial',
            'type': 'Tutorial',
            'link': 'https://kernelnewbies.org/FirstKernelPatch',
            'source': 'Kernel Newbies'
        },
        {
            'title': 'Kernel Development Guide',
            'type': 'Guide',
            'link': 'https://kernelnewbies.org/Documents',
            'source': 'Kernel Newbies'
        }
    ]
    
    resources = []
    
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://kernelnewbies.org/Documents')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                links = soup.find_all('a', href=True)
                for a in links[:20]:
                    href = a['href']
                    text = a.get_text(strip=True)
                    
                    if not text or len(text) < 4:
                        continue
                    if any(skip in href for skip in ['action=', 'mailto:', 'RecentChanges']):
                        continue
                    
                    full_link = href if href.startswith('http') else 'https://kernelnewbies.org' + href
                    resources.append({
                        'title': text,
                        'type': 'Tutorial',
                        'link': full_link,
                        'source': 'Kernel Newbies'
                    })
                    
                    if len(resources) >= 15:
                        break
    except Exception as e:
        print(f"Error scraping Kernel Newbies: {e}")
    
    return resources if resources else fallback


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
