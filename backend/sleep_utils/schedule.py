import numpy as np
from datetime import datetime, timedelta
### HELPER FUNCTIONS ###

## CONVERSIONS ##

def d_to_s(time):
    temp = dec_to_m(time)
    return military_to_standard(temp)

# Function to convert military time (24-hour) to standard time (12-hour AM/PM)
def s_to_d(time):
    temp = standard_to_military(time)
    return m_to_dec(temp)

def standard_to_military(time_str):
  
    # Parse the time in the "2:00 PM" format
    t = datetime.strptime(time_str, "%I:%M %p")

    # Convert to military time (24-hour)
    return t.strftime("%H:%M")

# Function to convert military time (24-hour) to standard time (12-hour AM/PM)
def military_to_standard(time_str):
    # Parse the time in the "14:00" format
    t = datetime.strptime(time_str, "%H:%M")
    # Convert to standard time (12-hour AM/PM)
    return t.strftime("%I:%M %p")

def m_to_dec(time_str):
    # Split the time into hours and minutes
    hours, minutes = map(int, time_str.split(":"))
    
    # Convert minutes to a fraction of an hour
    decimal_minutes = minutes / 60
    
    # Combine the whole hours and fractional minutes
    decimal_time = hours + decimal_minutes
    
    return decimal_time

def dec_to_m(decimal_time):
    # Separate the whole hours and fractional part
    hours = int(decimal_time)
    fractional_part = decimal_time - hours
    
    # Convert the fractional part to minutes
    minutes = round(fractional_part * 60)  # Rounding to get a whole number
    
    # Format hours and minutes to ensure proper military time
    formatted_hours = f"{hours:02d}"  # Pad with zero if single-digit
    formatted_minutes = f"{minutes:02d}"  # Pad with zero if single-digit
    
    # Combine hours and minutes to get military time
    military_time = f"{formatted_hours}:{formatted_minutes}"
    
    return military_time

## TIME COMPUTATIONS ##

def time_to_seconds(time_str):
    dt = datetime.strptime(time_str, "%H:%M")
    return dt.hour * 3600 + dt.minute * 60

# Calculate the mean in seconds
def mean_time(times):
    total_seconds = sum(time_to_seconds(t) for t in times)
    mean_seconds = total_seconds / len(times)

    # Convert the mean back to HH:MM
    mean_time = (datetime.min + timedelta(seconds=mean_seconds)).time()
    mean_time_str = mean_time.strftime("%H:%M")
    rounded_time = nearest_quarter(m_to_dec(mean_time_str))
    return rounded_time

### MAIN FUNCTIONS ###

class Sleeper:
    def __init__(self, id, sleepscore, bedtimes, waketimes):
        self.id = id
        self.sleepscore = sleepscore
        self.bedtime = mean_time(bedtimes)
        self.waketime = mean_time(waketimes)

class Optimal(Sleeper):
    def __init__(self):
        super().__init__(0, 100, ["23:00"], ["8:00"])

def get_coef(score):
    k = 0
    if score >= 90:
        return 0.9
    elif score >= 75:
        return 0.7
    elif score >= 50:
        return 0.5
    elif score >= 30:
        return 0.3
    else:
        return 0.2
    
def nearest_quarter(time):
    # Extract the hour and minute part
    hour = int(time)
    minute_fraction = abs(time - hour)
    
    # Convert the minute fraction to a full number representing minutes
    minutes = minute_fraction * 60
    
    # Round the minutes to the nearest quarter (15, 30, 45, 0)
    if minutes % 15 < 7.5:
        rounded_minutes = 15 * (minutes // 15)
    else:
        rounded_minutes = 15 * ((minutes // 15) + 1)
    
    # Adjust if rounding over 60 minutes
    if rounded_minutes >= 60:
        hour += 1
        rounded_minutes = 0
    
    # Convert back to the decimal representation (hour.minute)
    rounded_time = hour + (rounded_minutes / 60.0)
    
    return rounded_time


def adjust(user, optimal):
    # Initial lists for adjusted bedtimes and waketimes
    new_bedtimes, new_waketimes = [], []
    k = get_coef(user.sleepscore)
    print(user.waketime)
    print(optimal.waketime)
    for i in range(1, 6):  # Day 1 through Day 5
        # Calculate a tentative adjustment
        adj_bedtime = optimal.bedtime 
        
        adj_waketime = optimal.waketime + ((user.waketime - optimal.waketime) * np.exp(-k*i))
        
        # Ensure adj_waketime is within 24-hour format
            
        new_bedtimes.append(adj_bedtime)
        new_waketimes.append(adj_waketime)
    
    # Ensure the function returns lists even if adjustments are not needed
    new_waketimes = list(map(nearest_quarter,new_waketimes))
    return new_bedtimes, new_waketimes

class Event:
    def __init__(self, label, start_time, end_time):
        self.label = label
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"{self.label}: {self.start_time} - {self.end_time}"

class Calendar:
    def __init__(self):
        self.days = {}  # Each key is a day (e.g., '2023-04-07'), value is a list of Event objects

    def add_event(self, day, event):
        if day not in self.days:
            self.days[day] = []
        self.days[day].append(event)
        self.days[day].sort(key=lambda x: x.start_time)  # Ensure events are sorted by start time

    def add_sleep_schedule(self, sleeper, optimal):
        new_bedtimes, new_waketimes = adjust(sleeper, optimal)
        for i, (bedtime, waketime) in enumerate(zip(new_bedtimes, new_waketimes), start=1):
            day_label = f"Day {i}"
            bedtime_event = Event("Bedtime", f"{int(bedtime)}:{int((bedtime % 1) * 60):02d}", f"{int(bedtime)}:{int((bedtime % 1) * 60):02d}")
            waketime_event = Event("Waketime", f"{int(waketime)}:{int((waketime % 1) * 60):02d}", f"{int(waketime)}:{int((waketime % 1) * 60):02d}")
            self.add_event(day_label, bedtime_event)
            self.add_event(day_label, waketime_event)

    def display_day(self, day):
        if day in self.days:
            print(f"Events on {day}:")
            for event in self.days[day]:
                print(event)
        else:
            print(f"No events scheduled for {day}.")

# Assuming the Sleeper and Optimal classes and adjust function are defined as previously

# Example usage
# calendar = Calendar()
# sleeper = Sleeper(1, 85, [23, 23.5, 24], [7, 7.5, 8])  # Initial bedtime and waketime averages
# optimal = Optimal()

# calendar.add_sleep_schedule(sleeper, optimal)

# # Display the schedule for each day
# for day in range(1, 6):
#     calendar.display_day(f"Day {day}")
