from poplib import CR
import sys
import requests
import os
from bs4 import BeautifulSoup
from preprocess import removeSGML
from collections import deque
import time


class Crawler:
    def __init__(self):
        self.header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
        }


    def get_robot(self):
        """Currently unused as files we crawl does not have robots.txt"""
        pathArray = self.baseURL.split('/')
        robotURL = pathArray[0] + '//' + pathArray[2] + '/robots.txt'
        print(robotURL)
        r = requests.get(robotURL, headers=self.header)
        r.raise_for_status()
        return r.text


    def crawlDebate(self, URL, url_div_id={}, content_div_id={}, baseURL='https://', output_folder='folder', wait_time=0.1):
        """Specialized to crawl CPD debate page"""
        # create folder if needed
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)


        # request URL and build soup
        r = requests.get(URL, headers=self.header)
        r.raise_for_status()
        mainPageSoup = BeautifulSoup(r.text, 'html.parser')

        # extract href from html
        links = mainPageSoup.find('div', url_div_id)
        links = links.find_all('a')
        hrefs = []
        for link in links:
            href = link['href']
            if href[:8] != 'https://' and href[:7] != 'http://':
                href = baseURL + href
            hrefs.append(href)
        
        # search over all file in href
        for i, href in enumerate(hrefs):
            # get website content
            # if not self.isValid(href):
            #     continue
            print(f'process {href}')
            r = requests.get(href, headers=self.header)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
            debate = soup.find('div', content_div_id)

            # add to local file
            if os.path.exists(f"{output_folder}/file{i}.output"):
                os.remove(f"{output_folder}/file{i}.output")
            with open(f'{output_folder}/file{i}.txt', 'a+') as file:
                content = debate.find_all('p')
                for sentence in content:
                    file.write(sentence.getText() + '\n')

            # wait for a few second for website to rest
            time.sleep(wait_time)
        return



def main():
    crawler = Crawler()
    # crawl CPD
    crawler.crawlDebate(URL = 'https://www.debates.org/voter-education/debate-transcripts/',
                        url_div_id = {'id' : 'content-sm'},
                        content_div_id = {'id' : 'content-sm'},
                        baseURL = 'https://www.debates.org',
                        output_folder = 'CPD_debate',
                        wait_time = 0.1)

    # crawl presidency
    crawler.crawlDebate(URL = "http://www.presidency.ucsb.edu/debates.php",
                        url_div_id = {"class": "field-body"},
                        content_div_id = {'class' : 'field-docs-content'},
                        baseURL = 'http://www.presidency.ucsb.edu',
                        output_folder = 'presidency_debate',
                        wait_time = 1)

if __name__ == "__main__":
    main()