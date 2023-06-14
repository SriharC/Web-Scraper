import string
import requests
import os
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url, element, attribute=None, attribute_value=None):
        self.URL = url
        self.element = element
        self.attribute = attribute
        self.attribute_value = attribute_value
        self.start()

    def start(self):
        try:
            number = int(input("Enter the number of pages to scrape: "))
            r = requests.get(self.URL, headers={'Accept-Language': 'en-US,en;q=0.5'})
            if r.status_code != 200:
                print(f'The URL returned {r.status_code}!')
                return
            links = self.find_elements(r.content)
            for i in range(1, number + 1):
                dirname = 'Page_' + str(i)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                os.chdir(dirname)
                if links:
                    self.process_element(links[i - 1])
                os.chdir(os.pardir)
            print("Scraping completed!")
        except ValueError:
            print('Wrong number!')

    def find_elements(self, content):
        links = list()
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(self.element, attrs={self.attribute: self.attribute_value}) if self.attribute else soup.find_all(self.element)
        for element in elements:
            link = element.get('href')
            if link:
                links.append(link)
        return links

    def process_element(self, link):
        r = requests.get(self.URL + link, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('title')
        filename = self.format_filename(title.text)
        self.save_element(filename, soup)

    def format_filename(self, title):
        filename = ''
        for letter in title:
            if letter in string.punctuation or letter in string.whitespace:
                filename += '_'
            else:
                filename += letter
        if filename[-1] == '_':
            filename = filename[:-1] + '.html'
        else:
            filename += '.html'
        return filename

    def save_element(self, filename, soup):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        print(f"Element {filename} saved.")


if __name__ == "__main__":
    url = input("Enter the URL to scrape: ")
    element = input("Enter the HTML element to scrape: ")
    attribute = input("Enter the attribute name (optional): ")
    attribute_value = input("Enter the attribute value (optional): ")
    Scraper(url, element, attribute, attribute_value)
