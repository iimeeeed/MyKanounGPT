import requests
import os
from bs4 import BeautifulSoup

# Base URL for POST requests
base_url = "https://www.joradp.dz/SCRIPTS/Joa_Rec.dll/AffPost"

# Common headers
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Dnt": "1",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "frame",
    "Referer": "https://www.joradp.dz/SCRIPTS/JOA_Rec.dll/OptPost",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7,fr;q=0.6",
}

# Session setup
session = requests.Session()
session.headers.update(headers)
session.cookies.set("cookiesession1", "678A3E4D09196D26E740E257F586C55C")

def make_request(dval_value):
    # Payload data including the incrementing `dval`
    data = {
        "Client": "66051",
        "Start": "0",
        "dfon": "3",  # This seems fixed, as provided
        "dval": str(dval_value)
    }

    response = session.post(base_url, data=data)
    print(f"Requested page with dval={dval_value}: Status Code = {response.status_code}")
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve page with dval={dval_value}. Status Code = {response.status_code}")
        return None

def extract_text_from_html(html_content):
    decoded_content = html_content.decode('windows-1256')
    soup = BeautifulSoup(decoded_content, 'html.parser')
    return soup.get_text(separator='\n', strip=True)

def save_text(text_content, dval_value):
    filename = f"page_dval_{dval_value}.txt"
    with open(filename, "w", encoding="utf-8") as text_file:
        text_file.write(text_content)
    print(f"Saved page with dval={dval_value} to '{filename}'")

# Ensure output directory exists
os.makedirs("output", exist_ok=True)
os.chdir("output")

# Loop through the pattern of dval values and scrape each page
dval_values = [-199] + [i for i in range(1, 29579, 200)]  # Pattern starts with -199, then increments by 200
for dval in dval_values:
    html_content = make_request(dval)
    if html_content:
        extracted_text = extract_text_from_html(html_content)
        save_text(extracted_text, dval)