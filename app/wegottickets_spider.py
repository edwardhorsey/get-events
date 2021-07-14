import scrapy
import simplejson as json

# This needs to be set!
maximum_items = 50


class WeGotTicketsSpider(scrapy.Spider):
    name = "wegottickets"
    request_counter = 0

    def parse(self, response):
        for event in response.css("a.event_link"):
            if self.request_counter < maximum_items:
                self.increment_requests()
                yield response.follow(event, self.parse_event)

        pagination_link = response.css(".nextlink::attr(href)").get()
        if pagination_link and self.request_counter < maximum_items:
            yield response.follow(pagination_link, self.parse)

    def parse_event(self, response):
        event_information = response.css("div.event-information")
        event_location = response.css("div.EventLocation")
        tickets = response.css("div.BuyBox.block")

        title = self.extract_with_css(event_information, "h1::text")
        date = self.extract_with_css(
            event_information, "table > tr:nth-child(2) > td:nth-child(2)::text"
        )
        time = self.extract_with_css(
            event_information, "table > tr:nth-child(3) > td:nth-child(2)::text"
        )
        city, venue = self.extract_city_and_venue(event_information)
        address = self.extract_address(event_location)
        prices = self.extract_prices(tickets)

        yield {
            "artists": title,
            "city": city,
            "date": date,
            "time": time,
            "venue_name": venue,
            "venue_address": address,
            "price": prices,
            "event_url": response.url,
        }

    def extract_with_css(self, selection, query):
        return selection.css(query).get(default="").strip()

    def extract_address(self, selection):
        return selection.xpath("//ul/li[1]/span/span[1]/text()").extract()

    def extract_city_and_venue(self, selection):
        city_and_venue = self.extract_with_css(
            selection, "table > tr:nth-child(1) > td:nth-child(2) > a::text"
        )

        if ": " in city_and_venue:
            city_and_venue = city_and_venue.split(": ")
            return city_and_venue[0], city_and_venue[1]
        else:
            return city_and_venue, city_and_venue

    def extract_prices(self, tickets):
        return [
            {
                "name": ticket.css("td.half.text-top > h2::text").get(),
                "price-components": ticket.css("div.price::text").get()[:-2],
                "price-total": ticket.css("div.price > strong::text").get()[1:],
            }
            for ticket in tickets
        ]

    def increment_requests(self):
        self.request_counter += 1
