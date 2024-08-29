import pandas as pd
from flask import Flask, render_template, request
import os

# Loading the datasets
sp500_dataset_path = 'sp500_companies.csv'
scores_dataset_path = 'scores.csv'

# Loading both datasets and checking their columns
sp500_df = pd.read_csv(sp500_dataset_path)
scores_df = pd.read_csv(scores_dataset_path)

# Print columns to verify the existence of the 'Ticker' column
print("S&P 500 DataFrame columns:", sp500_df.columns)
print("Scores DataFrame columns:", scores_df.columns)

# Rename the necessary columns in sp500_df to match with scores_df
# Assuming 'MMM' is the Ticker column and '3M' is the Company column
sp500_df.rename(columns={'MMM': 'Ticker', '3M': 'Company'}, inplace=True)

# Check if the rename was successful
print("Renamed S&P 500 DataFrame columns:", sp500_df.columns)

# Merge the DataFrames on the 'Ticker' column
merged_df = pd.merge(sp500_df, scores_df, how='left', on='Ticker')

# Check if the merge was successful
print("Merged DataFrame columns:", merged_df.columns)
print("Sample of merged DataFrame:", merged_df.head())

# Flask application setup
app = Flask(__name__)

@app.route('/')
def index():
    # Print the path Flask is using to look for templates
    print("Template path:", os.path.join(app.root_path, 'templates'))
    
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    ticker = request.form.get('ticker').upper()
    print(f"Received ticker: {ticker}")
    
    # Query the dataset for the given ticker
    company_data = merged_df[merged_df['Ticker'] == ticker]

    # Check if the ticker exists in the dataset
    if company_data.empty:
        return f"Error: No data is available for ticker {ticker}. Please check the ticker symbol and try again."

    # Extract the relevant data using the correct column names
    company_name = company_data.iloc[0]['Company_x']  # Use Company_x or Company_y depending on which one you want
    esg_score = company_data.iloc[0]['ESG Risk score']
    environment_score = company_data.iloc[0]['Environment Risk Score']
    social_score = company_data.iloc[0]['Social Risk Score']
    governance_score = company_data.iloc[0]['Governance Risk Score']
    controversy_level = company_data.iloc[0]['Controversy Level']
    cdp_score = company_data.iloc[0]['CDP Score']
    sustainability_score = company_data.iloc[0]['Sustainability Score']

    # Prepare the data to send to the template
    esg_data = [esg_score, environment_score, social_score, governance_score, controversy_level, sustainability_score]
    cdp_data = {
        "cdp_score": cdp_score,
        "company_name": company_name
    }

    # Render the results page
    return render_template('result.html', ticker=ticker, esg_data=esg_data, cdp_data=cdp_data)
