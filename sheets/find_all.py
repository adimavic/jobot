import os
import pandas as pd
import re

# Function to extract emails from a given text
def extract_emails(text):
    if isinstance(text, str):
        # Regular expression to find email addresses
        return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return []

# Initialize an empty set to store unique emails
unique_emails = set()

# Get the current directory
current_dir = os.getcwd()

# Iterate over all files in the current directory
for file in os.listdir(current_dir):
    # Check if the file is an Excel file
    if file.endswith(('.xls', '.xlsx')):
        # Read the Excel file
        try:
            df = pd.read_excel(file, sheet_name=None)  # Read all sheets
            for sheet_name, sheet_df in df.items():
                # Apply the extract_emails function to each cell and update the unique_emails set
                sheet_emails = sheet_df.applymap(extract_emails).values.flatten()
                for email_list in sheet_emails:
                    unique_emails.update(email_list)
        except Exception as e:
            print(f"Error reading {file}: {e}")

# Convert the set to a sorted list
unique_emails = sorted(unique_emails)

# Create a DataFrame from the list of unique emails
email_df = pd.DataFrame(unique_emails, columns=['Email'])

# Write the DataFrame to a new Excel file
output_file = 'consolidated_unique_emails.xlsx'
email_df.to_excel(output_file, index=False)

print(f"Consolidated file '{output_file}' created with {len(unique_emails)} unique email addresses.")
