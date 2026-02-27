import math
import random
import statistics
import matplotlib.pyplot as plt
import os


# =========================================================
# AYARLAR (CONFIG)
# =========================================================

FILES = ["berlin11_modified.tsp", "berlin52.tsp", "kroA100.tsp", "kroA150.tsp"]

POP_SIZE = 60
GENERATIONS = 300
TOURNAMENT_SIZE = 3
MUTATION_TESTS = [0.01, 0.2, 0.5]

SEED = 42
random.seed(SEED)


# =========================================================
# SEHIR SINIFI
# =========================================================

class City:
    def __init__(self, number, x, y):
        self.number = int(number)
        self.x = float(x)
        self.y = float(y)


# =========================================================
# DOSYA OKUMA (TSP PARSER)
# =========================================================

def load_tsp(filename):
    cities = []
    with open(filename, "r") as f:
        start = False
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == "NODE_COORD_SECTION":
                start = True
                continue
            if parts[0] == "EOF":
                break
            if start and len(parts) >= 3:
                cities.append(City(parts[0], parts[1], parts[2]))
    return cities


# =========================================================
# MESAFE VE FITNESS
# =========================================================

def euclidean(c1, c2):
    return math.sqrt((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2)

def fitness(route, city_map):
    dist = 0.0
    for i in range(len(route) - 1):
        dist += euclidean(city_map[route[i]], city_map[route[i+1]])
    dist += euclidean(city_map[route[-1]], city_map[route[0]])
    return dist


# =========================================================
# GREEDY ALGORITMA
# =========================================================

def greedy(cities, city_map, start):
    unvisited = set(c.number for c in cities)
    current = start.number
    route = [current]
    unvisited.remove(current)

    while unvisited:
        nxt = min(
            unvisited,
            key=lambda x: euclidean(city_map[current], city_map[x])
        )
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    return route

def greedy_all(cities, city_map):
    scores = []
    best_route = None
    best_score = float("inf")

    for c in cities:
        r = greedy(cities, city_map, c)
        s = fitness(r, city_map)
        scores.append(s)
        if s < best_score:
            best_score = s
            best_route = r[:]

    return scores, best_route


# =========================================================
# GENETIK ALGORITMA OPERATORLERI
# =========================================================

def tournament(pop, city_map):
    group = random.sample(pop, TOURNAMENT_SIZE)
    return min(group, key=lambda r: fitness(r, city_map))[:]

def ordered_crossover(p1, p2):
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[a:b] = p1[a:b]

    used = set(child[a:b])
    idx = b

    for g in p2:
        if g not in used:
            if idx >= size:
                idx = 0
            child[idx] = g
            idx += 1
    return child

def inversion(route, rate):
    if random.random() < rate:
        i, j = sorted(random.sample(range(len(route)), 2))
        route[i:j] = reversed(route[i:j])
    return route


# =========================================================
# ROTA CIZIMI (VISUALIZE)
# =========================================================

def plot_route(route, city_map, title):
    x, y = [], []

    for cid in route:
        x.append(city_map[cid].x)
        y.append(city_map[cid].y)

    x.append(city_map[route[0]].x)
    y.append(city_map[route[0]].y)

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, '-o', markersize=3)
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


# =========================================================
# GENETIK ALGORITMA ANA FONKSIYONU
# =========================================================

def genetic_algorithm(cities, city_map, greedy_seed, mutation_rate):
    population = [greedy_seed[:]]

    for _ in range(int(POP_SIZE * 0.15)):
        population.append(inversion(greedy_seed[:], 0.6))

    while len(population) < POP_SIZE:
        r = [c.number for c in cities]
        random.shuffle(r)
        population.append(r)

    best = min(population, key=lambda r: fitness(r, city_map))
    best_score = fitness(best, city_map)
    history = [best_score]

    for _ in range(GENERATIONS):
        new_pop = [best[:]]

        while len(new_pop) < POP_SIZE:
            p1 = tournament(population, city_map)
            p2 = tournament(population, city_map)
            child = ordered_crossover(p1, p2)
            child = inversion(child, mutation_rate)
            new_pop.append(child)

        population = new_pop

        current_best = min(population, key=lambda r: fitness(r, city_map))
        current_score = fitness(current_best, city_map)

        if current_score < best_score:
            best_score = current_score
            best = current_best[:]

        history.append(best_score)

    return best_score, best, history


# =========================================================
# DOSYA CALISTIRMA
# =========================================================

def run_file(filename):
    print(f"\nProcessing: {filename}")

    cities = load_tsp(filename)
    city_map = {c.number: c for c in cities}

    greedy_scores, greedy_best = greedy_all(cities, city_map)

    histories = []
    ga_results = []

    for rate in MUTATION_TESTS:
        score, route, history = genetic_algorithm(
            cities, city_map, greedy_best, rate
        )
        histories.append(history)
        ga_results.append((score, route, rate))

    # Learning Curve
    plt.figure(figsize=(10, 6))
    for h, r in zip(histories, MUTATION_TESTS):
        plt.plot(h, label=f"Mutation {r}")
    plt.title(filename)
    plt.xlabel("Generation")
    plt.ylabel("Best Distance")
    plt.legend()
    plt.grid()
    plt.show()

    best_score, best_route, best_rate = min(ga_results, key=lambda x: x[0])

    print(f"Greedy best: {min(greedy_scores):.2f}")
    print(f"GA best: {best_score:.2f} (mutation={best_rate})")

    # VISUALIZE – EN IYI GA ROTASI
    plot_route(
        best_route,
        city_map,
        f"Best GA Route – {filename} (mutation={best_rate})"
    )


# =========================================================
# PROGRAM BASLANGICI
# =========================================================

if __name__ == "__main__":
    for f in FILES:
        run_file(f)
