
# importing pandas library
import pandas as pd
# importing matplotlib library
import matplotlib.pyplot as plt

static_df = pd.read_csv (r'/home/basilreji/catkin_ws/src/data/Stand-gps.csv')


plt.title("Static GPS Plot")
plt.xlabel("UTM Easting")
plt.ylabel("UTM Northing")

easting, northing = static_df[".UTM_easting"] / static_df[".UTM_easting"].max(), static_df[".UTM_northing"] / static_df[".UTM_northing"].max()
plt.scatter(easting, northing, color = 'r')


plt.show()



