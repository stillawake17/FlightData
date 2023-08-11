import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Read directly from JSON
df = pd.read_json("/flights_data_2023_08_11.json")
# Ensure the "LandedTime" column is in datetime format
df["LandedTime"] = pd.to_datetime(df["LandedTime"], errors='coerce')

# Finding the date range and the time of the last flight in the dataset
start_date_arr = df["LandedDate"].min()
end_date_arr = df["LandedDate"].max()
last_time_arr = df[df["LandedDate"] == end_date_arr]["LandedTime"].max()

# Extract the minute information
df["Minute"] = df["LandedTime"].dt.minute

# Create a new column to categorize each flight by its time
df["Time_Category"] = "Regular departures"
df.loc[(df["Hour"] == 23) & (df["Minute"] < 30), "Time_Category"] = "Shoulder hour flights"
df.loc[(df["Hour"] == 23) & (df["Minute"] >= 30), "Time_Category"] = "Night hour departures"
df.loc[(df["Hour"] < 6), "Time_Category"] = "Night hour departures"
# New code to categorize the time between 06:00 and 07:00 as shoulder hours
df.loc[(df["Hour"] == 6) & (df["Minute"] < 60), "Time_Category"] = "Shoulder hour flights"

# Count the number of flights for each hour and time category
hourly_arrivals_by_category = df.groupby(["Hour", "Time_Category"]).size().unstack(fill_value=0)

# Sort the index for proper plotting
hourly_arrivals_by_category = hourly_arrivals_by_category.sort_index()

# Mapping colors to each category
color_map = {
    "Shoulder hour flights": "yellow",
    "Night hour departures": "red",
    "Regular departures": "blue"
}

# Plotting the histogram with custom colors
fig, ax = plt.subplots(figsize=(12, 7))
bottoms = [0] * len(hourly_arrivals_by_category)
for category, color in color_map.items():
    bars = ax.bar(hourly_arrivals_by_category.index, hourly_arrivals_by_category[category], 
                  bottom=bottoms, color=color, edgecolor='black', alpha=0.7, label=category)
    bottoms = [i + j for i, j in zip(bottoms, hourly_arrivals_by_category[category])]

#ax.set_title("Hourly Arrivals Categorized by Time")
#ax.set_xlabel("Hour of the Day")
#ax.set_ylabel("Number of Flights")
#ax.legend()
#plt.show()

# Plotting the histogram with the updated title
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(hourly_arrivals.index, hourly_arrivals.values, color=colors_arr, edgecolor='black', alpha=0.7)

# Setting the updated title with the date range, Bristol Airport, and the time of the last flight
ax.set_title(f"Bristol Airport - Number of Plane Landed by Hour ({start_date_arr} to {end_date_arr}, Last Flight at {last_time_arr})")


# Setting labels and legend

ax.set_xlabel("Hour of Day")
ax.set_ylabel("Number of Flights")
ax.set_xticks(range(24))
ax.legend(["Night Time Arrivals", "Regular Arrivals", "Shoulder Hour Arrivals"], loc='upper left')



fig = px.bar(hourly_arrivals_by_category, x=hourly_arrivals_by_category.index, y="Number of Flights", color="Time_Category", title="Hourly Arrivals Categorized by Time")
fig.show()

plt.tight_layout()
plt.show()
