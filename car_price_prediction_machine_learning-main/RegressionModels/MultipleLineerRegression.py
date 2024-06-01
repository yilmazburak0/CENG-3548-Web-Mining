import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the dataset
allData = pd.read_csv('../Csv_Excel_files/encoded_data_csv.csv', encoding="utf-8")
df = pd.DataFrame(allData)

# Display the first few rows of the dataset
df.head()

# Separate the input features and the target variable
input_data = df.drop(columns=['Price'])
output_data = df['Price']

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.2, random_state=42)

# Initialize the Linear Regression model
model = LinearRegression()

# Train the model on the training data
model.fit(x_train, y_train)

# Make predictions on the test data
predict = model.predict(x_test)

# Create a DataFrame for a new data point to predict its price
input_data_model = pd.DataFrame([[24,281,1372,2014,225000.0,2,2,0,3,1461,110,0,4.4,60,0,1,0,0]],
 columns = ['Brand','Series','Model','Year','Mileage','Transmission Type','Fuel Type','Body Type','Color','Engine Volume','Engine Power','Drive','Average Fuel Consumption','Fuel Tank','Exchangeable','From Whom','paint','changed'])

# Uncomment the following line to see the DataFrame for the new data point
# print(input_data_model)

# Uncomment the following line to predict the price for the new data point
# print(model.predict(input_data_model))

# Import metrics to evaluate the model
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Make predictions on the test data
y_pred = model.predict(x_test)

# Calculate the R^2 score
r2 = r2_score(y_test, y_pred)
print(f"Modelin R^2 skoru: {r2}")

# Calculate the Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print(f"Modelin Ortalama Kare Hatası (MSE): {mse}")

# Calculate the Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print(f"Modelin Ortalama Mutlak Hatası (MAE): {mae}")

# Calculate the Root Mean Squared Error (RMSE)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Root Mean Squanred Error (RMSE): {rmse}")

# Calculate the Relative Absolute Error (RAE)
rae = mean_absolute_error(y_test, y_pred) / mean_absolute_error(y_test, [np.mean(y_test)]*len(y_test))
print(f"Relative Absolute Error (RAE): {rae}")

# Calculate the Relative Squared Error (RSE)
rse = mean_squared_error(y_test, y_pred) / mean_squared_error(y_test, [np.mean(y_test)]*len(y_test))
print(f"Relative Squared Error (RSE): {rse}")

# Model performance metrics
# Modelin R^2 skoru: 0.7688722965654105
# Modelin Ortalama Kare Hatası (MSE): 23826002501.464832
# Modelin Ortalama Mutlak Hatası (MAE): 85973.99616906734
# Root Mean Squanred Error (RMSE): 154356.7377909524
# Relative Absolute Error (RAE): 0.3877141789553546
# Relative Squared Error (RSE): 0.23112770343458952
