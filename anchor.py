import csv
import requests
from bs4 import BeautifulSoup

def read_keywords_from_csv(file_path):
    """Reads keywords from a CSV file and returns a list of keywords."""
    keywords = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            keywords.extend(row)
    return keywords

def scrape_html_from_webpage(url):
    """Scrapes the HTML text from a live webpage."""
    response = requests.get(url)
    return response.text

def check_keywords_in_html(html_text, keywords):
    """Checks the HTML text for the presence of keywords and returns a dictionary of found keywords."""
    found_keywords = {keyword: keyword in html_text for keyword in keywords}
    return found_keywords

def dump_results_to_html(html_text, found_keywords, output_file='results.html'):
    """Dumps the results into an HTML file and highlights the keywords."""
    soup = BeautifulSoup(html_text, 'html.parser')
    for keyword, found in found_keywords.items():
        if found:
            highlighted = soup.find_all(text=lambda text: keyword in text)
            for text in highlighted:
                new_text = text.replace(keyword, f'<mark>{keyword}</mark>')
                text.replace_with(new_text)
    
    with open(output_file, 'w') as file:
        file.write(str(soup))


keywords = read_keywords_from_csv('keywords.csv')  # Replace with your CSV file path
html_text = scrape_html_from_webpage('https://bartwagener.com/')  # Replace with your target URL
found_keywords = check_keywords_in_html(html_text, keywords)
dump_results_to_html(html_text, found_keywords)


# Example usage:
# keywords = read_keywords_from_csv('keywords.csv')
# html_text = scrape_html_from_webpage('https://example.com')
# found_keywords = check_keywords_in_html(html_text, keywords)
# dump_results_to_html(html_text, found_keywords)