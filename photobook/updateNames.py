#script to update js dictionary with thumbnail filenames

import os
from PIL import Image

cwd = os.getcwd()
# List of filenames
fileNames = [f for f in os.listdir(f"{cwd}/") if str(f)[-3:].lower() == "jpg"]

fileDict = {name:Image.open(f"{cwd}/{name}")._getexif()[36867] for name in fileNames}
#print(fileDict)

# Writing names to python
nameFile = open(f"{cwd}/nameFile.js", "w+")
nameFile.write("var DATA = {")
for key in fileDict.keys():
    nameFile.write(f"\"{key}\":\"{fileDict[key]}\"")
    nameFile.write(",")
nameFile.write("}")
nameFile.close()
