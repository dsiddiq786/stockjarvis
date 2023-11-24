import pandas as pd
from datetime import datetime, timedelta,date
import os


""" 
    Step No 3:  (Find Profit & Loss)
    Author : Dawood Siddiq
    Formulas : 
        P1 = Entry Price - Current Time Price 
        P = P1 + P2 + ....
        entry_price = LTP value at User provided Time
"""


folder_path = 'complete_data'
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

dataframes = [pd.read_csv(file, delimiter=',') for file in csv_files]

entry_time = input("Enter the entry time (HH:MM:SS): ")
loss_threshold = float(input("Enter the loss threshold: "))
profit_threshold = float(input("Enter the profit threshold: "))

# entry_time = "14:12:14"
# loss_threshold = -30
# profit_threshold = 18

# Function to calculate value of P= P1+P2+P3+So-On
def calculate_P(entry_prices, current_prices):
    P_values = [entry_price - current_price for entry_price, current_price in zip(current_prices,entry_prices)]
    # print(P_values)
    return sum(P_values)

# First we convert entry_time to datetime object
entry_datetime = datetime.combine(date.today() - timedelta(days=1), datetime.strptime(entry_time, "%H:%M:%S").time())
# print(entry_datetime)

# Then we initialize entry prices with None
entry_prices = [None] * len(dataframes)

# Now Iterate over seconds from entry_time and calculate P value
time_increment = timedelta(seconds=1)
current_time = entry_datetime
# print(current_time)
found_threshold = False

while True:
    current_time_prices = []
    for idx, df in enumerate(dataframes):
        # print(f"Columns in DataFrame {idx + 1}: {df.columns}")

        # Get the current price at current_time from each DataFrame
        current_price = df[df['Time'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")) == current_time]['LTP'].values
        # print(current_price)

        if len(current_price)  > 0:
            current_time_prices.append(float(current_price[0]))
            
            # Check if entry price hasn't been set and current time matches entry time
            if entry_prices[idx] is None and current_time.strftime("%H:%M:%S") == entry_time:
                entry_prices[idx] = float(current_price[0])
        else:
            current_time_prices.append(None)
        # print(entry_prices)
        # print(current_time_prices)
    
    # Check if all entry prices have been found then proceed to calculate value of P
    if all(entry_prices):
        P = calculate_P(entry_prices=entry_prices, current_prices=current_time_prices)
        # print(P)
        
        # Output data if thresholds are met
        if P <= loss_threshold or P >= profit_threshold:
            found_threshold = True
            
            # Form Output Data
            data = {
                'Entry Time': entry_datetime,
                'Threshold Time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                'Loss threshold': loss_threshold,
                'Profit threshold': profit_threshold,
                
            }
            
            # Add DataFrames Entry Prices in following format "P1_entryPrice"
            for i in range(len(entry_prices)):
                diff_key = f'P{i+1}_entryPrice'
                data[diff_key] = entry_prices[i]

            # Now Add DataFrames Difference in following Format P1, P2 , P3 ....
            for i in range(len(entry_prices)):
                diff_key = f'P{i+1}' 
                data[diff_key] = entry_prices[i] - current_time_prices[i]

            # Print the resulting data
            # print(data)
            
            output_df = pd.DataFrame([data])
            output_df.to_csv('threshold_data.csv', index=False)
            break
    
    # Move to the next second to continue the iteration
    current_time += time_increment

    # Break if current time exceeds a certain limit to avoid infinite loop
    if current_time.hour >= 16:
        break

if not found_threshold:
    print("Thresholds not met within the specified time limit.")