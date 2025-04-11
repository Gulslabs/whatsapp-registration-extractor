import csv
import re

# Constants
INPUT_FILE = 'whatsapp_students_registration.txt'
OUTPUT_FILE = 'whatsapp_students_registration.csv'

# Ordered list of fields based on the given format (including duplicates)
COLUMNS = [
    'Full Name', 'Mobile#', 'WhatsApp#',
    'Area/Locality', 'City', 'District', 'State',
    'Area/Locality', 'Mandal', 'City', 'State',
    'Age', 'Qualification', 'Profession', 'Email Address',
    'Full Name', 'Mobile#', 'Student ID#', 'Batch#'
]

SEPARATOR_REGEX = r'[\-=]{2,}|[\-=:]{1,}'  # Decorative separators
FIELD_REGEX = re.compile(r'^(.*?)(?:\s*[:=\-]+\s*)(.*)$')  # Flexible key-value match
WHATSAPP_MSG_REGEX = re.compile(r"^\[\d{1,2}:\d{2}, \d{1,2}/\d{1,2}/\d{4}\] \+?\d{1,15}: ")

def clean_value(value):
    """Cleans values by trimming and removing +91 from phone numbers."""
    value = value.strip()
    if value.startswith('+91'):
        value = value[3:]
    return value

def parse_registration_entries(text):
    """Parses all registration blocks into a list of dictionaries with fixed column order."""
    entries = [entry.strip() for entry in text.split("TSAP-B02 STUDENT DETAILS") if entry.strip()]
    parsed_data = []

    for entry in entries:
        values = []
        for line in entry.splitlines():
            line = line.strip()

            if not line or re.fullmatch(SEPARATOR_REGEX, line) or WHATSAPP_MSG_REGEX.match(line):
                continue

            match = FIELD_REGEX.match(line)
            if match:
                key = match.group(1).strip()
                value = clean_value(match.group(2))
                values.append((key, value))

        # Flatten into a dictionary using COLUMNS
        registration = {}
        col_idx = 0
        for key, value in values:
            if col_idx < len(COLUMNS):
                registration[COLUMNS[col_idx]] = value
                col_idx += 1
        # Fill missing fields with empty string
        for col in COLUMNS:
            registration.setdefault(col, '')
        parsed_data.append(registration)

    return parsed_data

def write_to_csv(data, output_file):
    """Writes the data into a CSV file with original field names and order."""
    if not data:
        print("No data to write.")
        return

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    with open(INPUT_FILE, encoding='utf-8') as f:
        text = f.read()

    parsed_data = parse_registration_entries(text)
    write_to_csv(parsed_data, OUTPUT_FILE)
    print(f"✅ Parsed {len(parsed_data)} entries and wrote to '{OUTPUT_FILE}'")

if __name__ == '__main__':
    main()
