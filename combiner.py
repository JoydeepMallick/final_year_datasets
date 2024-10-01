import os
import pandas as pd

# Base directory where the folders (A1, A2, C1, ...) are located
base_dir = "./Preprocessed" 

# Directory to save the cleaned CSV files
cleaned_dir = "./Cleaned"  

# Create the cleaned directory if it doesn't exist
os.makedirs(cleaned_dir, exist_ok=True)

def filter_zero_rows(df):
    """
    Filters out rows where 'Customer' and 'Loc' columns are invalid (both zero).
    
    Parameters:
    df (pd.DataFrame): The input DataFrame to be filtered.

    Returns:
    pd.DataFrame: The filtered DataFrame with invalid rows removed.
    """
    # Initialize a list to hold valid rows
    rows_to_keep = []
    
    # Iterate through each row in the DataFrame
    for ind, row in df.iterrows():
        # Check if both 'Customer' and 'Loc' columns are zero
        if not ((row['Customer'] in [0, '0']) and (row['Loc'] in [0, '0'])):
            rows_to_keep.append(row)
    
    # Combine the rows back into a DataFrame
    updated_df = pd.DataFrame(rows_to_keep, columns=df.columns)
    
    return updated_df.reset_index(drop=True)


def combine_csv_files(main_folder, folder_path):
    all_data = []
    # Iterate through the folders and read the CSV files
    for folder in os.listdir(folder_path):
        sub_folder_path = os.path.join(folder_path, folder)
        
        if os.path.isdir(sub_folder_path):
            # Find the CSV file in each folder
            for file in os.listdir(sub_folder_path):
                if file.endswith('.csv'):
                    csv_file_path = os.path.join(sub_folder_path, file)
                    
                    # Read the CSV file
                    df = pd.read_csv(csv_file_path)
                    
                    df_filtered = filter_zero_rows(df)

                    # Append to the updated list
                    all_data.append(df_filtered)

    # Combine all the data into a single DataFrame
    combined_data = pd.concat(all_data, ignore_index=True)

    # Save the combined data to a new CSV file with the folder's name
    output_csv_path = os.path.join(cleaned_dir, f"{main_folder}.csv")
    combined_data.to_csv(output_csv_path, index=False)

    print(f"All CSV files from folder {folder} combined and saved to {output_csv_path}")




if __name__ == "__main__":
# Iterate through all folders in the base directory
    for folder in os.listdir(base_dir):
        
        folder_path = os.path.join(base_dir, folder)
        
        if os.path.isdir(folder_path):
            print("Working on folder:", folder)
            combine_csv_files(folder, folder_path)

            