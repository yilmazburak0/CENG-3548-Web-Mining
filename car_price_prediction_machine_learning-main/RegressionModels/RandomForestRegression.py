import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

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

# Initialize the Random Forest Regressor with 300 trees
rf = RandomForestRegressor(n_estimators=300, random_state=22)

# Train the model on the training data
rf.fit(x_train, y_train)

# Import metrics to evaluate the model
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Make predictions on the test data
y_pred = rf.predict(x_test)

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
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Calculate the Relative Absolute Error (RAE)
rae = mean_absolute_error(y_test, y_pred) / mean_absolute_error(y_test, [np.mean(y_test)] * len(y_test))
print(f"Relative Absolute Error (RAE): {rae}")

# Calculate the Relative Squared Error (RSE)
rse = mean_squared_error(y_test, y_pred) / mean_squared_error(y_test, [np.mean(y_test)] * len(y_test))
print(f"Relative Squared Error (RSE): {rse}")

# Results with n_estimators=100
# Modelin R^2 skoru: 0.9955716825678157
# Modelin Ortalama Kare Hatası (MSE): 456496995.5943135
# Modelin Ortalama Mutlak Hatası (MAE): 4534.536611872146
# Root Mean Squanred Error (RMSE): 21365.790310548156
# Relative Absolute Error (RAE): 0.020449254632269313
# Relative Squared Error (RSE): 0.004428317432184307

# Results with n_estimators=200
# Modelin R^2 skoru: 0.9957029781207071
# Modelin Ortalama Kare Hatası (MSE): 442962278.0977332
# Modelin Ortalama Mutlak Hatası (MAE): 4523.841809448542
# Root Mean Squanred Error (RMSE): 21046.669049940734
# Relative Absolute Error (RAE): 0.020401024624063076
# Relative Squared Error (RSE): 0.004297021879292954

# Results with n_estimators=300
# Modelin R^2 skoru: 0.9956826795792677
# Modelin Ortalama Kare Hatası (MSE): 445054771.08720475
# Modelin Ortalama Mutlak Hatası (MAE): 4516.443237384381
# Root Mean Squanred Error (RMSE): 21096.32126905553
# Relative Absolute Error (RAE): 0.02036765952041409
# Relative Squared Error (RSE): 0.004317320420732284
