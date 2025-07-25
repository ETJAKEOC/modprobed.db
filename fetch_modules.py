import os
import time
import random

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://web.archive.org/web/20250703123328/https://linux-hardware.org"
TIMELINE_URL = f"{BASE_URL}/?view=timeline&offset={{}}"
PAGE_DIR = "pages"
os.makedirs(PAGE_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
    )
}


def random_number(minimum=None, maximum=None):
    if maximum is None:
        mean = minimum
        minimum = 0
        maximum = mean * 2
    return random.triangular(minimum, maximum) + random.triangular(minimum, maximum)


def safe_get(url, retries=5):
    for i in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS)
            resp.raise_for_status()
            return resp
        except Exception as e:
            print(f"[!] Retry {i+1}/{retries} failed for {url}: {e}")
            time.sleep(2 ** i + random_number(1, 2))
    return None


def fetch_page(offset):
    return safe_get(TIMELINE_URL.format(offset)).text


def parse_reports(html):
    soup = BeautifulSoup(html, 'html.parser')
    return [
        BASE_URL + link['href']
        for link in soup.find_all('a', href=True)
        if '/?probe=' in link['href']
    ]


def main():
    offset = 0
    while True:
        print(f"Fetching offset {offset}...")
        html = fetch_page(offset)
        if html is None:
            print(f"[!] Failed to fetch timeline page at offset {offset}. Exiting.")
            break

        report_links = parse_reports(html)
        if not report_links:
            break

        for link in report_links:
            print(f" -> {link}")
            resp = safe_get(link)
            if resp is None:
                continue

            ts = int(time.time() * 1000)
            out = os.path.join(PAGE_DIR, f"{ts}.html")
            with open(out, 'w', encoding='utf-8') as f:
                f.write(resp.text)
            print(f"   [+] Saved: {out}")
            time.sleep(random_number(4, 6))  # 4–6 seconds between requests

        offset += 100


if __name__ == "__main__":
    main()
