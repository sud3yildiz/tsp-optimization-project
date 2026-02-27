import math
import random
import statistics
import os

FILE_NAME = "kroA150.tsp"  # 150 Şehir

# --- TEMEL ---
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

def run_stats_150():
    print(f"--- ANALİZ: {FILE_NAME} (Büyük Veri) ---")
    cities = read_file(FILE_NAME)
    if not cities: print("Dosya yok!"); return
    d = {c.number: c for c in cities}
    
    # 1. GREEDY
    print("1. Greedy hesaplanıyor...")
    greedy_scores = []
    best_greedy = None
    min_g = float('inf')
    for city in cities:
        curr = city.number; route = [curr]; unvisited = {c.number for c in cities}; unvisited.remove(curr)
        while unvisited:
            nxt = min(unvisited, key=lambda x: dist(d[curr], d[x]))
            route.append(nxt); unvisited.remove(nxt); curr = nxt
        s = fit(route, d)
        greedy_scores.append(s)
        if s < min_g: min_g = s; best_greedy = route[:]
    print(f"   Greedy Ort: {statistics.mean(greedy_scores):.2f}")

    # 2. GA
    print("2. Genetik Algoritma (10 Tekrar) - Sabırlı olun...")
    ga_scores = []
    for run in range(10):
        pop = [best_greedy[:]] 
        for _ in range(149): # 150 Popülasyon
            c = best_greedy[:]; i, j = random.sample(range(150), 2); c[i], c[j] = c[j], c[i]
            pop.append(c)
        
        for _ in range(400): # 400 Epoch (Daha fazla nesil gerekli)
            pop.sort(key=lambda x: fit(x, d))
            new_pop = pop[:20]
            while len(new_pop) < 150:
                p = random.choice(pop[:60])[:]
                if random.random() < 0.35: # Biraz daha yüksek mutasyon
                    i, j = random.sample(range(150), 2)
                    p[i], p[j] = p[j], p[i]
                new_pop.append(p)
            pop = new_pop
        
        b = fit(pop[0], d)
        ga_scores.append(b)
        print(f"   Run {run+1}: {b:.2f}")

    print("-" * 30)
    print(f"SONUÇ ({FILE_NAME}):")
    print(f"GA En İyi: {min(ga_scores):.2f}")
    print(f"GA Ortalama: {statistics.mean(ga_scores):.2f}")
    print(f"GA Std Sapma: {statistics.stdev(ga_scores):.2f}")

if __name__ == "__main__":
    run_stats_150()