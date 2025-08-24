import pandas as pd
import sys
from datetime import datetime
import re

# Global Configuration
ENABLE_DURATION_THRESHOLD = True  # Set to True to enable duration threshold splitting
DURATION_THRESHOLD = 20  # Minimum duration to stay in main sheet

def process_name(name):
    """Process the name according to the specified rules"""
    # Handle NaN or None values
    if pd.isna(name) or name is None:
        return ""
    
    # Convert to string if it's not already
    name = str(name).strip()
    
    # Skip empty strings
    if not name:
        return ""
    
    # Rule 1: Simple name like 'Tariq Fareed' - copy as is
    if '(' not in name:
        return name
    
    # Rule 2: Check if first bracket contains 'Naqeeb'
    # Pattern: 'IK_Irfan Khan(Naqeeb) (Irfan Khan Yousufzai)'
    first_bracket_match = re.search(r'\(([^)]+)\)', name)
    if first_bracket_match:
        first_bracket_content = first_bracket_match.group(1)
        if 'Naqeeb' in first_bracket_content:
            # Keep everything up to and including the first bracket
            end_pos = first_bracket_match.end()
            return name[:end_pos]
        else:
            # Rule 3: If first bracket doesn't contain 'Naqeeb', remove everything from first bracket onwards
            start_pos = first_bracket_match.start()
            return name[:start_pos].strip()
    
    return name

def extract_date_from_datetime(datetime_str):
    """Extract date part from datetime string like '8/23/2025 07:35:40 PM'"""
    try:
        # Parse the datetime string and extract just the date part
        dt = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M:%S %p')
        return dt.strftime('%m/%d/%Y')  # Return in same format
    except:
        # If parsing fails, try to extract date part manually
        if ' ' in datetime_str:
            return datetime_str.split(' ')[0]
        return datetime_str

def generate_filename(topic_cell):
    """Generate filename from the topic cell (A1)"""
    # Handle NaN or None values
    if pd.isna(topic_cell) or topic_cell is None:
        return "Time_Sheet_Unknown.xlsx"
    
    # Convert to string if it's not already
    topic_cell = str(topic_cell).strip()
    
    # Skip empty strings
    if not topic_cell:
        return "Time_Sheet_Unknown.xlsx"
    
    # Extract the part in parentheses for filename
    # '(KARMH-B02) #90 Surah Al-Balad' -> 'Time_Sheet_KARMH-B02_Surah Al-Balad.xlsx'
    
    # Remove parentheses and # symbol, replace spaces with underscores
    # First extract the content within parentheses
    match = re.search(r'\(([^)]+)\)', topic_cell)
    if match:
        code_part = match.group(1)  # KARMH-B02
    else:
        code_part = "Unknown"
    
    # Extract the title part (everything after the parentheses and #number)
    # Remove parentheses part and # with number
    remaining = re.sub(r'\([^)]+\)\s*#\d+\s*', '', topic_cell).strip()
    title_part = remaining.replace(' ', '_')
    
    filename = f"Time_Sheet_{code_part}_{title_part}.xlsx"
    return filename

def split_data_by_duration_threshold(participants_data, duration_threshold=20):
    """
    Split participant data based on duration threshold
    
    Parameters:
    participants_data (list): List of participant dictionaries
    duration_threshold (int): Minimum duration to stay in main sheet
    
    Returns:
    tuple: (main_sheet_data, below_threshold_data)
    """
    main_sheet_data = []
    below_threshold_data = []
    
    for participant in participants_data:
        duration = participant.get('Duration (minutes)', '')
        
        # Check if duration is a number and below threshold
        try:
            duration_value = int(duration) if duration != '' else 0
            if duration_value < duration_threshold:
                below_threshold_data.append(participant)
            else:
                main_sheet_data.append(participant)
        except (ValueError, TypeError):
            # If duration is not a valid number, keep in main sheet
            main_sheet_data.append(participant)
    
    return main_sheet_data, below_threshold_data




def load_naqeeb_mapping(naqeeb_file_path='naqeeb_to_initial.csv'):
    """
    Load Naqeeb mapping from CSV file
    
    Parameters:
    naqeeb_file_path (str): Path to the naqeeb mapping CSV file
    
    Returns:
    dict: Dictionary mapping initials to naqeeb names
    """
    naqeeb_mapping = {}
    try:
        df = pd.read_csv(naqeeb_file_path)
        for _, row in df.iterrows():
            if len(row) >= 2:
                naqeeb_name = str(row.iloc[0]).strip()
                initials = str(row.iloc[1]).strip()
                naqeeb_mapping[initials] = naqeeb_name
        print(f"Loaded {len(naqeeb_mapping)} Naqeeb mappings from {naqeeb_file_path}")
    except FileNotFoundError:
        print(f"Warning: Naqeeb mapping file '{naqeeb_file_path}' not found. Naqeeb column will remain blank.")
    except Exception as e:
        print(f"Warning: Error loading Naqeeb mapping: {str(e)}")    
    return naqeeb_mapping

