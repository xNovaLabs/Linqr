import requests
import json
import os
from bs4 import BeautifulSoup as bs
import blockUtil


unblockedDomains = []
domains = []
ids = []
for i in range(10):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'tz=9Ac0bCS9vl16NEKqkgUZV41l; __utma=4955364.869240143.1709500076.1709500076.1709500076.1; __utmz=4955364.1709500076.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); PHPSESSID=eb7coustcqe7agj994q6dgvo9s',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'page': i+1,
    }

    response = requests.get('https://freedns.afraid.org/domain/registry/', params=params, headers=headers)
    soup = bs(response.text, features="html.parser")
    atags = [a for a in soup.find_all("a")]
    for domain in atags:
        if ("/subdomain/edit.php?edit_domain_id" in str(domain)):
            domains.append(domain.contents[0])
            print(domain.contents[0])

  
print(domains)        

if (os.path.exists("./validatedDomains.json")):
        os.remove("validatedDomains.json")
count = 0
for domain in domains:

    domainStatus = blockUtil.getStatusLS(domain=domain)
    print(domainStatus)
    if (domainStatus == "Unblocked"):
                entry = {'domain': domain}
                print(entry)
                unblockedDomains.append(entry)

    count = count + 1
                
print(unblockedDomains)
with open("validatedDomains.json", mode='w', encoding='utf-8') as f:
    json.dump(unblockedDomains, f)