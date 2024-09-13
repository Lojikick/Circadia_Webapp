import pandas as pd
from subprocess import Popen, PIPE
from sleep_utils.schedule import Sleeper, Optimal, Calendar, Event, adjust
from sleep_utils.sleep_score import sleep_score
import os
import mne
import yasa
import numpy as np
import matplotlib.pyplot as plt


# Step 1: Read EEG data (ASSUMING 'my_hypno.csv' (predicted sleep stages) is available)
# not sure how csv is formatted 
def convert_csv_to_stages(input_csv):
    sample_data = pd.read_csv('sleep_eeg.csv')
    sample_data =sample_data.fillna(0)
    sampling_rate = 256
    ch_names = ['TP9', 'AF7', 'AF8', 'TP10']
    time_series = []
    time_series.append(np.array(sample_data['ch1']))
    time_series.append(np.array(sample_data['ch2']))
    time_series.append(np.array(sample_data['ch3']))
    time_series.append(np.array(sample_data['ch4']))
    time_series = np.array(time_series)
    info = mne.create_info(ch_names,sampling_rate)
    raw = mne.io.RawArray(time_series, info)
    sls = yasa.SleepStaging(raw, eeg_name="TP10", metadata=dict(age=21, male=False))
    y_pred = sls.predict()
    df_pred = pd.DataFrame({'Stage': y_pred})
    sleep_cycles = list(df_pred["Stage"])
    return sleep_cycles


def remove_leading(arr, target_element):
    first_diff_index = np.argmax(arr != target_element)
    return arr[first_diff_index:]
def remove_trailing(arr, target_element):
    # Reverse the array to find the index of the last non-target element
    reversed_arr = arr[::-1]
    
    # Find the first index in the reversed array that is not the target_element
    first_non_target_index = np.argmax(reversed_arr != target_element)
    
    # Slice the original array up to this point from the end
    return arr[:-first_non_target_index] if first_non_target_index > 0 else arr
def calculate_score(n3_p, d_p, w_p):
    n3_score = min(n3_p * (20 / 25), 20)  
    
    d_score = min(n3_p * (60 / 70), 60)  
    
    if w_p <= 10:
        w_score = 20 
    else:
        w_score = max(20 - (w_p - 10) * (20 / 10), 0) 
    total_score = n3_score + d_score + w_score
    return total_score

def calculate_sleep_score(input_csv):
    # Read sleep stages from the text file
    sleep_stages = convert_csv_to_stages(input_csv)
    sleep_stages = np.array(sleep_stages)
    sleep_stages = remove_leading(sleep_stages, 'W')
    sleep_stages = remove_trailing(sleep_stages, 'W')
    w_p = (np.count_nonzero(sleep_stages == "W")/sleep_stages.size) *100
    n1_p = (np.count_nonzero(sleep_stages == "N1")/sleep_stages.size) *100
    n2_p = (np.count_nonzero(sleep_stages == "N2")/sleep_stages.size) *100
    n3_p = (np.count_nonzero(sleep_stages == "N3")/sleep_stages.size) *100
    r_p = (np.count_nonzero(sleep_stages == "R")/sleep_stages.size) *100
    d_p = n2_p + n3_p
    return calculate_score(n3_p,d_p,w_p)

# # Get the current working directory
# current_dir = os.getcwd()

# # Specify the full path to the CSV file
# csv_file_path = os.path.join(current_dir, "petal_eeg.csv")

# # Call the function with the full path to the CSV file
# # convert_csv_to_text(csv_file_path, "my_hypno.txt")

# # convert_csv_to_text("my_hypno.csv", "my_hypno.txt")
# sleep_score_value = calculate_sleep_score(csv_file_path)
# print("Sleep Score:", sleep_score_value)


# # # Step 3: User Input for Sleep Schedule
# # user_input = {
# #     "sleep_data": {
# #         "bedtime": "23:00",
# #         "waketime": "07:00"
# #     }
# # }


# # # Step 4: Adjust Sleep Schedule
# # sleeper = Sleeper(1, sleep_score_value, [24], [7])  # Example sleeper
# # optimal = Optimal()

# # adjusted_bedtimes, adjusted_waketimes = adjust(sleeper, optimal)

# # print("Adjusted Bedtimes:", adjusted_bedtimes)
# # print("Adjusted Waketimes:", adjusted_waketimes)


# ## bed time, wake time, weekly schedule 

# # Step 5: Create Calendar and Display Adjusted Schedule
# calendar = Calendar()

# # Add adjusted sleep schedule to the calendar
# calendar.add_sleep_schedule(sleeper, optimal)

# # Display the adjusted schedule for each day
# for day in range(1, 6):
#     calendar.display_day(f"Day {day}")