import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
allData = pd.read_csv('../Csv_Excel_files/imputed_last_data_csv.csv', delimiter=";", encoding="utf-8")
df = pd.DataFrame(allData)

# Display the first few rows of the dataset
df.head()

# Remove duplicate rows based on 'Ad No'
print(len(df))
df = df.drop_duplicates(subset=['Ad No'])
print(len(df))

# Drop columns that won't be used for price prediction
df = df.drop(columns=['Ad No','Ad Date', 'Vehicle Condition'])

# Define a dictionary for month conversions
months = { 'Oca': '1','Şub': '2', 'Mar': '3', 'Nis': '4', 'May': '5', 'Haz': '6', 'Tem': '7', 'Ağu': '8', 'Eyl': '9', 'Eki': '10', 'Kas': '11', 'Ara': '12'}

# Conversion function for 'Average Fuel Consumption'
def convert_date_AFC(date):
    if '.' in date:
        day, month = date.split('.')
        month_num = months.get(month, month)
        return f"{day}.{month_num}"
    return date

# Apply the conversion to 'Average Fuel Consumption' column
df['Average Fuel Consumption'] = df['Average Fuel Consumption'].apply(convert_date_AFC)

# Conversion function for 'Model'
def convert_date_Model(date):
    for ay, num in months.items():
        if f'1.{ay}' in date:
            return date.replace(f'1.{ay}', f'1.{num}')
    return date

# Apply the conversion to 'Model' column
df['Model'] = df['Model'].apply(convert_date_Model)

# Encode categorical columns with low unique values
df['Exchangeable'] = df['Exchangeable'].replace({'Takasa Uygun': 0, 'Takasa Uygun Değil': 1})
df['From Whom'] = df['From Whom'].replace({ 'Yetkili Bayiden': 0, 'Sahibinden': 1, 'Galeriden': 2})
df['Drive'] = df['Drive'].replace({ 'Önden Çekiş': 0, 'Arkadan İtiş': 1, '4WD (Sürekli)': 2, 'AWD (Elektronik)': 3})
df['Transmission Type'] = df['Transmission Type'].replace({'Düz': 0, 'Otomatik': 2, 'Yarı Otomatik': 1})
df['Fuel Type'] = df['Fuel Type'].replace({'LPG & Benzin': 0, 'Benzin': 1, 'Dizel': 2, 'Hibrit': 3})
df['Body Type'] = df['Body Type'].replace({'Sedan': 0, 'Hatchback/3': 1, 'Hatchback/5': 2, 'Station wagon': 3, 'Coupe': 4, 'Cabrio': 5, 'Roadster': 6, 'MPV': 7, 'SUV': 8, 'Pick-up': 9})

# Function to encode columns with many unique values
def encode_column(df, column_name):
    unique_values = df[column_name].unique().tolist()
    encoding = {value: idx + 1 for idx, value in enumerate(unique_values)}
    df[column_name] = df[column_name].map(encoding)
    return encoding

# Encode 'Brand', 'Series', 'Model', and 'Color' columns
brands_encoding = encode_column(df, 'Brand')
series_encoding = encode_column(df, 'Series')
model_encoding = encode_column(df, 'Model')
color_encoding = encode_column(df, 'Color')

# Display unique values of each column
for column in df.columns:
    print("Unique Values of "+ column)
    print(df[column].unique())
    print("/////////////////////////////////////\n")

# Save the encoded DataFrame to a new CSV file
df.to_csv('../Csv_Excel_files/encoded_data_csv.csv', index=False)
