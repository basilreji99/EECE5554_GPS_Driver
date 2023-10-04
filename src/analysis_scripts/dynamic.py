
# importing pandas library
import pandas as pd
# importing matplotlib library
import matplotlib.pyplot as plt

dynamic_df = pd.read_csv (r'/home/basilreji/catkin_ws/src/data/moving-gps.csv')

plt.title("Dynamic GPS Plot")
plt.xlabel("UTM Easting")
plt.ylabel("UTM Northing")

easting1, northing1 = dynamic_df[".UTM_easting"] / dynamic_df[".UTM_easting"].max(), dynamic_df[".UTM_northing"] / dynamic_df[".UTM_northing"].max()
plt.scatter(easting1, northing1, color = 'b')
plt.show()

