import requests
from bs4 import BeautifulSoup


class LightScraper:
    def __init__(self):
        # Initialize the LightScraper object
        self.url = None
        self.wanted_list = None
        self.result = None

    def set_url(self, url):
        """Set the URL of the website to scrape."""
        # Set the URL to scrape
        self.url = url

    def set_wanted_list(self, wanted_list):
        """Set the list of data elements to extract from the website."""
        # Set the list of desired data elements
        self.wanted_list = wanted_list

    def scrape(self):
        """
        Scrape the website and extract the desired data.

        This method sends an HTTP GET request to the specified URL, retrieves the website content,
        and uses BeautifulSoup to parse the HTML. It extracts the text from the desired elements
        specified in the wanted_list and stores the result in the 'result' attribute.
        """
        # Check if the URL and wanted_list are set
        if not self.url or not self.wanted_list:
            raise ValueError("URL and wanted_list must be set before calling scrape().")

        # Send an HTTP GET request to the website
        response = requests.get(self.url)
        if response.status_code != 200:
            raise ConnectionError("Failed to fetch the website content.")

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the desired elements
        self.result = [self.get_text_from_element(soup, item) for item in self.wanted_list]

    def get_text_from_element(self, soup, item):
        """
        Extract the text from a specific HTML element identified by item.

        This method uses CSS selectors to find the specified HTML element within the parsed HTML
        and extracts its text content.
        """
        # Find the element using CSS selectors
        element = soup.select_one(item)
        if element:
            # Extract the text content of the element
            return element.text.strip()
        else:
            return ''

    def save_data(self, filename):
        """
        Save the scraped data to a text file.

        This method saves the scraped data stored in the 'result' attribute to a text file.
        Each item in the result list is written as a separate line in the file.
        """
        # Check if there is data available to save
        if not self.result:
            raise ValueError("No data available to save. Run scrape() method first.")

        # Write the scraped data to the file
        with open(filename, 'w') as file:
            for item in self.result:
                file.write(item + '\n')


# Example usage
if __name__ == '__main__':
    # Create an instance of LightScraper
    scraper = LightScraper()

    # Set the URL of the website to scrape
    scraper.set_url('https://example.com')

    # Set the list of data elements to extract
    scraper.set_wanted_list(['h1', 'p'])

    # Scrape the website and extract the desired data
    scraper.scrape()

    # Save the scraped data to a file
    scraper.save_data('scraped_data.txt')
