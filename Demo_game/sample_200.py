import pandas
import random

n = 10000 #number of records in file
s = 200 #desired sample size
filename = "/Users/li-tigre/Desktop/data/shuffled_stuff.csv"
skip = sorted(random.sample(range(n),n-s))
df = pandas.read_csv(filename, skiprows=skip)

df.to_csv("/Users/li-tigre/Desktop/MR_AI/Demo_game/random200_7.csv", index=False)
