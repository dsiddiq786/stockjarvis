import os
import pandas as pd

""" 
    Step No 1:  (Clean the Dataset)
    Author : Dawood Siddiq
    Description : Remove Duplicate Rows and keep the last one from all provided datasets
"""

# Function to clean and save the CSV files
def clean_csv_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    csv_files = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

    for file in csv_files:
        df = pd.read_csv(os.path.join(input_folder, file))

        df.drop_duplicates(subset='Time', keep='last', inplace=True)

        output_path = os.path.join(output_folder, f"cleaned_{file}")
        df.to_csv(output_path, index=False)

input_folder_path = './data'
output_folder_path = './cleaned_data'

clean_csv_files(input_folder_path, output_folder_path)
