import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    data = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    plt.scatter(data['Year'], data['CSIRO Adjusted Sea Level'])

    # Create first line of best fit (using all data)
    slope, intercept, r_value, p_value, std_err = linregress(data['Year'], data['CSIRO Adjusted Sea Level'])
    
    # Plot the first line of best fit (from 1880 to 2050)
    years_extended = range(1880, 2051)  # Extend years to 2050 for prediction
    sea_levels_extended = [slope * year + intercept for year in years_extended]
    plt.plot(years_extended, sea_levels_extended, label='Fit Line (All Data)', color='blue')

    # Create second line of best fit (using data from 2000 onwards)
    recent_data = data[data['Year'] >= 2000]
    slope_recent, intercept_recent, _, _, _ = linregress(recent_data['Year'], recent_data['CSIRO Adjusted Sea Level'])
    
    # Plot the second line of best fit (from 2000 to 2050)
    years_recent_extended = range(2000, 2051)  # Extended years for the second line (2000-2050)
    sea_levels_recent_extended = [slope_recent * year + intercept_recent for year in years_recent_extended]
    plt.plot(years_recent_extended, sea_levels_recent_extended, label='Fit Line (2000 Onwards)', color='red')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    plt.legend()

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()

# Call the function to draw the plot
draw_plot()