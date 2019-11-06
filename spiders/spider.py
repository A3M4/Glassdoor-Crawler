import scrapy
import re
import urllib.request
import json
from ..items import GlassdoorItem

jobtitle = input("Please enter the job title you want to crawl \n"
                 "(word separated by '-', e.g. web-developer) :")
pages = input("Please enter the number of pages you want to crawl :")


class MonsterSpider(scrapy.Spider):
    name = 'glass'
    allowed_domains = ['glassdoor.com']

    def start_requests(self):
        start_urls = []
        for page in range(1, int(pages) + 1):
            url = 'https://glassdoor.ca/Job/us-' + jobtitle + '-jobs-SRCH_IL.0,2_' \
                                                              'IN1_KO3,15_IP' + str(page) + '.htm'
            start_urls.append(url)
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_d)

    def parse_d(self, response):
        item = GlassdoorItem()
        pattern = re.compile("'\d{10}'\s")
        matches = pattern.findall(response.body.decode('utf-8'))

        jobIds = []

        for match in matches:
            match = re.sub(r'[^\d]', '', match)

            jobIds.append(match)
        jobIds = list(set(jobIds))  # remove dupulicate value

        for id in jobIds:
            next_url = "https://www.glassdoor.ca/Job/json/details.htm?&jobListingId=" + id
            req = urllib.request.Request(next_url,
                                         headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x"
                                                                "64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                "Chrome/77.0.3865.120 Safari/537.36"})
            con = urllib.request.urlopen(req)
            string = con.read().decode("utf-8")
            stringtojson = json.loads(string)
            try:
                title = stringtojson["gaTrackerData"]["jobTitle"]
                empname = stringtojson["gaTrackerData"]["empName"]
                location = stringtojson["header"]["location"]
                size = stringtojson["gaTrackerData"]["empSize"]
                salarylow = stringtojson["header"]["salaryLow"]
                salaryhigh = stringtojson["header"]["salaryHigh"]
                jobId = stringtojson["gaTrackerData"]["jobId"]
                year = stringtojson["overview"]["foundedYear"]
                rating = stringtojson["header"]["rating"]
                item['title'] = title
                item['empname'] = empname
                item['location'] = location
                item['size'] = size
                item['salarylow'] = salarylow
                item['salaryhigh'] = salaryhigh
                item['jobId'] = jobId
                item['year'] = year
                item['rating'] = rating
                yield item
            except:
                continue

