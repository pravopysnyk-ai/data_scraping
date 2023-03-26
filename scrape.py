from data_classes.WebScraper import WebScraper
from data_classes.TextMerger import TextMerger
import os

def main(website_exports_folder="/data/raw_exports", output_path="data/output"):
    """
    Main function for getting the links from Telegram exports and getting the text from them.
    """
    # initialization
    web_scraper = WebScraper()
    text_merger = TextMerger()
    # if the output path does not exist, create it
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # scraping the text from each link
    for website_folder in os.listdir(website_exports_folder):
        website_folder = website_exports_folder + website_folder
        htmls = web_scraper.get_html_from_folder(website_folder)
        urls = web_scraper.extract_urls(website_folder, htmls)
        lines = web_scraper.extract_text_from_urls(urls)
        web_scraper.save_lines(lines, website_folder, output_path)
    # and merging it together
    text_merger.merge_text(output_path)
    return 0

if __name__ == "__main__":
    main()