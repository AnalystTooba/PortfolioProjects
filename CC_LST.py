import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Load the single file
data = pd.read_csv('/content/Final.csv')

# Define column names
lst_20m_col = 'LST_20m'
lst_10m_col = 'LST_10m'
cc20px_d20_col = 'CC20px_D20'
cc20px_d10_col = 'CC20px_D10'
cc10px_d20_col = 'CC10px_D20'
cc10px_d10_col = 'CC10px_D10'

# LULC classes with their representations
lulc_classes = {
    1: 'Trees',
    53: 'Buildings',
    101: 'Grass',
    110: 'Paved',
    146: 'Water',
    167: 'Agriculture',
    168: 'Vacant Land'
}

# Prepare data for each scenario
data_10m_100m = data[[lst_10m_col, cc10px_d10_col]].dropna()
data_10m_200m = data[[lst_10m_col, cc10px_d20_col]].dropna()
data_20m_100m = data[[lst_20m_col, cc20px_d10_col]].dropna()
data_20m_200m = data[[lst_20m_col, cc20px_d20_col]].dropna()

# Perform linear regression for each scenario
model_10m_100m = LinearRegression().fit(data_10m_100m[[cc10px_d10_col]], data_10m_100m[lst_10m_col])
model_10m_200m = LinearRegression().fit(data_10m_200m[[cc10px_d20_col]], data_10m_200m[lst_10m_col])
model_20m_100m = LinearRegression().fit(data_20m_100m[[cc20px_d10_col]], data_20m_100m[lst_20m_col])
model_20m_200m = LinearRegression().fit(data_20m_200m[[cc20px_d20_col]], data_20m_200m[lst_20m_col])

# Plot the data and regression lines
plt.figure(figsize=(15, 10))

# 10m Resolution - 100m CC
plt.subplot(2, 2, 1)
plt.scatter(data_10m_100m[cc10px_d10_col], data_10m_100m[lst_10m_col], color='black', s=15, alpha=0.7)
plt.plot(data_10m_100m[cc10px_d10_col], model_10m_100m.predict(data_10m_100m[[cc10px_d10_col]]), color='red', linewidth=2)
plt.xlabel('Cooling Capacity (10m)')
plt.ylabel('Land Surface Temperature')
plt.title('10m Resolution - 100m CC')
plt.grid(True, linestyle='--', alpha=0.7)

# 10m Resolution - 200m CC
plt.subplot(2, 2, 2)
plt.scatter(data_10m_200m[cc10px_d20_col], data_10m_200m[lst_10m_col], color='black', s=15, alpha=0.7)
plt.plot(data_10m_200m[cc10px_d20_col], model_10m_200m.predict(data_10m_200m[[cc10px_d20_col]]), color='red', linewidth=2)
plt.xlabel('Cooling Capacity (10m)')
plt.ylabel('Land Surface Temperature')
plt.title('10m Resolution - 200m CC')
plt.grid(True, linestyle='--', alpha=0.7)

# 20m Resolution - 100m CC
plt.subplot(2, 2, 3)
plt.scatter(data_20m_100m[cc20px_d10_col], data_20m_100m[lst_20m_col], color='black', s=15, alpha=0.7)
plt.plot(data_20m_100m[cc20px_d10_col], model_20m_100m.predict(data_20m_100m[[cc20px_d10_col]]), color='red', linewidth=2)
plt.xlabel('Cooling Capacity (20m)')
plt.ylabel('Land Surface Temperature')
plt.title('20m Resolution - 100m CC')
plt.grid(True, linestyle='--', alpha=0.7)

# 20m Resolution - 200m CC
plt.subplot(2, 2, 4)
plt.scatter(data_20m_200m[cc20px_d20_col], data_20m_200m[lst_20m_col], color='black', s=15, alpha=0.7)
plt.plot(data_20m_200m[cc20px_d20_col], model_20m_200m.predict(data_20m_200m[[cc20px_d20_col]]), color='red', linewidth=2)
plt.xlabel('Cooling Capacity (20m)')
plt.ylabel('Land Surface Temperature')
plt.title('20m Resolution - 200m CC')
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
