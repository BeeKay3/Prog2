import json
import os



content = []


for file in os.listdir("."):
    if file.endswith(".json") and file != "team_Artiom_Bikalpa_Seifalislam.json": 
        with open(file, "r") as readFile:
            content.append(json.load(readFile))
            readFile.close()

print("All members of the team (Common JSON-file content):")
for element in content:
    print(element)

with open("team_Artiom_Bikalpa_Seifalislam.json", "w") as outputFile:
    json.dump(content, outputFile, indent=1)
    outputFile.close()

    

print("\n\nJob's done!")