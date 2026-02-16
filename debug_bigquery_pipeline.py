
import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from app.sub_agents.technical_analyst.tools import download_data
from app.sub_agents.oracle_predictor.signal_processing import prepare_for_timesfm

# Force Env Vars for Debug
os.environ["GOOGLE_CLOUD_PROJECT"] = "custom-ground-482813-s7"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["BQ_DATASET"] = "trademate_ml"

def debug_pipeline(ticker="NVDA"):
    print(f"\n--- 1. DATA FETCH ({ticker}) ---")
    try:
        df = download_data(ticker, period="1y")
        print(f"Success! Shape: {df.shape}")
        print(df.tail(3)[['Close']])
    except Exception as e:
        print(f"FAIL: {e}")
        return

    print(f"\n--- 2. PREPROCESSING ---")
    processed_df = prepare_for_timesfm(df)
    
    # CRITICAL: We want to inspect what we are sending.
    # Changing hypothesis: Let's Inspect 'Clean_Close' vs 'Log_Returns'
    print(processed_df[['Close', 'Clean_Close', 'Log_Returns']].tail(5))

    # Prepare Context schema
    # IMPORTANT: We are going to test sending CLEAN_CLOSE (Raw Prices) instead of Log Returns 
    # to see if the model behaves better.
    context_df = processed_df.reset_index()[['Date', 'Clean_Close']]
    context_df.columns = ['time_series_timestamp', 'time_series_data'] # Standard BQML Names
    context_df['time_series_id'] = ticker
    
    print(f"\n--- 3. BQ UPLOAD PAYLOAD (First 3 Rows) ---")
    print(context_df.head(3))
    print(f"--- 3. BQ UPLOAD PAYLOAD (Last 3 Rows) ---")
    print(context_df.tail(3))
    
    print(f"\n--- 4. BIGQUERY CONNECTION ---")
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    dataset_id = os.environ["BQ_DATASET"]
    table_id = f"{project_id}.{dataset_id}.debug_oracle_{ticker}"
    
    client = bigquery.Client(project=project_id, location="us-central1")
    
    print(f"Uploading to {table_id}...")
    try:
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        job = client.load_table_from_dataframe(context_df, table_id, job_config=job_config)
        job.result()
        print("Upload Successful.")
    except Exception as e:
        print(f"UPLOAD FAILED: {e}")
        return

    print(f"\n--- 5. FORECAST EXECUTION (TimesFM 2.5) ---")
    # Using the strict AI.FORECAST syntax
    query = f"""
        SELECT *
        FROM AI.FORECAST(
            TABLE `{table_id}`,
            data_col => 'time_series_data',
            timestamp_col => 'time_series_timestamp',
            id_cols => ['time_series_id'],
            model => 'timesfm-2.5',
            horizon => 14,
            confidence_level => 0.8
        )
    """
    
    print("Sending Query...")
    try:
        query_job = client.query(query)
        res_df = query_job.to_dataframe()
        print("\n--- 6. RAW RESULT ---")
        print(res_df)
    except Exception as e:
        print(f"\nQUERY FAILED: {e}")
        if "bit.ly" in str(e) or "Not found" in str(e):
            print("\nHINT: The error suggests 'timesfm-2.5' model name is not recognized in this region OR API is not enabled.")

if __name__ == "__main__":
    debug_pipeline()
