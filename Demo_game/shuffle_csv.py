import random
fid = open("/Users/li-tigre/Desktop/data/test_names.csv", "r")
li = fid.readlines()
fid.close()
print(li)

random.shuffle(li)
print(li)

fid = open("/Users/li-tigre/Desktop/data/shuffled_stuff.csv", "w")
fid.writelines(li)
fid.close()