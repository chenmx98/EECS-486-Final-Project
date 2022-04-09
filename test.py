
from poplib import CR
import sys
import requests
import os
from bs4 import BeautifulSoup
from preprocess import removeSGML
from collections import deque
import time

header = { 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}

href = "http://www.presidency.ucsb.edu/debates.php"
r = requests.get(href, headers=header)
r.raise_for_status()

soup = BeautifulSoup(r.text, 'html.parser')
content = soup.find('div', {"class": "field-body"})
links = content.find_all('a')
for link in links:
    print(f"{link['href']}")