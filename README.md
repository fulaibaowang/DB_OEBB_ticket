# Train Ticket PDF Extractor (DB Deutsche Bahn, ÖBB Österreichische Bundesbahnen)

A Python script to extract travel information from train ticket PDFs stored in a folder and save the results into a summarized Excel file. This tool is especially useful for automating the processing of Deutsche Bahn or ÖBB tickets.

## Usage
```
python DB.py -d <folder_path> -o <output_file>
```
eg.
```
python DB.py -d ./train_tickets -o tickets_summary.xlsx
```

## Features

- Extracts key travel information such as:
  - **Travel Date**
  - **Train Information**
  - **Cost**
  - **Booking Reference (Auftragsnummer)**
- Processes all PDF files in a specified folder.
- Outputs the extracted information into an Excel file, e.g `tickets_summary.xlsx`.

## Requirements

The script requires the following Python packages:

- `pdfplumber`
- `pandas`
- `openpyxl`

## old version DB tickets (before 2024)

Use `DB_old.py` for old version tickets

```
python DB_old.py -d <folder_path> -o <output_file>
```

## ÖBB tickets 

```
python Oebb.py -d <folder_path> -o <output_file>
```

## docker
```
 MSYS_NO_PATHCONV=1 docker run -it -v /c/Users/freed/develop/DB_OEBB_ticket:/workdir fulaibaowang/dbticket:1.0.0 python DB_OEBB_ticket/DB.py -d /workdir/new_ticket -o /workdir/test.xlsx
```

[dockerfile](https://github.com/fulaibaowang/docker_images/tree/main/dbticket/1.0.0)