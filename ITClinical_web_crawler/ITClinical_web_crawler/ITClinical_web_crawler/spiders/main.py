import scrapy
import csv


class ITClinicalCrawler(scrapy.Spider):
    name = 'itclinical'
    start_urls = ["https://itclinical.com/it.php"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_file = open("ITClinical_Data.csv", "w", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Title", "Feature"])

    def closed(self, reason):
        print(f"Closed: {reason}")
        self.csv_file.close()

    def parse(self, response, **kwargs):
        print("Visited", response.url)
        sections = response.xpath('//a[contains(@href, "it.php")]/following-sibling::ul/li/a/@href').getall()
        print("Sections Found:", sections)
        for section in sections:
            yield response.follow(section, callback=self.parse_section)

    def parse_section(self, response):
        title = response.xpath('//h2/text()').get()
        features = []

        if title:
            title = title.strip()
            features = response.xpath('//div[@class="container"]//h3[@class="margin-reset"]/following-sibling::ul/li/text()').getall()
        else:
            print("Page not found")

        print(title, "\n")
        for feature in features:
            feature = feature.strip()
            print("    ", feature)
            self.csv_writer.writerow([title, feature])

        print("\n")
