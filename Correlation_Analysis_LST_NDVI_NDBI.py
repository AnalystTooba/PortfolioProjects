# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Excel file (replace 'path_to_file.xlsx' with your actual file path)
file_path = '/content/sample_data/CORR.xlsx'
data = pd.read_excel(file_path)

# Extract years from the column names
years = ['1993', '1998', '2003', '2008', '2013', '2018', '2023']

# Initialize lists to store correlation results
correlations_ndvi_lst = []
correlations_ndbi_lst = []

# Calculate number of rows and columns for subplots
n_cols = 4
n_rows = int(np.ceil(len(years) / n_cols))

# Create a figure for NDVI vs. LST correlation
plt.figure(figsize=(16, 10))

for i, year in enumerate(years):
    # Compute correlation between NDVI and LST for the year
    corr_ndvi_lst = data[f'NDVI_{year}'].corr(data[f'LST_{year}'])
    correlations_ndvi_lst.append(corr_ndvi_lst)

    # Create a scatter plot
    plt.subplot(n_rows, n_cols, i + 1)
    sns.regplot(
        x=data[f'NDVI_{year}'], y=data[f'LST_{year}'],
        scatter_kws={'color': 'black', 'alpha': 0.7, 's': 10, 'edgecolor': 'grey'},
        line_kws={'color': 'red', 'lw': 2, 'alpha': 0.8},
    )
    plt.title(f'NDVI vs. LST {year}\nCorrelation: {corr_ndvi_lst:.2f}', fontsize=10)
    plt.xlabel(f'NDVI {year}', fontsize=8)
    plt.ylabel(f'LST {year}', fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

plt.tight_layout()
plt.suptitle('NDVI vs. LST Correlation Analysis', y=1.02, fontsize=16)
plt.show()

# Create a figure for NDBI vs. LST correlation
plt.figure(figsize=(16, 10))

for i, year in enumerate(years):
    # Compute correlation between NDBI and LST for the year
    corr_ndbi_lst = data[f'NDBI_{year}'].corr(data[f'LST_{year}'])
    correlations_ndbi_lst.append(corr_ndbi_lst)

    # Create a scatter plot
    plt.subplot(n_rows, n_cols, i + 1)
    sns.regplot(
        x=data[f'NDBI_{year}'], y=data[f'LST_{year}'],
        scatter_kws={'color': 'black', 'alpha': 0.7, 's': 10, 'edgecolor': 'grey'},
        line_kws={'color': 'red', 'lw': 2, 'alpha': 0.8},
    )
    plt.title(f'NDBI vs. LST {year}\nCorrelation: {corr_ndbi_lst:.2f}', fontsize=10)
    plt.xlabel(f'NDBI {year}', fontsize=8)
    plt.ylabel(f'LST {year}', fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

plt.tight_layout()
plt.suptitle('NDBI vs. LST Correlation Analysis', y=1.02, fontsize=16)
plt.show()

# Print correlation results
correlation_results = pd.DataFrame({
    'Year': years,
    'NDVI vs. LST Correlation': correlations_ndvi_lst,
    'NDBI vs. LST Correlation': correlations_ndbi_lst
})

print("\nCorrelation Results:")
print(correlation_results)

# Save correlation results to a CSV file
output_path = '/content/sample_data/correlation_results.csv'
correlation_results.to_csv(output_path, index=False)
print(f"Correlation results saved to {output_path}")

# Create the dataframe with the correlation data
data = {
    'Year': [1993, 1998, 2003, 2008, 2013, 2018, 2023],
    'NDVI vs. LST Correlation': [-0.693208, -0.669235, -0.829980, -0.860369, -0.859963, -0.831691, -0.745947],
    'NDBI vs. LST Correlation': [0.781815, 0.794218, 0.887275, 0.898917, 0.903256, 0.867285, 0.854505]
}

df = pd.DataFrame(data)

# Create a heatmap-friendly format
correlation_matrix = np.array([df['NDVI vs. LST Correlation'], df['NDBI vs. LST Correlation']])

# Set the plot style
sns.set(style="whitegrid")

# Create the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", xticklabels=df['Year'], yticklabels=["NDVI vs. LST", "NDBI vs. LST"], cbar_kws={'label': 'Correlation'}, linewidths=0.5)

# Add titles and labels
plt.title('Correlation Between NDVI/NDBI and LST Over the Years', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Correlation Type', fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()
