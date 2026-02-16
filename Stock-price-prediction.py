import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Prompt the user to enter a time frame
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Define the ticker symbol for a JSE stock, e.g., "SHP.JO" for Shoprite Holdings Ltd.
ticker_symbol = "SHP.JO"

# Fetch stock data
stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Preprocess the data
# Use only the 'Adj Close' column for LSTM
data = stock_data['Adj Close'].values.reshape(-1, 1)

# Scale the data to be between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Prepare the data for the LSTM model
X_train = []
y_train = []
time_step = 15  # Use 15 days to predict the next day

# Ensure there is enough data to form at least one sequence
if len(scaled_data) > time_step:
    for i in range(time_step, len(scaled_data)):
        X_train.append(scaled_data[i-time_step:i, 0])
        y_train.append(scaled_data[i, 0])
else:
    print("Not enough data to form sequences. Consider using a smaller time_step.")

# Check if X_train and y_train are not empty
if len(X_train) > 0 and len(y_train) > 0:
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Reshape the data to be [samples, time steps, features] for LSTM
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    # Compile and train the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, batch_size=1, epochs=10)  # Increased epochs

    # Predict the prices for the given data
    predictions = model.predict(X_train)
    predictions = scaler.inverse_transform(predictions)

    # Calculate daily returns based on the predicted prices
    predicted_returns = np.diff(predictions.flatten()) / predictions[:-1].flatten()

    # Calculate the volatility (standard deviation of the predicted returns)
    predicted_volatility = np.std(predicted_returns)

    # Annualize the volatility (assuming 252 trading days in a year)
    annualized_predicted_volatility = predicted_volatility * np.sqrt(252)

    # Plot the actual vs predicted prices (optional)
    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['Adj Close'], label='Actual Prices')
    plt.plot(stock_data.index[time_step:], predictions, label='Predicted Prices')
    plt.title(f"{ticker_symbol} Stock Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

    # Output the predicted volatility
    print(f"\nThe annualized volatility of {ticker_symbol} from {start_date} to {end_date} based on LSTM predictions is: {annualized_predicted_volatility:.4f}")
else:
    print("X_train or y_train is empty. Check the data or reduce the time_step.")import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Prompt the user to enter a time frame
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Define the ticker symbol for a JSE stock, e.g., "SHP.JO" for Shoprite Holdings Ltd.
ticker_symbol = "SHP.JO"

# Fetch stock data
stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Preprocess the data
# Use only the 'Adj Close' column for LSTM
data = stock_data['Adj Close'].values.reshape(-1, 1)

# Scale the data to be between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Prepare the data for the LSTM model
X_train = []
y_train = []
time_step = 15  # Use 15 days to predict the next day

# Ensure there is enough data to form at least one sequence
if len(scaled_data) > time_step:
    for i in range(time_step, len(scaled_data)):
        X_train.append(scaled_data[i-time_step:i, 0])
        y_train.append(scaled_data[i, 0])
else:
    print("Not enough data to form sequences. Consider using a smaller time_step.")

# Check if X_train and y_train are not empty
if len(X_train) > 0 and len(y_train) > 0:
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Reshape the data to be [samples, time steps, features] for LSTM
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    # Compile and train the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, batch_size=1, epochs=10)  # Increased epochs

    # Predict the prices for the given data
    predictions = model.predict(X_train)
    predictions = scaler.inverse_transform(predictions)

    # Calculate daily returns based on the predicted prices
    predicted_returns = np.diff(predictions.flatten()) / predictions[:-1].flatten()

    # Calculate the volatility (standard deviation of the predicted returns)
    predicted_volatility = np.std(predicted_returns)

    # Annualize the volatility (assuming 252 trading days in a year)
    annualized_predicted_volatility = predicted_volatility * np.sqrt(252)

    # Plot the actual vs predicted prices (optional)
    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['Adj Close'], label='Actual Prices')
    plt.plot(stock_data.index[time_step:], predictions, label='Predicted Prices')
    plt.title(f"{ticker_symbol} Stock Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

    # Output the predicted volatility
    print(f"\nThe annualized volatility of {ticker_symbol} from {start_date} to {end_date} based on LSTM predictions is: {annualized_predicted_volatility:.4f}")
else:
    print("X_train or y_train is empty. Check the data or reduce the time_step.")
