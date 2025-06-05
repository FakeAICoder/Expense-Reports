# Expense Report PDF Importer

This simple command line tool parses expense information from PDF files and can
either create expense reports in SAP Concur using their REST API or export the
data to CSV for manual import.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. To upload reports automatically you must obtain SAP Concur API credentials and a refresh token.

## Usage

Run the script with your credentials and a PDF file containing expenses:

```bash
python expense_report_app.py receipt.pdf \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET \
  --refresh-token YOUR_REFRESH_TOKEN
```

If you do not have Concur API credentials, you can export the parsed expenses
to a CSV file instead and then import that file manually through Concur's web
interface:

```bash
python expense_report_app.py receipt.pdf --csv-output expenses.csv
```

The script extracts simple line items from the PDF. By default the entries are
sent directly to Concur if credentials are provided. When using `--csv-output`
no network requests are made and a CSV file is produced instead.

> **Note**: The PDF parsing relies on a naive regular expression and may need to
> be adjusted for your receipt format.
