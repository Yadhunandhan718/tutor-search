# Tutor-Ward Index

A Python-based application that searches an Excel spreadsheet containing
tutor and student information.

## Features

- Search for tutors and retrieve information about their wards.
- Search for students using their registration numbers.
- Search for students by name.
- Web interface built using HTML, CSS, JavaScript, and Flask.

## Requirements

- Python 3
- pandas
- Flask
- RapidFuzz
- openpyxl

Install the required libraries using pip:

    pip install pandas flask rapidfuzz openpyxl

## Setup

### 1. Obtain the Excel workbook

The original Excel workbook is not included in this repository because
it contains private data.

Obtain an authorized copy of the workbook separately.

### 2. Configure the workbook

Place the Excel workbook in the project's root directory (the directory
containing app.py).

Open app.py and update the EXCEL_FILE variable to match your workbook's
filename.

For example:

    EXCEL_FILE = "tw-details.xlsx"

### 3. Verify the workbook structure

The application expects the Excel workbook to follow a specific format.

The relevant columns include:

| Tutor Name | Roll No | Name | Registration No |
| ---------- | ------- | ---- | --------------- |
| ABC        | 789     | JAM  | 1234            |

The example above is illustrative. Ensure that your workbook's column
names and sheet structure match the expectations of the application.

### 4. Run the application

From the project's root directory, run:

    python3 app.py

Open the local address printed by Flask in your browser.

## Notes

- Do not commit the original Excel workbook to the repository.
- Ensure that the workbook is formatted correctly before running the
  application.