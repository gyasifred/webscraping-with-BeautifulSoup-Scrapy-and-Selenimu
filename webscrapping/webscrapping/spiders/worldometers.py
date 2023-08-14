import scrapy


class WorldometersSpider(scrapy.Spider):
    name = 'worldometers'
    allowed_domains = ['www.worldometers.info']
    start_urls = [
        'https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        #title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')
        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            #absolute_url = f'https://{self.allowed_domains[0]}{link}'
            absolute_url = response.urljoin(link)

            yield scrapy.Request(url=absolute_url, callback=self.parse_country, meta={"Country": country_name})

    def parse_country(self, response):
        country = response.request.meta['Country']
        rows = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                'Country': country,
                'Year': year,
                "Population": population
            }
