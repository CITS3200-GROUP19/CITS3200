# Imports
import pandas as pd


# Data positions
# Right eye positions
right_eye_data_map = [22, 6, 7, 12, 13, 14, 20, 21, 23, 29, 30, 31, 32, 33, 25, 8, 9, 15, 16, 17, 24, 26, 27, 34, 35, 36, 37, 55, 44, 45, 46, 47, 54, 56, 57, 63, 64, 65, 70, 71, 52, 39, 40, 41, 42, 43, 50, 51, 53, 60, 61, 62, 68, 69]
# Left eye positions
left_eye_data_map = [25, 9, 8, 17, 16, 15, 27, 26, 24, 38, 37, 36, 35, 34, 22, 7, 6, 14, 13, 12, 23, 22, 20, 33, 32, 31, 30, 52, 43, 42, 41, 40, 53, 51, 50, 62, 61, 60, 69, 68, 55, 48, 47, 46, 45, 44, 57, 56, 54, 65, 64, 63, 70, 71]



# Function that takes which eye it is and the static point data
# and populates a dictionary with this data as the values and the positions
# as keys
# eye argument = data.iloc[0, ?], 0 for left and 1 for right eye
# data argument = split_data, this is the staticpointdata that has been processed
def map_to_dict(eye, data, left_eye_dict, right_eye_dict):
    i = 0
    # If left eye
    if eye == '0':
        for key in left_eye_data_map:
            left_eye_dict[key] = data[i]
            i = i + 1
        print(left_eye_dict)
    # If right eye
    elif eye == '1':
        for key in right_eye_data_map:
            right_eye_dict[key] = data[i]
            i = i + 1
        print("yeet", right_eye_dict)

