import scrapy
import simplejson as json
import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from wegottickets_spider import WeGotTicketsSpider

url = "https://www.wegottickets.com/searchresults/all"


def run_spider():
    now = str(datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S"))
    results_location = f"results/{now}.json"

    process = CrawlerProcess(
        settings={
            "FEEDS": {
                results_location: {"format": "json"},
            },
        }
    )
    process.crawl(WeGotTicketsSpider, start_urls=[url])
    process.start()

    return results_location


if __name__ == "__main__":
    print("Running spider")
    results_location = run_spider()
    print("\nSpider finished")
    print(f"Please find your results here -> ./{results_location}")
