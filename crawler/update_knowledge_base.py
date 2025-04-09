from saas_sales_agent.crawler.website_crawler import WebsiteCrawler
from saas_sales_agent.knowledge_base.elasticrun_kb import ElasticRunKnowledgeBase
import json
from typing import Dict, List
import re

def extract_product_info(content: Dict) -> Dict:
    """Extract product information from crawled content."""
    products = {}
    
    for url, page_content in content.items():
        # Look for product sections
        for section_title, section_content in page_content['sections'].items():
            if 'product' in section_title.lower() or 'platform' in section_title.lower():
                # Extract product name
                product_name_match = re.search(r'(Libera|RTMNxt|Mity|ElasticRun|ElasticRun Platform)', section_title)
                if product_name_match:
                    product_name = product_name_match.group(1)
                    if product_name not in products:
                        products[product_name] = {
                            'description': '',
                            'features': [],
                            'metrics': {},
                            'benefits': [],
                            'use_cases': []
                        }
                    
                    # Extract features
                    if 'feature' in section_title.lower():
                        features = re.findall(r'([^:]+):\s*([^\n]+)', section_content)
                        for name, description in features:
                            products[product_name]['features'].append({
                                'name': name.strip(),
                                'description': description.strip()
                            })
                    
                    # Extract metrics
                    if 'metric' in section_title.lower() or 'stat' in section_title.lower():
                        metrics = re.findall(r'([^:]+):\s*([^\n]+)', section_content)
                        for name, value in metrics:
                            products[product_name]['metrics'][name.strip()] = value.strip()
                    
                    # Extract benefits
                    if 'benefit' in section_title.lower():
                        benefits = [line.strip() for line in section_content.split('\n') if line.strip()]
                        products[product_name]['benefits'].extend(benefits)
                    
                    # Extract use cases
                    if 'use case' in section_title.lower():
                        use_cases = [line.strip() for line in section_content.split('\n') if line.strip()]
                        products[product_name]['use_cases'].extend(use_cases)
    
    return products

def extract_industry_info(content: Dict) -> Dict:
    """Extract industry information from crawled content."""
    industries = {}
    
    for url, page_content in content.items():
        # Look for industry sections
        for section_title, section_content in page_content['sections'].items():
            if 'industry' in section_title.lower():
                # Extract industry name
                industry_name_match = re.search(r'(E-Commerce|Courier, Express, Parcel \(CEP\)|Parcels and Posts|Freight Forwarders)', section_title)
                if industry_name_match:
                    industry_name = industry_name_match.group(1)
                    if industry_name not in industries:
                        industries[industry_name] = {
                            'description': '',
                            'use_cases': [],
                            'challenges': [],
                            'solutions': []
                        }
                    
                    # Extract use cases
                    if 'use case' in section_title.lower():
                        use_cases = [line.strip() for line in section_content.split('\n') if line.strip()]
                        industries[industry_name]['use_cases'].extend(use_cases)
                    
                    # Extract challenges
                    if 'challenge' in section_title.lower():
                        challenges = [line.strip() for line in section_content.split('\n') if line.strip()]
                        industries[industry_name]['challenges'].extend(challenges)
                    
                    # Extract solutions
                    if 'solution' in section_title.lower():
                        solutions = [line.strip() for line in section_content.split('\n') if line.strip()]
                        industries[industry_name]['solutions'].extend(solutions)
    
    return industries

def update_knowledge_base():
    # Initialize crawler
    crawler = WebsiteCrawler('https://saas.elastic.run/')
    
    # Crawl the website
    print("Starting website crawl...")
    content = crawler.crawl()
    
    # Save crawled content
    crawler.save_content('crawled_content.json')
    
    # Extract information
    print("Extracting product information...")
    products = extract_product_info(content)
    
    print("Extracting industry information...")
    industries = extract_industry_info(content)
    
    # Update knowledge base
    kb = ElasticRunKnowledgeBase()
    
    # Update products
    for product_name, product_info in products.items():
        product = kb.get_product_by_name(product_name)
        if product:
            # Update existing product
            product.description = product_info.get('description', product.description)
            product.features.extend([ProductFeature(f['name'], f['description']) for f in product_info.get('features', [])])
            product.metrics.update(product_info.get('metrics', {}))
            product.benefits.extend(product_info.get('benefits', []))
            product.use_cases.extend(product_info.get('use_cases', []))
    
    # Update industries
    for industry_name, industry_info in industries.items():
        industry = kb.get_industry_by_name(industry_name)
        if industry:
            # Update existing industry
            industry.description = industry_info.get('description', industry.description)
            industry.use_cases.extend(industry_info.get('use_cases', []))
            industry.challenges.extend(industry_info.get('challenges', []))
            industry.solutions.extend(industry_info.get('solutions', []))
    
    print("Knowledge base updated successfully!")

if __name__ == "__main__":
    update_knowledge_base() 