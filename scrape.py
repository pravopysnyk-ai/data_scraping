for website_folder in os.listdir(website_exports_folder):
    website_folder = website_exports_folder + website_folder
    htmls = web_scraper.get_html_from_folder(website_folder)
    urls = web_scraper.extract_urls(website_folder, htmls)
    lines = web_scraper.extract_text_from_urls(urls)
    web_scraper.save_lines(lines, website_folder, output_path)