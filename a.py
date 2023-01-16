# importing the module
import json
import pandas as pd

# Opening JSON file
with open('static\\web-assets\\data\\flags\\us.json') as json_file:
    data = json.load(json_file)

    flag_data = []
    for key in data.keys():
        flag_data.append([key, data[key]])

    df = pd.DataFrame(flag_data, columns=['state', 'flag'])
    print(df)
    df.to_csv('static\\web-assets\\data\\flags\\us_small.csv',
              index=False, header=True)
