import csv
from esg_score import ESGScoreScraper
from google_finance_api import CDPScoreScraper
from tqdm import tqdm
import os



encoding_mapping = {
    '-': 0,
    'F-': 1,
    'F': 2,
    'E-': 3,
    'E': 4,
    'D-': 5,
    'D': 6,
    'C-': 7,
    'C': 8,
    'B-': 9,
    'B': 10,
    'A-': 11,
    'A': 12
}

class Company:
    def __init__(self, ticker, name):
        self.ticker = ticker
        self.name = name
        self.esg_score = None
        self.env_score = None
        self.social_score = None
        self.governance_score = None
        self.controversy_level = None
        self.climate_score = None
        self.sustainability_score = None
        self.title = None
        self.quote = None
        self.current_price = None
        self.day_range = None
        self.year_range = None
        self.market_cap = None
        self.revenue = None
        self.website = None
        self.net_income = None
        self.news1 = None
        self.news2 = None

    def write_company_to_csv(self):
        with open('scores.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            t = []
            if self.esg_score:
                t.append(self.esg_score)
            else:
                t.append(0)
            if self.env_score:
                t.append(self.env_score)
            else:
                t.append(0)
            if self.social_score:
                t.append(self.social_score)
            else:
                t.append(0)
            if self.governance_score:
                t.append(self.governance_score)
            else:
                t.append(0)
            if self.controversy_level:
                t.append(self.controversy_level)
            else:
                t.append(0)
            if self.climate_score:
                t.append(self.climate_score)
            else:
                t.append('-')
            t.append(self.sustainability_score)
            if self.title:
                t.append(self.title)
            else:
                t.append('-')
            if self.quote:
                t.append(self.quote)
            else:
                t.append('-')
            if self.current_price:
                t.append(self.current_price)
            else:
                t.append('NaN')
            if self.day_range:
                t.append(self.day_range)
            else:
                t.append('-')
            if self.year_range:
                t.append(self.year_range)
            else:
                t.append('-')
            if self.market_cap:
                t.append(self.market_cap)
            else:
                t.append('NaN')
            if self.revenue:
                t.append(self.revenue)
            else:
                t.append('NaN')
            if self.website:
                t.append(self.website)
            else:
                t.append('-')
            if self.net_income:
                t.append(self.net_income)
            else:
                t.append('NaN')
            if self.news1:
                t.append(self.news1)
            else:
                t.append('-')
            if self.news2:
                t.append(self.news2)
            else:
                t.append('-')
            spamwriter.writerow([self.ticker, self.name]+t)

    def calculate_score(self):
        esg = int(self.esg_score) if self.esg_score else 0
        ctl = int(self.controversy_level) if self.controversy_level else 0
        cdp = self.climate_score if self.climate_score else '-'
        cdp = encoding_mapping[cdp]

        n_esg = (esg - 0)/(100 - 0)
        n_ctl = (ctl - 0)/(5 - 0)
        n_cdp = (cdp - 0)/(12 - 0)

        self.sustainability_score = (n_esg + n_ctl + n_cdp)*100//3


file_path = "scores.csv"

if os.path.exists(file_path):
    os.remove(file_path)

with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Ticker","Company","ESG Risk score","Environment Risk Score","Social Risk Score","Governance Risk Score","Controversy Level","CDP Score", "Sustainability Score", "title",
            "quote", "current_price", "day_range", "year_range", "market_cap", "revenue", "website", "net_income",
            "news1", "news2"])

print("----------------------- Generating Sustainability Score for S&P 500  -----------------------")

# Define the CSV file path
csv_file_path = 'sp500_companies.csv'

# Create an instance of the ESGScoreScraper class
esg_scraper = ESGScoreScraper()
cdp_scraper = CDPScoreScraper()

# Open the CSV file and read data line by line
try:
    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if it exists

        for row in tqdm(csv_reader, desc="Processing"):
            if len(row) >= 2:
                company = Company(row[0], row[1])
                esg_score = esg_scraper.get_esg_score(company.ticker)
                company.esg_score = esg_score[0]
                company.env_score = esg_score[1]
                company.social_score = esg_score[2]
                company.governance_score = esg_score[3]
                company.controversy_level = esg_score[4]
                aboutCompany = cdp_scraper.get_cdp_score(company.ticker)
                if aboutCompany != None:
                    if aboutCompany.get("cdp") and len(aboutCompany.get("cdp")) > 0:
                        company.climate_score = aboutCompany.get("cdp")[0] 
                    company.title = aboutCompany.get("title")
                    # print(company.title)
                    company.quote = aboutCompany.get("quote")
                    company.current_price = aboutCompany.get("current_price")
                    company.day_range = aboutCompany.get("day_range")
                    company.year_range = aboutCompany.get("year_range")
                    company.market_cap = aboutCompany.get("market_cap")
                    company.revenue = aboutCompany.get("revenue")
                    company.website = aboutCompany.get("website")
                    company.net_income = aboutCompany.get("net_income")
                    sizeOfNews = len(aboutCompany.get("news").get("items"))
                    # print(len(aboutCompany.get("news").get("items")))
                    if(sizeOfNews >= 2):
                        company.news1 = aboutCompany.get("news").get("items")[0].get("link")
                        company.news2 = aboutCompany.get("news").get("items")[1].get("link")
                    elif(sizeOfNews == 1):
                        company.news1 = aboutCompany.get("news").get("items")[0].get("link")
                company.calculate_score()
                company.write_company_to_csv()

finally:
    # Close the ESGScoreScraper
    esg_scraper.close()

print("----------------------- Done Generating Sustainability Score for S&P 500!  -----------------------")
