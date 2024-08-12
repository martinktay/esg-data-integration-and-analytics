import pandas as pd

# Encoding mapping for CDP scores
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

# Define the Company class
class Company:
    def __init__(self, ticker, name, esg_score=None, env_score=None, social_score=None, governance_score=None, controversy_level=None, climate_score=None):
        self.ticker = ticker
        self.name = name
        self.esg_score = esg_score
        self.env_score = env_score
        self.social_score = social_score
        self.governance_score = governance_score
        self.controversy_level = controversy_level
        self.climate_score = climate_score
        self.sustainability_score = None

    def calculate_score(self):
        esg = float(self.esg_score) if pd.notna(self.esg_score) else 0
        ctl = float(self.controversy_level) if pd.notna(self.controversy_level) else 0
        cdp = self.climate_score if pd.notna(self.climate_score) else '-'
        cdp = encoding_mapping[cdp]

        n_esg = (esg - 0) / (100 - 0)
        n_ctl = (ctl - 0) / (5 - 0)
        n_cdp = (cdp - 0) / (12 - 0)

        self.sustainability_score = (n_esg + n_ctl + n_cdp) * 100 // 3

    def display(self):
        print(f"Company Name: {self.name}")
        print(f"ESG Score: {self.esg_score}")
        print(f"Environment Score: {self.env_score}")
        print(f"Social Score: {self.social_score}")
        print(f"Governance Score: {self.governance_score}")
        print(f"Controversy Level: {self.controversy_level}")
        print(f"Sustainability Score: {self.sustainability_score}")
        print(f"CDP Score: {self.climate_score}")

# Load the datasets
sp500_path = 'sp500_companies.csv'
scores_path = 'scores.csv'

try:
    sp500_df = pd.read_csv(sp500_path)
    scores_df = pd.read_csv(scores_path)
    print("Datasets loaded successfully")
except FileNotFoundError as e:
    print(f"File not found: {e.filename}")
    exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

# Merge the datasets if necessary, or just work with the relevant data
# Assuming that 'ticker' is the linking key
merged_df = pd.merge(sp500_df, scores_df, how='left', left_on='Ticker', right_on='Ticker')

# Process the dataset
for index, row in merged_df.iterrows():
    company = Company(
        ticker=row['Ticker'],  # Adjusted to match the actual column name
        name=row['Company'],  # Adjusted to match the actual column name
        esg_score=row['ESG Risk score'],
        env_score=row['Environment Risk Score'],
        social_score=row['Social Risk Score'],
        governance_score=row['Governance Risk Score'],
        controversy_level=row['Controversy Level'],
        climate_score=row['CDP Score']
    )
    company.calculate_score()
    company.display()
