import pytest
import scrapy
import simplejson as json
import os.path
from scrapy.crawler import CrawlerProcess
from app.wegottickets_spider import WeGotTicketsSpider

filename = "all.html"
folder = "tests/example-site/search-results"
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
url = f"file://{base_dir}/{folder}/{filename}"
results_file = "tests/tmp/items.json"


def empty_results():
    if os.path.exists(results_file):
        json_file = open(results_file, "r+")
        json_file.truncate(0)


@pytest.fixture(scope="session")
def spider_results():
    empty_results()
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                results_file: {"format": "json"},
            },
        }
    )
    process.crawl(WeGotTicketsSpider, start_urls=[url])
    process.start()

    with open(results_file) as json_file:
        data = json.load(json_file)
        return data


def test_contains_first_event_title(spider_results):
    contains_first_event_title = False
    first_event_title = "Arkwright\u2019s Special Pass"

    for item in spider_results:
        if item["artists"] == first_event_title:
            contains_first_event_title = True
            break

    assert contains_first_event_title


def test_contains_entire_sixth_event(spider_results):
    contains_sixth_event = False
    for item in spider_results:
        if (
            item["artists"] == "Riviera Ramblers"
            and item["city"] == "ASHBURTON"
            and item["date"] == "Sunday 30th May, 2021"
            and item["time"] == "Door time: 12:30pm, Start time: 1:00pm"
            and item["venue_name"] == " Arts Centre"
            and "".join(item["venue_address"])
            == "".join(["15 West St", "Ashburton", "TQ13 7DT"])
            and json.dumps(item["price"])
            == json.dumps(
                [
                    {
                        "name": "Full Price (Support the Artists and the Arts)",
                        "price-components": "\u00a39.00 + \u00a30.90 Booking fee ",
                        "price-total": "9.90",
                    },
                    {
                        "name": "Mid Price (a bit cheaper if you need it)",
                        "price-components": "\u00a36.00 + \u00a30.60 Booking fee ",
                        "price-total": "6.60",
                    },
                    {
                        "name": "Low Price (even cheaper for anyone who needs it)",
                        "price-components": "\u00a33.00 + \u00a30.30 Booking fee ",
                        "price-total": "3.30",
                    },
                ]
            )
        ):
            contains_sixth_event = True
            break

    assert contains_sixth_event


def test_contains_all_events(spider_results):
    assert len(spider_results) == 20
