from bs4 import BeautifulSoup
import requests
import math
import os

class WebScraper(object):
    """
    Amalgamation of the functions used for scraping data for websites.
    """
    def __init__(self):
        pass

    def get_html_from_folder(self, website_folder):
        """
        Gets HTML files into a single list
        """
        html_docs = []
        for filename in os.listdir(website_folder):
            with open(os.path.join(website_folder, filename), 'r') as f:
                msg = f.read()
                html_docs.append(msg)
        return html_docs

    def extract_urls(self, website_folder, html_docs):
        """
        Extracts all readable URLs from the parsed HTMLs.
        """
        urls = []

        for doc in html_docs:
            soup = BeautifulSoup(doc, 'html.parser')
            # getting all the links and moving them to a specific list
            for link in soup.find_all('a'):
                l = link.get('href')
                urls.append(l)

        # making sure that the links left are only the urls we want
        urls = [url for url in urls if website_folder.split('/')[-1].lower() in url]
        urls = [url for url in urls if ((not '@' in url) and (len(url) > 20))]

        # removing the duplicate links
        urls = list(set(urls))


        # DON'T FORGET TO REMOVE THIS BEFORE PUSHING TO GITHUB
        # IF YOU SEE THIS -- LET ME KNOW AND I WILL FIX IT (Artem)


        urls = urls[:20]









        print(f"The URL list for {website_folder.split('/')[-1]} is compiled!\nNumber of URLs to parse: " + str(len(urls)))
        return urls

    def extract_text_from_urls(self, urls):
        """
        Extracts all lines from a given list of URLs.
        """
        # set for the lines to be added
        lines = []

        # different counters for statistics stuff
        url_counter = 0
        result_counter = 0

        # for url in the list of generater urls
        for url in urls:
            # statistics
            if url_counter % 300 == 0:
                print(str(math.floor((url_counter/len(urls))*100)) + ' % of the urls are processed. ' + str(result_counter) + ' lines were added.')
            # following the link
            # r = requests.get(url)
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) # uncomment if 403 or 429 emerge way too often
            url_counter = url_counter + 1
            if r.status_code == 403 or r.status_code == 429:
                print("The website thinks you're DDOSing it!")
            # if the link is valid
            if r.status_code == 200:
                # get the content
                p = r.content
                # most of the stuff we need comes in <p> tags, so we'll focus on them
                soup_p = BeautifulSoup(p, 'html5lib')
                text = soup_p.find_all('p')
                # for each text object we obtained
                for s in text:
                    # splitting them into lines (not sentences)
                    t = s.get_text().split('\n')
                    # if the sentence is not empty and finishes on a period (a nice way to catch the artifacts)
                    if t[0] and t[0][-1] == '.':
                        # then append it to the list
                        lines.append(t[0])
                        result_counter = result_counter + 1
            else:
                print(f"Unexpected error! This is the status code: {r.status_code}")
        print("The lines have been extracted!")
        return lines

    def save_lines(self, lines, website_folder, output_folder_path):
        text = '\n'.join(lines)
        filename = output_folder_path + "/" + website_folder.split('/')[-1] + ".txt"
        with open(filename, 'w') as f:
            f.write(text)
        print("Saved!\n")
