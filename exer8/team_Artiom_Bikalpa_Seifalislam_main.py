import requests
import matplotlib.pyplot as plt
import json
import threading

class weather:
    def __init__(self, lat, lon, start, end, zone, city):
        self.url = "https://archive-api.open-meteo.com/v1/era5?latitude={}&longitude={}&start_date={}&end_date={}&daily=temperature_2m_mean&timezone={}".format(lat, lon, start, end, zone)
        self.city = city

    def getData(self, store):
        response = requests.get(self.url)
        data = response.json()["daily"]
        
        sum = data["temperature_2m_mean"][0]
        n = 1
        self.data = {}
        for x in range(1, len(data["time"])):
            if "01" == data["time"][x][-2:]:
                avg = sum/n
                self.data.update({data["time"][x-1][:7]: avg})
                store.add(self.city, data["time"][x-1][:7], avg)
                sum = data["temperature_2m_mean"][x]
                n = 1
            else:
                sum += data["temperature_2m_mean"][x]
                n += 1

class jsonFile:
    def __init__(self, c):
        self.cities = c
        self.data = {c[0]:{}, c[1]:{}, c[2]:{}}

    def add(self, c1, key, value):
        self.data[c1].update({key: value})

    def save(self, name):
        with open(name, "w") as File:
            try:
                json.dump(self.data, File, indent=4)
            except PermissionError:
                print("Insufficient permissions to save file")

class graph:
    def __init__(self, t):
        self.fig, self.ax = plt.subplots(figsize=(16,9))
        plt.title("Temperature")
        plt.xlabel("Month")
        plt.ylabel("Average Temperature (Celcius)")
        plt.xticks(rotation=45)
        plt.grid(True)
        self.t = t

    def add(self, x, name):
        self.ax.plot(self.t, x, label=name)

    def show(self):
        plt.legend(loc="upper right")
        plt.show()

lat = 27.71, 47.02, 31.20
lon = 85.32, 28.84, 29.89
cities = 'Kathmandu', 'Chisinau', 'Alexandria'
start = "2024-04-01"
end = "2025-04-01"
zone = "Europe/Berlin"

w1 = weather(lat[0], lon[0], start, end, zone, cities[0])
w2 = weather(lat[1], lon[1], start, end, zone, cities[1])
w3 = weather(lat[2], lon[2], start, end, zone, cities[2])
f = jsonFile(cities)

t1 = threading.Thread(target=w1.getData, args=(f,))
t2 = threading.Thread(target=w2.getData, args=(f,))
t3 = threading.Thread(target=w3.getData, args=(f,))
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()

f.save("team_Artiom_Bikalpa_Seifalislam_results.json")

g = graph(w1.data.keys())
g.add(w1.data.values(), w1.city)
g.add(w2.data.values(), w2.city)
g.add(w3.data.values(), w3.city)
g.show()

