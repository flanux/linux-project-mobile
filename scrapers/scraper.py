#!/usr/bin/env python3
import httpx
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

def scrape_lfx_mentorship():
    """Scrape Linux Foundation Mentorship programs"""
    print("Scraping LFX Mentorship...")
    
    internships = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        with httpx.Client(headers=headers, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://mentorship.lfx.linuxfoundation.org/projects')
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Generic scraping for project cards
            project_cards = soup.find_all('div', class_='project-card')
            
            for card in project_cards[:10]:  # Limit to 10
                try:
                    title_elem = card.find(['h3', 'h4', 'h5'])
                    title = title_elem.text.strip() if title_elem else 'Mentorship Opportunity'
                    
                    desc_elem = card.find('p')
                    description = desc_elem.text.strip() if desc_elem else 'Check website for details'
                    
                    link_elem = card.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = 'https://mentorship.lfx.linuxfoundation.org' + link
                    
                    internships.append({
                        'title': title,
                        'organization': 'Linux Foundation',
                        'description': description[:200],
                        'link': link,
                        'type': 'mentorship'
                    })
                except Exception as e:
                    continue
            
            # Fallback data if scraping fails
            if len(internships) == 0:
                internships.append({
                    'title': 'Linux Kernel Mentorship Program',
                    'organization': 'Linux Foundation',
                    'description': 'Hands-on mentorship for Linux kernel development. Check the LFX platform for current opportunities.',
                    'link': 'https://mentorship.lfx.linuxfoundation.org/projects',
                    'type': 'mentorship'
                })
    
    except Exception as e:
        print(f"Error scraping LFX: {e}")
        internships.append({
            'title': 'Visit LFX Mentorship Platform',
            'organization': 'Linux Foundation',
            'description': 'Visit the platform to see current mentorship opportunities in Linux kernel, CNCF projects, and more.',
            'link': 'https://mentorship.lfx.linuxfoundation.org/',
            'type': 'mentorship'
        })
    
    return internships


def scrape_linux_foundation_jobs():
    """Scrape Linux Foundation careers page"""
    print("Scraping Linux Foundation Jobs...")
    
    jobs = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        
        with httpx.Client(headers=headers, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://www.linuxfoundation.org/about/careers')
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_listings = soup.find_all(['div', 'li'], class_=['job-listing', 'job-item', 'career-item'])
            
            for job in job_listings[:10]:
                try:
                    title_elem = job.find(['h3', 'h4', 'a'])
                    title = title_elem.text.strip() if title_elem else 'Position Available'
                    
                    link_elem = job.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = 'https://www.linuxfoundation.org' + link
                    
                    jobs.append({
                        'title': title,
                        'company': 'Linux Foundation',
                        'location': 'Remote',
                        'link': link
                    })
                except Exception as e:
                    continue
            
            if len(jobs) == 0:
                jobs.append({
                    'title': 'Check Linux Foundation Careers',
                    'company': 'Linux Foundation',
                    'location': 'Various',
                    'link': 'https://www.linuxfoundation.org/about/careers'
                })
    
    except Exception as e:
        print(f"Error scraping LF jobs: {e}")
        jobs.append({
            'title': 'Visit Careers Page',
            'company': 'Linux Foundation',
            'location': 'Remote/Hybrid',
            'link': 'https://www.linuxfoundation.org/about/careers'
        })
    
    return jobs


def scrape_lwn_news():
    """Scrape Linux Weekly News"""
    print("Scraping LWN News...")
    
    news = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        
        with httpx.Client(headers=headers, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://lwn.net/')
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # LWN has specific article structure
            articles = soup.find_all('div', class_='ArticleText')[:5]
            
            for article in articles:
                try:
                    link_elem = article.find('a')
                    if link_elem:
                        title = link_elem.text.strip()
                        link = 'https://lwn.net' + link_elem.get('href', '')
                        
                        news.append({
                            'title': title,
                            'source': 'LWN.net',
                            'link': link,
                            'date': datetime.now().strftime('%Y-%m-%d')
                        })
                except Exception as e:
                    continue
            
            if len(news) == 0:
                news.append({
                    'title': 'Visit LWN for Latest Linux News',
                    'source': 'LWN.net',
                    'link': 'https://lwn.net/',
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
    
    except Exception as e:
        print(f"Error scraping LWN: {e}")
        news.append({
            'title': 'Linux Weekly News',
            'source': 'LWN.net',
            'link': 'https://lwn.net/',
            'date': datetime.now().strftime('%Y-%m-%d')
        })
    
    return news


def scrape_linux_projects():
    """Scrape Linux Foundation projects"""
    print("Scraping Linux Foundation Projects...")
    
    projects = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        
        with httpx.Client(headers=headers, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://www.linuxfoundation.org/projects')
            soup = BeautifulSoup(response.text, 'html.parser')
            
            project_cards = soup.find_all(['div', 'article'], class_=['project', 'project-card'])
            
            for card in project_cards[:10]:
                try:
                    title_elem = card.find(['h2', 'h3', 'h4'])
                    title = title_elem.text.strip() if title_elem else 'Linux Project'
                    
                    desc_elem = card.find('p')
                    description = desc_elem.text.strip() if desc_elem else 'Open source project'
                    
                    link_elem = card.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    
                    projects.append({
                        'name': title,
                        'description': description[:150],
                        'link': link,
                        'category': 'Linux Foundation'
                    })
                except Exception as e:
                    continue
            
            if len(projects) == 0:
                # Fallback with known projects
                projects = [
                    {
                        'name': 'Linux Kernel',
                        'description': 'The core of the Linux operating system',
                        'link': 'https://www.kernel.org/',
                        'category': 'Core'
                    },
                    {
                        'name': 'Kubernetes',
                        'description': 'Container orchestration platform',
                        'link': 'https://kubernetes.io/',
                        'category': 'CNCF'
                    },
                    {
                        'name': 'Node.js',
                        'description': 'JavaScript runtime built on Chrome V8',
                        'link': 'https://nodejs.org/',
                        'category': 'OpenJS Foundation'
                    }
                ]
    
    except Exception as e:
        print(f"Error scraping projects: {e}")
        projects = [
            {
                'name': 'Explore Linux Foundation Projects',
                'description': 'Visit the projects page to see all active Linux Foundation hosted projects',
                'link': 'https://www.linuxfoundation.org/projects',
                'category': 'General'
            }
        ]
    
    return projects


def scrape_kernel_newbies():
    """Scrape Kernel Newbies learning resources"""
    print("Scraping Kernel Newbies...")
    
    resources = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        
        with httpx.Client(headers=headers, follow_redirects=True, timeout=30.0) as client:
            response = client.get('https://kernelnewbies.org/Documents')
            soup = BeautifulSoup(response.text, 'html.parser')
            
            links = soup.find_all('a')
            
            for link in links[:10]:
                try:
                    href = link.get('href', '')
                    text = link.text.strip()
                    
                    if text and len(text) > 5 and 'Documents' not in text:
                        full_link = href if href.startswith('http') else 'https://kernelnewbies.org' + href
                        
                        resources.append({
                            'title': text,
                            'type': 'Tutorial',
                            'link': full_link,
                            'source': 'Kernel Newbies'
                        })
                except Exception as e:
                    continue
            
            if len(resources) == 0:
                resources.append({
                    'title': 'Kernel Newbies Documentation',
                    'type': 'Learning',
                    'link': 'https://kernelnewbies.org/Documents',
                    'source': 'Kernel Newbies'
                })
    
    except Exception as e:
        print(f"Error scraping Kernel Newbies: {e}")
        resources.append({
            'title': 'Visit Kernel Newbies',
            'type': 'Learning',
            'link': 'https://kernelnewbies.org/',
            'source': 'Kernel Newbies'
        })
    
    return resources


def main():
    print("Starting Linux Project data scraping...")
    print("=" * 50)
    
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
    print(f"Scraping completed!")
    print(f"Internships: {len(data['internships'])}")
    print(f"Jobs: {len(data['jobs'])}")
    print(f"News: {len(data['news'])}")
    print(f"Projects: {len(data['projects'])}")
    print(f"Learning Resources: {len(data['learning'])}")
    print(f"Data saved to: {output_file}")

if __name__ == '__main__':
    main()
