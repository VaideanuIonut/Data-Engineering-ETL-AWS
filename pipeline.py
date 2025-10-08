import requests
import json
import os
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# GitHub API Endpoint 
API_URL = "https://api.github.com/users/octocat"

# Folder for saving raw data
DATA_FOLDER = "data"

def extract_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR during data extraction: {e}")
        return None

def save_raw_data(data, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(folder, f"raw_data_{timestamp}.json")
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"SUCCESS: Raw data saved to {file_path}")
    return file_path

def transform_json_to_dataframe(json_data):
    if not json_data:
        return None
    
    df = pd.DataFrame([json_data])
    
   
    df = df[['login', 'id', 'name', 'email', 'company', 'location', 'followers', 'public_repos', 'created_at']]
    
    
    df['created_at'] = pd.to_datetime(df['created_at']).dt.date


    df = df.fillna('N/A')
    
    return df

def validate_data(df):
    if df is None or df.empty:
        print("ERROR: DataFrame is empty or invalid.")
        return False
    
 
    if df.isnull().sum().sum() > 0:
        print("WARNING: Data still contains missing values after initial cleanup.")
        return False
    
    print("VALIDATION SUCCESS: Data is clean and ready for loading.")
    return True

def load_data_to_sql(df):
    """
    NOTE FOR GITHUB: Replace these placeholder values with your actual AWS RDS credentials
    """
    DB_DETAILS = {
        'host': 'ENDPOINT from AWS - Connectivity & security', 
        'database': 'postgres',                                                       
        'user': 'db_username',                                                   
        'password': 'PASSWORD',                                           
        'port': '5432' 
    }
    
    
    engine_string = f"postgresql+psycopg2://{DB_DETAILS['user']}:{DB_DETAILS['password']}@{DB_DETAILS['host']}:{DB_DETAILS['port']}/{DB_DETAILS['database']}"
    
    try:
        
        engine = create_engine(engine_string)
        
       
        df.to_sql(
            'github_users',          
            engine,                  
            if_exists='replace',     
            index=False              
        )
        print("LOAD SUCCESS: Data successfully moved to 'github_users' table on AWS RDS.")
        
    except Exception as e:
        print(f"ERROR during database loading: {e}")


if __name__ == "__main__":
    raw_data = extract_data(API_URL)
    
    if raw_data:
        
        save_raw_data(raw_data, DATA_FOLDER)

        
        df = transform_json_to_dataframe(raw_data)
        
        
        if validate_data(df):
            print("\nFinal DataFrame is ready. First rows:")
            print(df.head())
            
            
            load_data_to_sql(df) 
        
    else:
        print("Data extraction failed. Pipeline halted.")