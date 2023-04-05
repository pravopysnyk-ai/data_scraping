# Dataset collection and cleaning

Amalgamation of all the methods we used for clean data collection. 

Terms and conditions of each website we scraped data from can be found here: [[1]](https://suspilne.media/terms-of-use/), [[2]](https://www.pravda.com.ua/rules/), [[3]](https://kunsht.com.ua/pro-proekt/), [[4]](https://www.bbc.com/ukrainian/institutional-38144387), [[5]](https://www.lbi.ua/about/reprint/)

## Installation

First, you need to initialize the helper submodule directory:

`git submodule update --init`

Then, run the following command to install all necessary packages:

`pip install -r requirements.txt`

The project was tested using Python 3.7.

## Scraping

To launch the data collection process, run `python scrape.py`. Before doing that, please check terms and conditions of each website we included.

## Dataset Cleaning

After the data has been collected, run `python create_dataset.py`. 
All these functions are tailored to our module architecture, so if you want to do something more specific, you might want to edit our filters.
