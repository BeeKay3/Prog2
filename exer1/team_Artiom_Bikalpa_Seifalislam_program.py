import json

file1 = open("Bikalpa_Khachhibhoya.json", "r")
file2 = open("Artiom_Triboi.json", "r")
file3 = open("Seifalislam_Sebak.json", "r")
file4 = open("team_Artiom_Bikalpa_Seifalislam.json", "w+")

data1 = json.load(file1)
data2 = json.load(file2)
data3 = json.load(file3)
final = {"teamMembers" : [data1, data2, data3]}
print(type(final))  

json.dump(final, file4, indent = 4)

file4.seek(0)
for x in file4.readlines():
    print(x, end = "")

file1.close()
file2.close()
file3.close()
file4.close()
