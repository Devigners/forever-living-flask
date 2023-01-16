import csv

# Open the text file
with open('us data.txt', 'r') as f:
    # Read the contents of the file into a list
    lines = f.readlines()

# Open the CSV file
with open('us_data_small.csv', 'w') as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the lines of the text file to the CSV file
    writer.writerows([line.strip().split(', ') for line in lines])