def get_naqeeb_name(original_name, naqeeb_mapping):
    """
    Get Naqeeb name based on initials in the original name
    
    Parameters:
    original_name (str): The original name from CSV
    naqeeb_mapping (dict): Dictionary mapping initials to naqeeb names
    
    Returns:
    str: Naqeeb name if found, empty string otherwise
    """
    if not original_name or not naqeeb_mapping:
        return ''
    
    # Check if name starts with any initials pattern (with or without underscore)
    for initials, naqeeb_name in naqeeb_mapping.items():
        # Check for "AZ_" pattern
        if original_name.startswith(f"{initials}_"):
            return naqeeb_name
        # Check for "RT " pattern (initials followed by space)
        elif original_name.startswith(f"{initials} "):
            return naqeeb_name
        # Check for exact initials at start followed by non-letter character
        elif len(original_name) > len(initials) and original_name.startswith(initials):
            # Make sure the character after initials is not a letter (to avoid partial matches)
            next_char = original_name[len(initials)]
            if not next_char.isalpha():
                return naqeeb_name
    
    return ''

def consolidate_duplicate_participants(participants_data):
    """
    Consolidate participants with multiple join/leave sessions
    
    Parameters:
    participants_data (list): List of participant dictionaries
    
    Returns:
    list: Consolidated list with merged sessions for duplicate participants
    """
    from datetime import datetime
    
    consolidated = {}
    
    for participant in participants_data:
        name = participant['Name']
        
        if name in consolidated:
            # Merge with existing entry
            existing = consolidated[name]
            
            # Parse times to find earliest join and latest leave
            try:
                # Current participant times
                current_join = datetime.strptime(participant['Join Time'], '%m/%d/%Y %I:%M:%S %p')
                current_leave = datetime.strptime(participant['Leave Time'], '%m/%d/%Y %I:%M:%S %p')
                
                # Existing participant times
                existing_join = datetime.strptime(existing['Join Time'], '%m/%d/%Y %I:%M:%S %p')
                existing_leave = datetime.strptime(existing['Leave Time'], '%m/%d/%Y %I:%M:%S %p')
                
                # Use earliest join time and latest leave time
                earliest_join = min(current_join, existing_join)
                latest_leave = max(current_leave, existing_leave)
                
                # Calculate total duration in minutes
                total_duration = int((latest_leave - earliest_join).total_seconds() / 60)
                
                # Add individual session duration to running total
                current_duration = int(participant['Duration (minutes)']) if participant['Duration (minutes)'] != '' else 0
                existing_session_duration = existing.get('session_duration', 0)
                total_session_duration = existing_session_duration + current_duration
                
                # Update consolidated entry
                consolidated[name].update({
                    'Join Time': earliest_join.strftime('%m/%d/%Y %I:%M:%S %p'),
                    'Leave Time': latest_leave.strftime('%m/%d/%Y %I:%M:%S %p'),
                    'Duration (minutes)': total_session_duration,  # Sum of all session durations
                })
                consolidated[name]['session_duration'] = total_session_duration
                
            except (ValueError, TypeError) as e:
                # If time parsing fails, keep the existing entry
                print(f"Warning: Could not parse times for {name}: {e}")
                continue
                
        else:
            # First occurrence of this participant
            duration = int(participant['Duration (minutes)']) if participant['Duration (minutes)'] != '' else 0
            participant_copy = participant.copy()
            participant_copy['session_duration'] = duration
            consolidated[name] = participant_copy
    
    # Convert back to list and remove the temporary session_duration field
    result = []
    for participant in consolidated.values():
        if 'session_duration' in participant:
            del participant['session_duration']
        result.append(participant)
    
    print(f"Consolidated {len(participants_data)} records into {len(result)} unique participants")
    return result

