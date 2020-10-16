import os

import json

import time

from main import *
print("TOTAL images:",len(os.listdir("task3")))

count = 0



for file in os.listdir("task3"):
    print(file)

    if count == 0:
        if str("json") in os.listdir():
            print("exists")
            os.chdir("json")
        else:
            os.mkdir("json")
            os.chdir("json")

    count+=1


    dict1 = {

        "name": "Lisa",
        "designation": "programmer",
        "age": "34",
        "salary": "54000"

    }
    print(count)
    print("task3/"+file)
    d = getDictionary(file)
    #i = input("Press Enter")
    print(d)





    # the json file where the output must be stored
    out_file = open(file.strip(".jpg")+".json", "w")

    json.dump(d, out_file, indent=6)

    out_file.close()