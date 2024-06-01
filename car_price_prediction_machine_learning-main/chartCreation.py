import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
allData = pd.read_csv('../Csv_Excel_files/imputed_last_data_csv.csv', delimiter=";", encoding="utf-8")
df = pd.DataFrame(allData)

# Uncomment the following block to create a pivot table and bar plot

# # Create a pivot table
# pivot_table = df.pivot_table(index='Brand', columns='Color', aggfunc='size', fill_value=0)
#
# # Create a color palette for the plot
# palette = sns.color_palette("hsv", len(pivot_table.columns))
#
# # Create a stacked bar plot
# ax = pivot_table.plot(kind='bar', stacked=True, figsize=(14, 8), color=palette)
#
# # Set the title and labels
# plt.title('Her Modelin Renk Dağılımı')
# plt.xlabel('Brand')
# plt.ylabel('Count')
#
# # Move the legend outside of the plot
# plt.legend(title='Renk', bbox_to_anchor=(1.05, 1), loc='upper left')
#
# # Show the plot
# plt.show()

# Uncomment the following block to create scatter plots based on mileage and price groups

# # Calculate the maximum and minimum values for mileage and price
# max_mileage = df['Mileage'].max()
# max_price = df['Price'].max()
# min_mileage = df['Mileage'].min()
# min_price = df['Price'].min()
#
# # Group the Mileage column into 50000 intervals
# bins_mileage = range(0, int(max_mileage) + 50000, 50000)
# labels_mileage = [f'{i}-{i+50000-1}' for i in bins_mileage[:-1]]
# df['Mileage_Group'] = pd.cut(df['Mileage'], bins=bins_mileage, labels=labels_mileage, right=False, include_lowest=True)
# df['Mileage_Group_Number'] = pd.cut(df['Mileage'], bins=bins_mileage, labels=False, right=False, include_lowest=True)
#
# # Group the Price column into 100000 intervals
# bins_price = range(100000, int(max_price) + 100000, 100000)
# labels_price = [f'{i}-{i+100000-1}' for i in bins_price[:-1]]
# df['Price_Group'] = pd.cut(df['Price'], bins=bins_price, labels=labels_price, right=False, include_lowest=True)
# df['Price_Group_Number'] = pd.cut(df['Price'], bins=bins_price, labels=False, right=False, include_lowest=True)
#
# # Filter out NaN values
# df = df.dropna(subset=['Mileage_Group_Number', 'Price_Group_Number'])
#
# # Create a scatter plot for Mileage and Price groups
# plt.figure(figsize=(15, 7))
# plt.scatter(df['Mileage_Group_Number'], df['Price_Group_Number'], alpha=0.6)
# plt.title('Distribution by Price & Mileage Groups')
# plt.xlabel('Mileage KM')
# plt.ylabel('Price TL')
# plt.xticks(ticks=np.arange(len(labels_mileage)), labels=labels_mileage, rotation=90)
# plt.yticks(ticks=np.arange(len(labels_price)), labels=labels_price)
#
# # Show the plot
# plt.show()
#
# # Remove the temporary grouping columns
# df.drop(columns=['Mileage_Group', 'Mileage_Group_Number', 'Price_Group', 'Price_Group_Number'], inplace=True)

# Uncomment the following block to create a scatter plot for Engine Power and Average Fuel Consumption

# # Create a scatter plot for Engine Power and Average Fuel Consumption
# plt.figure(figsize=(8, 15))
# plt.scatter(df['Engine Power'], df['Average Fuel Consumption'], color='blue', alpha=0.6)
#
# # Set the title and labels
# plt.title('Engine Power vs. Average Fuel Consumption')
# plt.xlabel('Engine Power')
# plt.ylabel('Average Fuel Consumption')
# plt.grid(True)
#
# # Show the plot
# plt.show()

# Uncomment the following block to create a box plot for Drive and Price relationship

# # Create a box plot for Drive and Price relationship
# plt.figure(figsize=(8, 6))
# sns.boxplot(x='Drive', y='Price', data=df)
#
# # Set the title and labels
# plt.title('Drive & Price Relationship')
# plt.xlabel('Drive')
# plt.ylabel('Price')
#
# # Show the plot
# plt.show()
