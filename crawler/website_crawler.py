import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from typing import Set, Dict, List
import re

class WebsiteCrawler:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.visited_urls: Set[str] = set()
        self.content: Dict[str, Dict] = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def is_valid_url(self, url: str) -> bool:
        """Check if the URL is valid and belongs to the same domain."""
        parsed_url = urlparse(url)
        base_domain = urlparse(self.base_url).netloc
        return (
            parsed_url.netloc == base_domain and
            not url.endswith(('.pdf', '.jpg', '.png', '.gif', '.zip', '.doc', '.docx')) and
            '#' not in url
        )

    def extract_content(self, soup: BeautifulSoup) -> Dict:
        """Extract relevant content from a page."""
        content = {
            'title': '',
            'text': '',
            'links': [],
            'sections': {}
        }

        # Extract title
        title = soup.find('title')
        if title:
            content['title'] = title.text.strip()

        # Extract main content
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main'))
        if main_content:
            # Extract text content
            paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
            content['text'] = '\n'.join(p.text.strip() for p in paragraphs if p.text.strip())

            # Extract sections
            for section in main_content.find_all(['section', 'div'], class_=re.compile(r'section|feature|benefit|solution')):
                section_title = section.find(['h2', 'h3'])
                if section_title:
                    title_text = section_title.text.strip()
                    section_content = '\n'.join(p.text.strip() for p in section.find_all(['p', 'li']) if p.text.strip())
                    content['sections'][title_text] = section_content

        # Extract links
        for link in soup.find_all('a', href=True):
            url = urljoin(self.base_url, link['href'])
            if self.is_valid_url(url):
                content['links'].append(url)

        return content

    def crawl_page(self, url: str) -> None:
        """Crawl a single page and its content."""
        if url in self.visited_urls:
            return

        print(f"Crawling: {url}")
        self.visited_urls.add(url)

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                self.content[url] = self.extract_content(soup)

                # Crawl linked pages
                for link in self.content[url]['links']:
                    if link not in self.visited_urls:
                        time.sleep(1)  # Be nice to the server
                        self.crawl_page(link)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    def crawl(self) -> Dict[str, Dict]:
        """Start crawling from the base URL."""
        self.crawl_page(self.base_url)
        return self.content

    def save_content(self, filename: str) -> None:
        """Save crawled content to a file."""
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.content, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_content(filename: str) -> Dict:
        """Load crawled content from a file."""
        import json
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f) 