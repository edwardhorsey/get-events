# Get events
## Install (requires Python 3.8)
`python3 -m venv get-events`

`source get-events/bin/activate` to enter env

`python3 -m pip install -r requirements.txt`

## Run scraper
`python3 app/run_spider.py`

Please note: `app/wegottickets_spider.py` line 5 `maximum_items = 50` is where to override the number of results.

## Run tests
`pytest`

Please note: if `maximum_items` variable is less than 20, 1 test will fail.


## Finish
`deactivate` to leave venv

## Extra
This is an unfinished solution. Further improvements to this script would include

- Scrape music category pages only
- Set the `maximum_items` variables as a flag when running the python script
- Order results by date. I used [Scrapy](https://scrapy.org/) for this task which scrapes asynchronously. To fetch events in date order some options could be to: 
   - add a datetime string as meta data to each scrape request and yield this to each result, 
   - reduce the number of consecutive scrape requests to 1, 
   - or deduce the appropriate date from the scraped data when cleaning the data..
   - I would need to look into this further..!