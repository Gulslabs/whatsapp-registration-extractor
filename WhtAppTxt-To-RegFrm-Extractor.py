def extract_student_details(file_path, output_file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        data = file.readlines()

    extracted_sections = []
    inside_section = False
    gulam_ahsan = False
    section = []

    for i, line in enumerate(data):                
        # Look for the start pattern and begin capturing
        if '*KARMH-B02 STUDENT DETAILS*' in line or 'KARMH-B02 STUDENT DETAILS' in line:            
            if i + 1 < len(data) and ('=====================' in data[i + 1] or '====================' in data[i + 1]):
                inside_section = True
                section.append(line)  # Include the start line                
                continue

        # Continue capturing until the next '====================='
        if inside_section:            
            section.append(line)
            if '=====================' in line and len(section) > 2:  # Ensure it's the second separator                
                extracted_sections.append(''.join(section))
                section = []
                inside_section = False

    # Save the extracted sections to a new file
    with open(output_file_path, 'w') as output_file:
        for section in extracted_sections:
            output_file.write(section)
            output_file.write("\n")  # Add a new line between sections

    print(f"Extracted data saved to {output_file_path}")


def clean_student_details(output_file_path):
    with open(output_file_path, 'r') as file:
        lines = file.readlines()

    cleaned_lines = []
    
    for line in lines:
        # If the line contains the target pattern, strip off anything before it
        if '*KARMH-B02 STUDENT DETAILS*' in line:
            index = line.find('*KARMH-B02 STUDENT DETAILS*')
            cleaned_lines.append(line[index:])  # Keep only the relevant part        
        elif 'KARMH-B02 STUDENT DETAILS' in line:            
            index = line.find('KARMH-B02 STUDENT DETAILS')
            cleaned_lines.append(line[index:])  # Keep only the relevant part        
        else:
            cleaned_lines.append(line)  # If the line doesn't need cleaning, just append it

    # Overwrite the original output file with the cleaned data
    with open(output_file_path, 'w') as file:
        file.writelines(cleaned_lines)

    print(f"Cleaned data saved to {output_file_path}")

# Example usage
input_file_path = 'WhatsApp Chat with KARMH-B02 Registrations.txt'  # Replace with the path to your input file
#input_file_path = 'dummy.txt'
output_file_path = 'KARMH-B02_Registrations.txt'  # Replace with the desired output file path

extract_student_details(input_file_path, output_file_path)
# Step 2: Clean the extracted file by removing unwanted parts
clean_student_details(output_file_path)