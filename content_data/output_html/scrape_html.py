import requests
from bs4 import BeautifulSoup

# URL for the POST request
url = "https://www.joradp.dz/SCRIPTS/Joa_Rec.dll/AffPost"

# Headers (as used in your POST request)
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://www.joradp.dz/SCRIPTS/JOA_Rec.dll/OptPost",
    "Dnt": "1",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7,fr;q=0.6",
    "Origin": "https://www.joradp.dz"
}

# Starting values for dval
dval_start = -199
dval_increment = 200
dval_max = 29578

# Iterate through each dval in the range
for dval in range(dval_start, dval_max + 1, dval_increment):
    # Data for the POST request
    data = {
        "Client": "66051",
        "Start": "0",
        "dfon": "3",
        "dval": str(dval)  # Set the dval for each request
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=data)

    # Decode the response using the correct encoding (windows-1256)
    decoded_content = response.content.decode('windows-1256')

    # Parse the HTML content using BeautifulSoup (without from_encoding)
    soup = BeautifulSoup(decoded_content, 'html.parser')

    # Define the filename based on dval
    filename = f"page_dval_{dval}.html"

    # Save the content to a file using the correct encoding
    with open(filename, "w") as file:
        file.write(soup.prettify())

    print(f"Saved page with dval={dval} to {filename}")