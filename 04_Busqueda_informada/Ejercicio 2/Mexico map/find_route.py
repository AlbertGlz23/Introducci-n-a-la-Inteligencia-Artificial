import argparse
import heapq
import json
import math
import sys


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def astar(start_id, goal_id, graph, cities_by_id):
    start_lat, start_lon = (
        cities_by_id[start_id]["lat"],
        cities_by_id[start_id]["lon"],
    )
    goal_lat, goal_lon = (
        cities_by_id[goal_id]["lat"],
        cities_by_id[goal_id]["lon"],
    )

    h_start = haversine(start_lat, start_lon, goal_lat, goal_lon)
    frontier = [(h_start, 0, start_id, [start_id])]
    g_scores = {start_id: 0}

    while frontier:
        f, g, current, path = heapq.heappop(frontier)

        if current == goal_id:
            return g, path

        if g > g_scores.get(current, float("inf")):
            continue

        for neighbor, edge_cost in graph[current]:
            tentative_g = g + edge_cost
            if tentative_g < g_scores.get(neighbor, float("inf")):
                g_scores[neighbor] = tentative_g
                n_lat, n_lon = (
                    cities_by_id[neighbor]["lat"],
                    cities_by_id[neighbor]["lon"],
                )
                h = haversine(n_lat, n_lon, goal_lat, goal_lon)
                f_score = tentative_g + h
                heapq.heappush(
                    frontier, (f_score, tentative_g, neighbor, path + [neighbor])
                )

    return float("inf"), []


def resolve_city_name(query_name, data_nodes):
    matches = [node for node in data_nodes if node["name"].strip().lower() == query_name.strip().lower()]

    if len(matches) == 0:
        print(f"Error: La ciudad '{query_name}' no se encontró en el grafo.")
        sys.exit(1)
    elif len(matches) > 1:
        print(f"\nError: El nombre '{query_name}' es ambiguo. Coincide con {len(matches)} ciudades:")
        for m in matches:
            print(f"  - ID: {m['id']} | {m['name']}, {m['state']}")
        print("Por favor especifica la ciudad de forma única.")
        sys.exit(1)

    return matches[0]["id"]


def main():
    parser = argparse.ArgumentParser(description="Calcula la ruta más corta usando A* y Haversine.")
    parser.add_argument("--from-city", required=True, help="Nombre de la ciudad de origen")
    parser.add_argument("--to", required=True, help="Nombre de la ciudad de destino")
    args = parser.parse_args()

    with open("mexico_cities_graph.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    cities_by_id = {node["id"]: node for node in data["nodes"]}

    start_id = resolve_city_name(args.from_city, data["nodes"])
    goal_id = resolve_city_name(args.to, data["nodes"])

    graph = {node["id"]: [] for node in data["nodes"]}
    for edge in data["edges"]:
        u, v, weight = edge["source"], edge["target"], edge["km"]
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    total_cost, path_ids = astar(start_id, goal_id, graph, cities_by_id)

    path_names = [f"{cities_by_id[nid]['name']} ({cities_by_id[nid]['state']})" for nid in path_ids]
    
    print(f"\nRuta: {' -> '.join(path_names)}")
    print(f"Costo total: {total_cost:.2f} km")


if __name__ == "__main__":
    main()