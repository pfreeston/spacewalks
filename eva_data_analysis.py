import matplotlib.pyplot as plt
import pandas as pd

'''
This script reads in data about extravehicular activities (EVAs) from a JSON file, 
processes it, and outputs a CSV file and a graph showing the cumulative time spent 
in space over the years. 

The JSON data is expected to have fields such as 'date', 'duration', and 'eva'. 
The script converts the duration from a string format (e.g., "2:30") to 
hours, calculates the cumulative time, and plots it against the date.
'''

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva-data.json', 'r', encoding='ascii')
output_file = open('./eva-data.csv', 'w', encoding='utf-8')
graph_file = './cumulative_eva_graph.png'

print("--START--")

# Read the JSON data into a DataFrame, convert 'eva' to float, and drop rows with missing 'duration' or 'date'
def read_json_to_dataframe(input_file):
    """
    Reads a JSON file and converts it into a pandas DataFrame, ensuring that the 'eva' column is of type float and dropping rows with missing 'duration' or 'date'.

    Args:
        input_file (file or str): The path to the JSON file or a file object.

    Returns:
        eva_df (pd.DataFrame): The cleaned DataFrame containing the EVA data.
    """
    print(f'Reading JSON file {input_file.name}')
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
    eva_df['eva'] = eva_df['eva'].astype(float)
    eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)
    return eva_df

# Save the processed DataFrame to a CSV file
def write_dataframe_to_csv(eva_df, output_file):
    """
    Saves a pandas DataFrame to a CSV file.

    Args:
        eva_df (pd.DataFrame): The DataFrame to save.
        output_file (file or str): The path to the CSV file or a file object.
    """
    print(f'Saving to csv file {output_file.name}')
    eva_df.to_csv(output_file, index=False, encoding='utf-8')

# Read the data from the json file
eva_data = read_json_to_dataframe(input_file)

# Convert and export the data to a csv file
write_dataframe_to_csv(eva_data, output_file)

# Sort the DataFrame by date, convert 'duration' to hours, and calculate the cumulative time spent in space
eva_data.sort_values('date', inplace=True)
eva_data['duration_hours'] = eva_data['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
eva_data['cumulative_time'] = eva_data['duration_hours'].cumsum()

# Plot the cumulative time spent in space over the years
def plot_cumulative_time_in_space(eva_data, graph_file):
    """
    Plots the cumulative time spent in space over the years and saves the plot to a file.

    Args:
        eva_data (pd.DataFrame): The DataFrame containing the EVA data.
        graph_file (str): The path to the file where the plot will be saved.
    """
    print(f'Plotting cumulative time spent in space over the years and saving to {graph_file}')
    plt.plot(eva_data['date'], eva_data['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()

plot_cumulative_time_in_space(eva_data, graph_file)

print("--END--")