import json
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def read_data(file_path):
    """Read temperature graph data from JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def plot_line_graph(df):
    """Plot a line graph of temperature data."""
    plt.figure(figsize=(10,5))
    plt.plot(df['date'], df['temperature'], label='Temperature Over Time')
    plt.title('Temperature Line Graph')
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_histogram(df):
    """Plot a histogram of temperature data."""
    plt.figure(figsize=(10,5))
    plt.hist(df['temperature'], bins=20, alpha=0.7, color='blue')
    plt.title('Temperature Histogram')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Generate meteorological data visualizations.')
    parser.add_argument('graph_type', choices=['line', 'histogram'], help='Type of graph to generate.')
    args = parser.parse_args()

    df = read_data('temp_graph_data.json')

    if args.graph_type == 'line':
        plot_line_graph(df)
    elif args.graph_type == 'histogram':
        plot_histogram(df)

if __name__ == '__main__':
    main()