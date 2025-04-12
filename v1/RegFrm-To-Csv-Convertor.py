import pandas as pd
import re
import sys

def extract_title(section):
    titles = ['HOMETOWN DETAILS', 'CURRENT RESIDENCE', 'OTHER DETAILS', 'REFERRED By']
    section_lines = section.strip().split('\n')
    if section_lines:
        first_line = section_lines[0].strip()
        for title in titles:
            if first_line == title or first_line == f'*{title}*':
                return title
    return 'STUDENT DETAILS' 

def parse_student_details(text):
    # Split the text into sections
    sections = text.split('------------------------------')
    #sections = re.split(r'-{30,}', text)
    data = {}
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Extract section title if present
        # title_match = re.match(r'\*(.*?)\*', section)
        # if title_match:
        #     section_title = title_match.group(1).strip()
        #     # Remove the title from the section text
        #     section = re.sub(r'\*(.*?)\*', '', section).strip()
        # else:
        #     section_title = "STUDENT DETAILS"
        section_title = extract_title(section)
        lines = section.strip().split('\n')
        # Parse key-value pairs
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                # Prefix the key with the section title to avoid duplicate keys
                if section_title != 'STUDENT DETAILS':
                      key = f"{section_title} - {key}"
                data[key] = value
    
    return data

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def split_entries(content):
    # Pattern to match the start and end of each entry
    pattern = r'KARMH-B02 STUDENT DETAILS\n={19,22}\n([\s\S]*?)(?=\n={19,22}\n|$)'
    entries = re.findall(pattern, content)
    #print(f"Number of entries found: {len(entries)}")
    if not entries:
        print("Warning: No valid entries found in the file. Check the file format.")
    return entries

def main():
    file_path = 'KARMH-B02_Registrations.txt'  # Replace with your file path
    content = read_file(file_path)
    #print(f"File content length: {len(content)} characters")
    entries = split_entries(content)
    print(f"Number of entries found: {len(entries)}")
    all_data = []
    for i, entry in enumerate(entries, 1):
        data = parse_student_details(entry)
        #print(f"Entry {i} parsed data: {data}")
        all_data.append(data)
    
    if not all_data:
        print("No data to process. Exiting.")
        return

    # Create a DataFrame
    df = pd.DataFrame(all_data)
    #print(f"DataFrame shape: {df.shape}")
    #print(f"DataFrame columns: {df.columns}")
    
    # Export to CSV
    csv_path = 'KARMH-B02_Registrations.csv'
    df.to_csv(csv_path, index=False)
    print(f"Data exported to {csv_path}")

if __name__ == "__main__":
    main()