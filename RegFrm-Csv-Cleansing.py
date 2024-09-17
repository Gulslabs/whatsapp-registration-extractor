import pandas as pd
import re
import os

def remove_empty_rows(df):
    """
    Remove empty rows from the DataFrame.
    
    :param df: Input DataFrame
    :return: DataFrame with empty rows removed
    """
    df_cleaned = df.dropna(how='all')
    print(f"Rows before removing empty rows: {len(df)}, Rows after: {len(df_cleaned)}")
    return df_cleaned

def clean_phone_numbers(df):
    """
    Clean phone numbers in the DataFrame.
    
    :param df: Input DataFrame
    :return: DataFrame with cleaned phone numbers
    """
    def clean_number(number):
        if pd.isna(number):
            return number
        # Remove '+91 ' or '+91' prefix and any non-digit characters
        return re.sub(r'^\+91\s?|\D', '', str(number))
    
    columns_to_clean = ['Mobile#', 'WhatsApp#', 'REFERRED By - Mobile#']
    
    for column in columns_to_clean:
        if column in df.columns:
            df[column] = df[column].apply(clean_number)
    
    print("Phone numbers cleaned in the DataFrame")
    return df

def clean_student_data(input_file, output_file):
    """
    Clean the student data by removing empty rows and cleaning phone numbers.
    Then delete the original input file.
    
    :param input_file: Path to the input CSV file
    :param output_file: Path to save the cleaned CSV file
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    print(f"Original DataFrame shape: {df.shape}")

    # Remove empty rows
    df = remove_empty_rows(df)

    # Clean phone numbers
    df = clean_phone_numbers(df)

    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
    print(f"Final DataFrame shape: {df.shape}")

    # Delete the original input file
    try:
        # os.remove(input_file)
        print(f"Original file {input_file} has been deleted.")
    except OSError as e:
        print(f"Error: {input_file} : {e.strerror}")

if __name__ == "__main__":
    input_file = 'KARMH-B02_Registrations.csv'
    output_file = 'KARMH-B02_Registrations-Final.csv'
    
    clean_student_data(input_file, output_file)
    
    print("Data cleaning completed.")