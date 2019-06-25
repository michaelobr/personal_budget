import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open("June").sheet1

def quick_look():
    # Get all expense categories from the sheet, omitting "Total"
    categories = sheet.col_values(2)
    categories.remove("Total")

    # Get each category's sum, omitting the total amount once again
    category_sum = sheet.col_values(1)[:-1]

    # Convert the category_sum list elements into floats from strings (need to strip $)
    category_sum = [float(s[1:]) for s in category_sum]

    # Enumerate through the lists
    for i, ele in enumerate(categories):
        print(categories[i], ": $", category_sum[i], sep="")

    print("Total: $", sum(category_sum), sep="")

# Pandas method
columns = sheet.col_values(2)
columns.remove("Total")

counter = 1
row_array = []
for i in columns:
    row = sheet.row_values(counter)[2:]
    row_array.append(row)
    counter += 1

df = pd.DataFrame(row_array, columns).T
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

'''plt.figure(figsize=(9, 3))
for name, index in enumerate(columns):
    plt.bar(name, row_array[name])
plt.suptitle('Categorical Plotting')
plt.show()'''