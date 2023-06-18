import os
import pandas as pd
import time

def merge_data_from_folder(folder_path):
    merged_df = pd.DataFrame()  # Create an empty DataFrame for merged data

    start_time = time.time()  # Record the start time

    # Iterate over files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Read the data file into a DataFrame
        df = pd.read_csv(file_path)

        # Append the DataFrame to the merged DataFrame
        merged_df = merged_df.append(df, ignore_index=True)

        # Print update with the name of the merged file
        print(f"Merged file: {file_name}")

    end_time = time.time()  # Record the end time
    merge_time = end_time - start_time  # Calculate the merge time

    # Print the time taken to merge the files
    print(f"Merge completed in {merge_time:.2f} seconds.")

    return merged_df
