import scrapy


class UserSpider(scrapy.Spider):
    name = "profile_spider"
    start_urls = [
        "http://picbear.com/twicetagram"
    ]

    def parse(self, response):
        for content in response.css("div.container div.grid-media"):
            if content.css("i.fa"):
                vidlink = response.urljoin(content.css("a.grid-media-media::attr(href)").extract_first())
                yield scrapy.Request(vidlink, callback=self.parse_vid)

            elif content.css("img::attr(alt)").extract_first() != "@twicetagram" and content.css("img::attr(src)"):
                yield {
                    "type": "img",
                    "image": content.css("img::attr(src)").extract_first(),
                    "desc": content.css("img::attr(alt)").extract_first(),
                }

    def parse_vid(self, response):
        yield {
            "type": "video",
            "content": response.css("video source::attr(src)").extract_first(),
            "image": response.css("video::attr(poster)").extract_first(),
            "desc": response.css("div.media-caption p::text").extract_first()
        }
