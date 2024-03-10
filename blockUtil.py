import requests
import json


def getStatusLS(domain):
    headers = {
            'authority': 'production-archive-proxy-api.lightspeedsystems.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://archive.lightspeedsystems.com',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'x-api-key': 'onEkoztnFpTi3VG7XQEq6skQWN3aFm3h'
        }

    json_data = {
            'query': "\nquery getDeviceCategorization($itemA: CustomHostLookupInput!, $itemB: CustomHostLookupInput!){\n  a: custom_HostLookup(item: $itemA) {\n    request {\n      host\n    }\n    cat\n    action\n    source_ip\n    archive_info {\n      filter {\n        category\n        transTime\n        reason\n        isSafetyTable\n        isTLD\n      }\n      rocket {\n        category\n      }\n    }\n  }\n  b: custom_HostLookup(item: $itemB) {\n    request {\n      host\n    }\n    cat\n    action\n    source_ip\n    archive_info {\n      filter {\n        category\n        transTime\n        reason\n      }\n      rocket {\n        category\n      }\n    }\n  }\n}",
            'variables': {
                'itemA': {
                    'hostname': domain,
                    'getArchive': True,
                },
                'itemB': {
                    'hostname': domain,
                    'getArchive': True,
                },
            },
        }

    response = requests.post(
            'https://production-archive-proxy-api.lightspeedsystems.com/archiveproxy',
            headers=headers,
            json=json_data,
        )
    
    lsfilter = response.json()["data"]["a"]["archive_info"]["filter"]["category"]

    with open("blocklist.json", "r") as f:
        data = json.load(f)
        for entry in data:
            if (entry["CategoryNumber"] == lsfilter):
                if (entry["Allow"] == "1"):
                    return "Unblocked"
                elif (entry["Allow"] == "0"):
                    return "Blocked"
                else:
                    return "Blocked"
            
        return "Blocked"

