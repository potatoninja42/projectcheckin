#Victoria Abreu
#Programming for IT
#Cis153
#00332297
#Final Project

import tkinter as tk
from tkinter import filedialog
import os
import pdfplumber
import re

def extract_text_with_pdfplumber(pdf_path):
    text = '' # Create an empty text variable to store extracted text
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text
# Return all the text extracted from the PDF

def find_name(text):
     # Use a regular expression to search for a name pattern
    name_match = re.search(r'Name:\s*(\w+ \w+)', text)
    return name_match.group(1) if name_match else None

def find_courier_id(text):
    # Regular expression to match the Courier ID
    courier_id_match = re.search(r'Courier ID:\s*(\d+)', text)
    # Extract the Courier ID if found
    return courier_id_match.group(1) if courier_id_match else None

def find_addresses(text):
    # Create a dictionary to store addresses
    addresses_per_day = {}
    # Create a variable to keep track of the current date
    current_date = None
    
    # Updated regex pattern to capture the second address in each line
    address_pattern = re.compile(r'200 FALLON RD STONEHAM MA \d{5}-\d{4}(.+?MA \d{5}-\d{4})')
    
 # Split the text into lines and check each line
    for line in text.split('\n'):
        # Check for date
        date_match = re.match(r'(\d{2}/\d{2}/\d{4})', line)
        if date_match:
            current_date = date_match.group(1) # Store the current date
            addresses_per_day[current_date] = []
            continue
        
        # If we have a current date, check for addresses
        if current_date:
            address_matches = address_pattern.findall(line)
            for address in address_matches:
                cleaned_address = address.strip() # Clean up the address by removing extra spaces
                addresses_per_day[current_date].append(cleaned_address)
            
    return addresses_per_day

def export_addresses_to_txt(addresses_per_day, responsible_person, courier_id, text_path):
    with open(text_path, 'w') as file:
        if responsible_person:
            file.write(f"Responsible Person: {responsible_person}\n")
        if courier_id:
            file.write(f"Courier ID: {courier_id}\n\n")
        for date, addresses in addresses_per_day.items():
              # Write each date to the file
            file.write(f"Date: {date}\n")
            for address in addresses:
                 # Write each address associated with the date to the file
                file.write(f"{address}\n")
                # Write the total number of addresses for the date to the file
            file.write(f"Total addresses for {date}: {len(addresses)}\n\n")

def main(pdf_path, output_path):
    extracted_text = extract_text_with_pdfplumber(pdf_path)
    responsible_person = find_name(extracted_text)
    courier_id = find_courier_id(extracted_text)
    addresses_per_day = find_addresses(extracted_text)
    export_addresses_to_txt(addresses_per_day, responsible_person, courier_id, output_path)
    print(f"Processed: {os.path.basename(pdf_path)}")

def run_script():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    if pdf_path and output_path:
        main(pdf_path, output_path)
        status_label.config(text=f"Processed: {os.path.basename(pdf_path)}")
    else:
        status_label.config(text="Operation cancelled or file not selected.")

# GUI Setup
root = tk.Tk()
root.title("PDF Address Extractor")

run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack(pady=20)

status_label = tk.Label(root, text="Select a PDF file to process")
status_label.pack(pady=10)

root.mainloop()
