import re
import csv
from collections import defaultdict
from pathlib import Path

# Define input and output files
input_file = Path("whatsapp_students_registration.txt")
output_file = Path("parsed_students.csv")

# Field normalization mapping
field_name_mapping = {
    'mobile#': 'Mobile#',
    'mobile': 'Mobile#',
    'whatsapp#': 'WhatsApp#',
    'whatsaap': 'WhatsApp#',
    'email': 'Email Address',
    'email address': 'Email Address',
    'full name': 'Full Name',
    'student id': 'Student ID#',
    'student id#': 'Student ID#',
    'batch': 'Batch#',
    'batch#': 'Batch#',
    'gender': 'Gender',
}

# Desired column order
output_headers = [
    'Full Name', 'Mobile#', 'WhatsApp#', 'Area/Locality', 'City', 'District', 'State',
    'Area/Locality_2', 'Mandal', 'City_2', 'State_2', 'Age', 'Qualification', 'Profession', 'Email Address',
    'Full Name_2', 'Mobile#_2', 'Student ID#', 'Batch#',
]

# Fields for formatting
camel_case_fields = {'Full Name', 'City', 'Area/Locality', 'District', 'State', 'Mandal', 'Profession'}
uppercase_fields = {'Student ID#', 'Batch#'}
number_fields = {'Mobile#', 'WhatsApp#', 'Mobile#_2'}
def to_camel_case(text):
    return ' '.join(word.capitalize() for word in text.split())

def normalize_fieldname(field):
    return field_name_mapping.get(field.lower().strip(), field.strip())

def clean_value(field, value):
    value = value.strip()
    norm_field = normalize_fieldname(field)
    if norm_field in number_fields:
        # Remove spaces and country codes like +91, 91, +966, 966
        value = re.sub(r'\s+', '', value)
        value = re.sub(r'^\+?(91|966|1)', '', value)

    if norm_field in camel_case_fields:
        return to_camel_case(value)
    if norm_field in uppercase_fields:
        return value.upper()
    return value.strip()

def parse_input(text):
    entries = []
    current_entry = defaultdict(str)
    for line in text.splitlines():
        line = line.strip()

        # Skip irrelevant lines
        if re.match(r'^\[\d{1,2}:\d{2}, \d{1,2}/\d{1,2}/\d{4}\] \+91 \d{5,}$', line) or not line or line.startswith('='):
            continue

        # New entry separator
        if line.startswith('[') and ']' in line and '+91' in line:
            if current_entry:
                entries.append(current_entry)
                current_entry = defaultdict(str)
            continue

        # Extract key-value pair
        if ':' in line:
            parts = line.split(':', 1)
            field = normalize_fieldname(parts[0])
            value = clean_value(field, parts[1])
            if not current_entry[field]:
                current_entry[field] = value
            else:
                i = 2
                while f"{field}_{i}" in current_entry:
                    i += 1
                current_entry[f"{field}_{i}"] = value
    if current_entry:
        entries.append(current_entry)
    return entries

def write_to_csv(entries):
    # Collect all unique headers
    headers = set(output_headers)
    for entry in entries:
        headers.update(entry.keys())
        
     # Remove Gender if present
    headers.discard("Gender")
    # Organize headers, prefer output_headers order
    final_headers = [h for h in output_headers if h in headers] + sorted(h for h in headers if h not in output_headers)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=final_headers)
        writer.writeheader()
        for entry in entries:
            row = {}
            for key in entry:
                norm_key = normalize_fieldname(key)
                if norm_key == "Gender":
                    continue  # skip gender
                value = clean_value(norm_key, entry[key])
                row[norm_key] = value
            row.pop("Gender", None)
            writer.writerow(row)

if __name__ == "__main__":
    text = input_file.read_text(encoding='utf-8')
    parsed_entries = parse_input(text)
    write_to_csv(parsed_entries)
    print(f"CSV file generated: {output_file}. Parsed {len(parsed_entries)} entries.")
