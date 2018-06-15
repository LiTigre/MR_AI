import csv
import os


PATH = '/Users/li-tigre/Desktop/test_model/'

with open('test_names.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile)
    for file in os.listdir(PATH):
        if file != '.DS_Store':
            if 'T' in file:
                spamwriter.writerow([file] + [1])
            else:
                spamwriter.writerow([file] + [0])

