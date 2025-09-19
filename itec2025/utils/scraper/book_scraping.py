from urllib.parse import urljoin
import requests, time
from bs4 import BeautifulSoup
BASE = 'https://books.toscrape.com/'

class Gateway:
    UA = {"User-Agent":"Estamos scrapeando"}
    
    def fetch(self, url: str, timeout=15) -> str:
        response = requests.get(url, headers=self.UA, timeout=timeout)
        response.raise_for_status()
        return response.text

class Parser:
    def parse_titles(self, html):
        soup = BeautifulSoup(html, 'lxml')
        titles = [
            titulo.get('title') 
            for titulo in 
            soup.select("article.product_pod h3 a")
        ]
        print(titles)

class Service:
    def __init__(self, gateway=Gateway, parser=Parser):
        self.gateway = gateway()
        self.parser = parser()

    def run(self, url=BASE):
        while url:
            html = self.gateway.fetch(url)
            titles = self.parser.parse_titles(html)
            return titles

""" 
from utils.scraper.book_scraping import Service, Gateway, Parser
service = Service(gateway=Gateway, parser=Parser)
service.run()
"""