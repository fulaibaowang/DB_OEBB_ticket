#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
                        travel_date_match = re.search(r'\nGültigkeit: (\d{2}.\d{2}.\d{4}) 00:00 Uhr', text)
                        travel_date = travel_date_match.group(1) if travel_date_match else 'N/A'

                        # Extract train information
                        train_match = re.search(r'\nEinfache Fahrt (.*?)\nVia:', text, re.DOTALL)
                        train = train_match.group(1).strip() if train_match else 'N/A'

                        # Extract cost
                        cost_match = re.search(r'\nGesamtpreis (.*?)€', text, re.DOTALL)
                        cost = cost_match.group(1).strip() if cost_match else 'N/A'

                        # Extract Auftragsnummer
                        auftragsnummer_match = re.search(r'\nAuftragsnummer: (.*?)\nIhre', text)
                        auftragsnummer = auftragsnummer_match.group(1).strip() if auftragsnummer_match else 'N/A'

                        # Append extracted info to the data list
                        data.append({
                            'Travel Date': travel_date,
                            'Train': train,
                            'Cost (€)': cost,
                            'Auftragsnummer': auftragsnummer,
                            'File Name': file_name  # Include file name for traceability
                        })

    # Convert the data into a DataFrame
    df = pd.DataFrame(data, columns=['Travel Date', 'Train', 'Cost (€)', 'Auftragsnummer', 'File Name'])

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




