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


# Read the JSON data into a DataFrame, convert 'eva' to float, and drop rows with missing 'duration' or 'date'
eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
eva_df['eva'] = eva_df['eva'].astype(float)
eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)

# Save the processed DataFrame to a CSV file
eva_df.to_csv(output_file, index=False, encoding='utf-8')

# Sort the DataFrame by date, convert 'duration' to hours, and calculate the cumulative time spent in space
eva_df.sort_values('date', inplace=True)
eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()

# Plot the cumulative time spent in space over the years
plt.plot(eva_df['date'], eva_df['cumulative_time'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()