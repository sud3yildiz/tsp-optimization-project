import math
import random
import matplotlib.pyplot as plt
import os

FILE_NAME = "kroA150.tsp"


class City:
    def __init__(self, n, x, y): self.number, self.x, self.y = int(n), float(x), float(y)
def read_file(f):
    c = []
    if not os.path.exists(f): return []
    with open(f) as fl:
        lines = fl.readlines()
        sec = False
        for l in lines:
            p = l.split()
            if not p: continue
            if p[0] == "NODE_COORD_SECTION": sec = True; continue
            if p[0] == "EOF": break
            if sec or (p[0].isdigit() and len(p)>=3):
                try: c.append(City(p[0], p[1], p[2]))
                except: continue
    return c
def dist(c1, c2): return math.sqrt((c1.x-c2.x)**2 + (c1.y-c2.y)**2)
def fit(r, d): return sum([dist(d[r[i]], d[r[i+1]]) for i in range(len(r)-1)]) + dist(d[r[-1]], d[r[0]])

def visualize_150():
    cities = read_file(FILE_NAME)
    if not cities: return
    d = {c.number: c for c in cities}
    
    print("Grafikler hazırlanıyor...")
    
    curr = cities[0].number; route = [curr]; unvisited = {c.number for c in cities}; unvisited.remove(curr)
    while unvisited:
        nxt = min(unvisited, key=lambda x: dist(d[curr], d[x]))
        route.append(nxt); unvisited.remove(nxt); curr = nxt
    
    # GA
    pop = [route[:] for _ in range(150)]
    history = []
    best_r = route[:]
    best_s = fit(route, d)
    
    for _ in range(400): # 400 gene
        pop.sort(key=lambda x: fit(x, d))
        if fit(pop[0], d) < best_s: best_s = fit(pop[0], d); best_r = pop[0][:]
        history.append(best_s)
        new_pop = pop[:20]
        while len(new_pop) < 150:
            p = random.choice(pop[:60])[:]
            if random.random() < 0.35:
                i, j = random.sample(range(len(cities)), 2)
                p[i], p[j] = p[j], p[i]
            new_pop.append(p)
        pop = new_pop

   
    plt.figure(figsize=(10,6))
    plt.plot(history, color='red', label='Best Fitness')
    plt.title(f"Learning Curve - {FILE_NAME}")
    plt.xlabel("Epochs"); plt.ylabel("Distance")
    plt.grid(True); plt.legend()
    plt.show() 
    
    # ÇİZİM 2
    x = [d[c].x for c in best_r]; y = [d[c].y for c in best_r]
    x.append(x[0]); y.append(y[0])
    plt.figure(figsize=(8,8))
    plt.plot(x, y, 'o-', color='black', mfc='cyan', markersize=4, linewidth=0.5)
    plt.title(f"Best Route Map - {FILE_NAME}\nScore: {best_s:.2f}")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    visualize_150()