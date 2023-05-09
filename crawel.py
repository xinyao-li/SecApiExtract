import requests
from bs4 import BeautifulSoup


def extract_section(url, section):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the section header
    header = soup.find(
        lambda tag: tag.name == 'p' and f'ITEM {section}' in tag.get_text(strip=True, separator=' ').upper())

    if not header:
        return None

    # Extract content until the next ITEM is found
    content = []
    sibling = header.find_next_sibling()

    while sibling and not sibling.get_text(strip=True, separator=' ').startswith('ITEM'):
        content.append(sibling)
        sibling = sibling.find_next_sibling()

    return content


url_10k = "https://www.sec.gov/Archives/edgar/data/1318605/000095017023001409/tsla-20221231.htm"
section_1A = extract_section(url_10k, "1A")

if section_1A:
    for tag in section_1A:
        print(tag.get_text(strip=True))
else:
    print("Section not found")
