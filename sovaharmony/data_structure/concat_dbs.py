import os
import pandas as pd
import pyarrow.feather as feather

def concatenate_feather_files_in_folder(folder_path, input_files, output_file):
    """
    Concatenate multiple Feather files in a folder into a single Feather file.

    Parameters:
    - folder_path (str): The path to the folder containing the Feather files.
    - input_files (list): List of input Feather files to concatenate.
    - output_file (str): The name of the output concatenated Feather file.

    Returns:
    None
    """
    # Create a list to store DataFrames for each input file
    dataframes = []

    # Combine paths to get full paths of input files
    input_file_paths = [os.path.join(folder_path, file) for file in input_files]

    # Read each Feather file and append its DataFrame to the list
    for input_file_path in input_file_paths:
        df = feather.read_feather(input_file_path)
        dataframes.append(df)

    # Concatenate all DataFrames in the list
    concatenated_df = pd.concat(dataframes, ignore_index=True)

    # Write the concatenated DataFrame to a new Feather file
    output_file_path = os.path.join(folder_path, output_file)
    feather.write_feather(concatenated_df, output_file_path)

# Example usage:
data_folder = r'C:\Users\Luisa\OneDrive - Universidad de Antioquia\Maestria_Luisa\data\Data_complete\ic'
input_feather_files = ['data_BIOMARCADORES_CE_columns_power_openBCI_False_components_dem.feather', 'data_DUQUE_resting_columns_power_openBCI_False_components_dem.feather']
output_feather_file = 'Data_complete_openBCI_False_components.feather'

concatenate_feather_files_in_folder(data_folder, input_feather_files, output_feather_file)
