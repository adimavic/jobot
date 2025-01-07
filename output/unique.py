import pandas as pd

# Load the Excel files
old_data = pd.read_excel("old.xlsx")
new_data = pd.read_excel("new.xlsx")

# Assuming the email column is named "Email"
old_emails = set(old_data['Email'])
new_emails = set(new_data['Email'])

# Find emails in new.xlsx that are not in old.xlsx
unique_emails = new_emails - old_emails

# Convert to a DataFrame for saving or display
unique_emails_df = pd.DataFrame(list(unique_emails), columns=["Email"])

# Save the result to a new Excel file
unique_emails_df.to_excel("unique.xlsx", index=False)

print(f"Unique emails saved to 'unique.xlsx'.")
