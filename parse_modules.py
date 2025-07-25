import os
import time
import re

from bs4 import BeautifulSoup


PAGE_DIR = "pages"
OUTDIR = "modprobed_raw"
os.makedirs(OUTDIR, exist_ok=True)

ALLOWED_TYPES = {
    "desktop",
    "docking station",
    "notebook",
    "tablet",
    "convertible",
    "portable",
    "all in one",
    "all-in-one",
    "space-saving",
    "mini tower",
    "mini pc",
    "low profile",
    "hand held",
    "detachable",
    "soc",
}


def should_keep(soup):
    host_box = soup.find('div', id='host')
    if not host_box:
        host_box = soup
    text = host_box.get_text().lower()

    type_match = any(t in text for t in ALLOWED_TYPES)
    arch_match = 'x86' in text
    years = re.findall(r'20\d{2}', text)
    year_match = any(int(y) >= 2010 for y in years)

    if type_match and arch_match and year_match:
        print(f"   [✓] MATCH: type={type_match}, arch={arch_match}, year={year_match}")
        return True
    else:
        print(f"   [x] SKIP: type={type_match}, arch={arch_match}, year={year_match}")
        return False


def extract_drivers(soup):
    drivers = []
    table = soup.find('table')
    if not table:
        return []

    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) >= 5:
            driver = cols[4].get_text().strip()
            if driver and driver != '-':
                drivers.append(driver)
    return drivers


def main():
    for file in sorted(os.listdir(PAGE_DIR)):
        if not file.endswith(".html"):
            continue

        filepath = os.path.join(PAGE_DIR, file)
        print(f"Parsing {filepath}...")
        with open(filepath, encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')
        if should_keep(soup):
            drivers = extract_drivers(soup)
            if drivers:
                ts = int(time.time() * 1000)
                out = os.path.join(OUTDIR, f"{ts}.txt")
                with open(out, 'w') as f:
                    for drv in drivers:
                        f.write(drv + "\n")
                print(f"   [+] Saved: {out}")


if __name__ == "__main__":
    main()
