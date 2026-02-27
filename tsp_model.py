import matplotlib.pyplot as plt

def plot_route(route, city_map, title):
    x = []
    y = []

    for city_id in route:
        x.append(city_map[city_id].x)
        y.append(city_map[city_id].y)

    
    x.append(city_map[route[0]].x)
    y.append(city_map[route[0]].y)

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, '-o', markersize=4)
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()
