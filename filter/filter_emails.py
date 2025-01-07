import os
import pandas as pd
import re

# Function to extract emails from a given text
def extract_emails(text):
    if isinstance(text, str):
        # Regular expression to find email addresses
        return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return []

# Function to filter out unwanted emails
def filter_emails(email):
    # Define unwanted patterns
    unwanted_patterns = [
        r'support', r'service', r'example', r'info', r'noreply',r'privacy',r'name',r'abc',r'xyz',r'jo',r'test',r'resumeworded',
        r'admin', r'contact', r'help', r'feedback', r'sales', r'press',r'complaints',r'mailer',r'payment',r'collection',r'helpdesk',r'john',r'unsubscribe',r'firstname'
    ]
    # Define valid domain extensions
    valid_extensions = ['com', 'org', 'net', 'edu', 'gov', 'co', 'in','technology']

    # Check if the email contains any of the unwanted patterns
    for pattern in unwanted_patterns:
        if re.search(pattern, email, re.IGNORECASE):
            return False

    # Check if the email has a valid domain extension
    domain_extension = email.split('.')[-1].lower()
    if domain_extension not in valid_extensions:
        return False

    # Remove emails with prefixes like "to%3A"
    if '%3A' in email or email.startswith(('to:', 'cc:')):
        return False

    # Remove generic emails with "name@mail.com", "name@domain.com"
    if re.match(r'^(name|your|test)[@]', email, re.IGNORECASE):
        return False

    # Remove hashed or auto-generated emails
    if re.match(r'^[a-f0-9]{32}@', email):  # Detect MD5-like hashes
        return False

    return True

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
                    for email in email_list:
                        if filter_emails(email):  # Filter emails before adding
                            unique_emails.add(email)
        except Exception as e:
            print(f"Error reading {file}: {e}")

# Convert the set to a sorted list
unique_emails = sorted(unique_emails)

# Create a DataFrame from the list of unique emails
email_df = pd.DataFrame(unique_emails, columns=['Email'])

# Write the DataFrame to a new Excel file
output_file = 'validated_unique_emails22.xlsx'
email_df.to_excel(output_file, index=False)

print(f"Validated file '{output_file}' created with {len(unique_emails)} unique and valid email addresses.")
