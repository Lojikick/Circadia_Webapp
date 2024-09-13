from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yasa
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
# CORS(app)

@app.route('/')
def home():
    # f = np.load('data_full_6hrs_100Hz_Cz+Fz+Pz.npz')
    # data, ch_names = f['data'], f['chan']
    # sf = 100.
    # times = np.arange(data.size) / sf

    # data_cz = data[0, :]
    # hypno_30s = np.loadtxt('data_full_6hrs_100Hz_hypno_30s.txt')
    # hypno = yasa.hypno_upsample_to_data(hypno=hypno_30s, sf_hypno=(1/30), data=data, sf_data=sf)

    # fig = yasa.plot_spectrogram(data_cz, sf, hypno=hypno, fmax=30, cmap='Spectral_r', trimperc=5)
    # Convert intervals to minutes
    weights = {
    'dips_n3': 20,
    'falling_deep_sleep': 15,
    'time_each_stage': 15,
    'times_awake': -8,
    'total_sleep_duration': 12,
    'percentage_deep_sleep': 20
    }
    
    stages_data = np.loadtxt('data_full_6hrs_100Hz_hypno_30s.txt')
    stages_data = list(stages_data)
    total_intervals = len(stages_data)
    total_minutes = total_intervals/2

    # Count occurrences of sleep stages
    n3_count = stages_data.count(3)
    n3_dips = stages_data.count(0) - 1  # transitions from non-N3 to N3

    # Find the index of the first occurrence of N3
    first_n3_index = stages_data.index(3) if 3 in stages_data else total_intervals

    # Calculate the time spent in each sleep stage
    time_n1 = stages_data[:first_n3_index].count(1) / 2
    time_n2 = stages_data[:first_n3_index].count(2) / 2
    time_n3 = n3_count / 2
    time_rem = stages_data.count(4) / 2

    # Calculate total sleep duration
    total_sleep_duration = time_n1 + time_n2 + time_n3 + time_rem

    # Count the number of awakenings
    num_awakenings = sum(1 for i in range(1, total_intervals) if stages_data[i] == 0 and stages_data[i - 1] != 0)

    # Calculate percentage of deep sleep
    percentage_deep_sleep = (time_n3 / total_minutes) * 100

    # Calculate the sleep quality score based on the rubric
    sleep_score = (
        (n3_dips * (weights['dips_n3'] / 15)) +
        ((first_n3_index / 2) * (weights['falling_deep_sleep'] / 10)) +
        (((time_n1 / total_minutes) * 100) * (weights['time_each_stage'] / 25)) +
        (((time_n2 / total_minutes) * 100) * (weights['time_each_stage'] / 25)) +
        (((time_n3 / total_minutes) * 100) * (weights['time_each_stage'] / 25)) +
        (((time_rem / total_minutes) * 100) * (weights['time_each_stage'] / 25)) +
        (num_awakenings * weights['times_awake']) +
        ((total_sleep_duration / 2) * (weights['total_sleep_duration'] / 20)) +
        (percentage_deep_sleep * (weights['percentage_deep_sleep'] / 25))
    )

    return str(sleep_score)
if __name__ == '__main__':
    app.run(debug=True)  
    
