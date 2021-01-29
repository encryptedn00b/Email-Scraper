from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

fucking_user_url = str (input('[+] Enter Target URL To Scan: '))
urls = deque([fucking_user_url])

fucking_scraped_url = set()
lmao_emails = set()

count = 0
try:
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        fucking_scraped_url.add(url)

        parts  = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}' .format(parts)

        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print('[%d] Fucking Processing !! %s' % (count, url))
        try:
            reponse = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) :
            continue

        new_email = set(re.findall(r"[a-z0-9\.\-+]+@[a-z0-9\.\-+]+\.[a-z]+", reponse.text, re.I ))
        lmao_emails.update(new_email)

        soup = BeautifulSoup (reponse.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url  + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in fucking_scraped_url:
                urls.append(link)
except KeyboardInterrupt:
    print('[-] Closing!')                

for mail in lmao_emails:
    print(mail) 