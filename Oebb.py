#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pdfplumber
import re
import pandas as pd
import os
import argparse


def extract_ticket_info_from_folder(folder_path, output_file):
    data = []
    
    # Loop through all PDF files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):  # Process only PDF files
            pdf_path = os.path.join(folder_path, file_name)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        # Extract travel date
                        travel_date_match = re.search(r'\nHF (\d{2}.\d{2}.\d{2})\nDATUM', text)
                        travel_date = travel_date_match.group(1) if travel_date_match else 'N/A'

                        # Extract train information
                        train_match = re.search(r'DATUM ZEIT VON -> NACH DATUM ZEIT KLASSE\n\d{2}\.\d{2} \d{2}:\d{2} (.*?) -> (.*?) \d{2}\.\d{2} \d{2}:\d{2}', text, re.DOTALL)
                        departure = train_match.group(1).strip() if train_match else 'N/A'
                        destination = train_match.group(2).strip() if train_match else 'N/A'

                        # Extract cost
                        cost_match = re.search(r'\nPREIS EUR (.*?)\nZug', text, re.DOTALL)
                        cost = cost_match.group(1).strip() if cost_match else 'N/A'

                        # Append extracted info to the data list
                        data.append({
                            'Travel Date': travel_date,
                            'Departure': departure,
                            'Destination': destination,
                            'Cost (€)': cost,
                            'File Name': file_name  # Include file name for traceability
                        })

    # Convert the data into a DataFrame
    df = pd.DataFrame(data, columns=['Travel Date', 'Departure','Destination', 'Cost (€)', 'File Name'])

    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False)
    return df


if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract train ticket info from PDF files in a folder.")
    parser.add_argument('-d', '--directory', required=True, help='Path to the folder containing PDF files')
    parser.add_argument('-o', '--output', required=True, help='Path to the output Excel file')
    
    args = parser.parse_args()

    # Call the extraction function with command-line arguments
    extract_ticket_info_from_folder(args.directory, args.output)






