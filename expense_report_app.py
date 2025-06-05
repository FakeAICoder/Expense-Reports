import re
import csv
import json
from dataclasses import dataclass
from typing import List, Optional

import pdfplumber
import requests


@dataclass
class ExpenseItem:
    vendor: str
    date: str
    amount: float
    description: Optional[str] = None


class ConcurClient:
    """Simple SAP Concur API client."""

    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.base_url = "https://us.api.concursolutions.com"
        self.access_token: Optional[str] = None

    def authenticate(self) -> None:
        """Retrieve an access token using the refresh token flow."""
        token_url = f"{self.base_url}/oauth2/v0/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        resp = requests.post(token_url, data=data)
        resp.raise_for_status()
        self.access_token = resp.json().get("access_token")

    def post_report(self, report_data: dict) -> dict:
        """Create a report in Concur."""
        if not self.access_token:
            self.authenticate()
        url = f"{self.base_url}/expense/reports/v3/reports"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        resp = requests.post(url, headers=headers, json=report_data)
        resp.raise_for_status()
        return resp.json()


def parse_expense_items(pdf_path: str) -> List[ExpenseItem]:
    """Parse simple expense items from a PDF."""
    items: List[ExpenseItem] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                match = re.search(r"(?P<date>\d{2}/\d{2}/\d{4})\s+(?P<vendor>[A-Za-z ]+)\s+\$(?P<amount>\d+\.\d{2})", line)
                if match:
                    items.append(
                        ExpenseItem(
                            vendor=match.group("vendor").strip(),
                            date=match.group("date"),
                            amount=float(match.group("amount")),
                            description=None,
                        )
                    )
    return items


def create_expense_report(pdf_path: str, client: ConcurClient) -> None:
    """Extract items from a PDF and create a report in Concur."""
    items = parse_expense_items(pdf_path)
    entries = [
        {
            "transaction-date": item.date,
            "vendor-description": item.vendor,
            "transaction-amount": {
                "amount": item.amount,
                "currency-code": "USD",
            },
            "comment": item.description or "Imported from PDF",
        }
        for item in items
    ]
    report_data = {
        "report-name": f"Imported Expenses {pdf_path}",
        "entries": entries,
    }
    response = client.post_report(report_data)
    print(json.dumps(response, indent=2))


def export_csv(pdf_path: str, csv_path: str) -> None:
    """Extract items from a PDF and write them to a CSV file."""
    items = parse_expense_items(pdf_path)
    with open(csv_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Date", "Vendor", "Amount", "Description"])
        for item in items:
            writer.writerow([item.date, item.vendor, f"{item.amount:.2f}", item.description or ""])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create Concur expense reports from PDFs")
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("--client-id")
    parser.add_argument("--client-secret")
    parser.add_argument("--refresh-token")
    parser.add_argument("--csv-output", help="Path to CSV file instead of Concur upload")
    args = parser.parse_args()

    if args.csv_output:
        export_csv(args.pdf, args.csv_output)
    else:
        if not (args.client_id and args.client_secret and args.refresh_token):
            raise SystemExit("Concur credentials are required unless --csv-output is used")
        client = ConcurClient(args.client_id, args.client_secret, args.refresh_token)
        create_expense_report(args.pdf, client)
