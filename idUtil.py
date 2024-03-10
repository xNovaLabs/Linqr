import requests
from bs4 import BeautifulSoup as bs

def getID(domain):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'tz=9Ac0bCS9vl16NEKqkgUZV41l; PHPSESSID=5q5e8fvuulivu6rddn7ran5gr1; dns_cookie=Sax1DsBBobQPaIRoQ4yVGPeY; __utma=4955364.869240143.1709500076.1709500076.1710102702.2; __utmb=4955364; __utmc=4955364; bgcolor=black',
        'Referer': 'https://freedns.afraid.org/domain/registry/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'sort': '5',
        'q': domain,
        'submit': 'SEARCH',
    }

    response = requests.get('https://freedns.afraid.org/domain/registry/', params=params, headers=headers)


    soup = bs(response.text, features="html.parser")
    atags = [a for a in soup.find_all("a")]
    for domain in atags:
        if ("/subdomain/edit.php?edit_domain_id" in str(domain)):
            return (domain["href"].split("=", 1)[1])

    return "Invalid"


