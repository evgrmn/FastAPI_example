f = open("/home/rmn/1/fastAPI/FastAPI_example/config/data.json")
print(f)

import os

#to get the current working directory
directory = os.getcwd()

print(directory)

with open('config/data.json') as user_file:
    file_contents = user_file.read()

print(file_contents)