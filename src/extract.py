import pandas as pd
def extract_csv(extracted_data_path):
    extract_results = pd.read_csv(extracted_data_path)
    return extract_results