def convert_zoom_csv_to_timesheet(csv_file_path, start_time, end_time):
    """
    Convert Zoom CSV to Excel timesheet
    
    Parameters:
    csv_file_path (str): Path to the CSV file
    start_time (str): Start time for the session
    end_time (str): End time for the session
    """
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        # Load Naqeeb mapping
        naqeeb_mapping = load_naqeeb_mapping()
        
        # Get the topic from A1 (index 0, column 0)
        topic_cell = df.iloc[0, 0]  # A1 cell
        
        # Generate filename
        filename = generate_filename(topic_cell)
        
        # Get the date from E1 (Start time column, row 1)
        start_time_cell = df.iloc[0, 4]  # E1 cell (Start time)
        
        # Handle NaN values for start_time_cell
        if pd.isna(start_time_cell):
            session_date = "Unknown"
        else:
            session_date = extract_date_from_datetime(str(start_time_cell))

        # Create the timesheet data
        # Based on the CSV structure:
        # Row 0: Topic and session info
        # Row 1: Headers ('Name (original name)', 'Email', etc.)
        # Row 2+: Participant data
        header_row_idx = 1
        data_start_idx = 2
        
        # Extract participant data
        participants_data = []
        
        for idx in range(data_start_idx, len(df)):
            row = df.iloc[idx]
            
            # Skip empty rows
            if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == '':
                continue
            
            name = str(row.iloc[0]).strip()  # Name (original name)
            join_time = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ''  # Join time
            leave_time = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ''  # Leave time
            duration = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ''  # Duration (minutes)
            duration = int(duration) if duration.isdigit() else '' 
            
            # Process the name according to rules
            processed_name = process_name(name)
            
            # Get Naqeeb name based on original name
            naqeeb_name = get_naqeeb_name(name, naqeeb_mapping)

            participants_data.append({
                'Name': processed_name,
                'Join Time': join_time,
                'Leave Time': leave_time,
                'Duration (minutes)': duration,
                'Naqeeb Name': naqeeb_name,
                'Remarks': ''  # Leave blank
            })
        
        # Consolidate duplicate participants
        participants_data = consolidate_duplicate_participants(participants_data)
        # Apply duration threshold splitting if enabled
        if ENABLE_DURATION_THRESHOLD:
            main_sheet_data, below_threshold_data = split_data_by_duration_threshold(participants_data, DURATION_THRESHOLD)
            participants_df = pd.DataFrame(main_sheet_data)
            below_threshold_df = pd.DataFrame(below_threshold_data) if below_threshold_data else None
        else:
            participants_df = pd.DataFrame(participants_data)
            below_threshold_df = None
        
        # Create Excel file
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Write participant data starting from row 3 (to leave space for header info)
            participants_df.to_excel(writer, sheet_name='Time_Sheet', index=False, header=True, startrow=2)
            
            # Get the workbook and worksheet to manually add header info
            workbook = writer.book
            worksheet = writer.sheets['Time_Sheet']
            
            # Write header information in row 1
            worksheet['A1'] = 'Date'
            worksheet['B1'] = session_date
            worksheet['C1'] = 'Start Time'
            worksheet['D1'] = start_time
            worksheet['E1'] = 'End Time'
            worksheet['F1'] = end_time
            
            # Write below threshold data to Sheet2 if enabled and data exists
            if ENABLE_DURATION_THRESHOLD and below_threshold_df is not None and len(below_threshold_df) > 0:
                below_threshold_df.to_excel(writer, sheet_name='Below_20_Minutes', index=False, header=True, startrow=2)
                
                # Add header info to Sheet2 as well
                worksheet2 = writer.sheets['Below_20_Minutes']
                worksheet2['A1'] = 'Date'
                worksheet2['B1'] = session_date
                worksheet2['C1'] = 'Start Time'
                worksheet2['D1'] = start_time
                worksheet2['E1'] = 'End Time'
                worksheet2['F1'] = end_time
        
        if ENABLE_DURATION_THRESHOLD:
            print(f"Successfully created timesheet: {filename}")
            print(f"Date: {session_date}")
            print(f"Start Time: {start_time}")
            print(f"End Time: {end_time}")
            print(f"Main sheet participants (>= {DURATION_THRESHOLD} minutes): {len(main_sheet_data)}")
            if below_threshold_data:
                print(f"Sheet2 participants (< {DURATION_THRESHOLD} minutes): {len(below_threshold_data)}")
        else:
            print(f"Successfully created timesheet: {filename}")
            print(f"Date: {session_date}")
            print(f"Start Time: {start_time}")
            print(f"End Time: {end_time}")
            print(f"Total participants processed: {len(participants_data)}")
        
        return filename
        
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) != 4:
        print("Usage: python script.py <csv_file_path> <start_time> <end_time>")
        print("Example: python script.py zoom_data.csv '07:30:00 PM' '11:00:00 PM'")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    
    result = convert_zoom_csv_to_timesheet(csv_file_path, start_time, end_time)
    
    if result:
        print(f"Timesheet generated successfully: {result}")
    else:
        print("Failed to generate timesheet.")

if __name__ == "__main__":
    main()