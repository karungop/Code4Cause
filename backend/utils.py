import requests
from bs4 import BeautifulSoup

# Function to scrape an individual Yahoo News article
def scrape_yahoo_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    try:
        title = soup.find('h1').text.strip()
    except AttributeError:
        title = None

    # Extract source (usually in a span with class 'caas-attr-source')
    try:
        source = soup.find('span', class_='caas-attr-source').text.strip()
    except AttributeError:
        source = None

    # Extract the description (article content)
    try:
        description = soup.find('div', class_='caas-body').text.strip()
    except AttributeError:
        description = None

    # Extract time (usually in a span with class 'caas-attr-time')
    try:
        time = soup.find('span', class_='caas-attr-time').text.strip()
    except AttributeError:
        time = None

    # Return the scraped data in a dictionary
    article_data = {
        'Title': title,
        'Source': source,
        'Description': description,
        'Link': url,
        'Time': time
    }

    return article_data

# Main function to scrape article information
def get_article_info(url):
    article_data = scrape_yahoo_article(url)
    return article_data
