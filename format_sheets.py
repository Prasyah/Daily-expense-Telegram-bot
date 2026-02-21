"""
Script to format column E (Amount) as Rupiah currency in all existing sheets
Run this once to fix formatting for all past sheets
"""

import core

# Get all worksheets in the spreadsheet
worksheets = core.spreadsheet.worksheets()

print(f"Found {len(worksheets)} worksheets")

for sheet in worksheets:
    try:
        core.format_column_E(sheet)
        print(f"✓ Formatted {sheet.title}")
    except Exception as e:
        print(f"✗ Error formatting {sheet.title}: {e}")

print("\nDone! All sheets formatted.")
