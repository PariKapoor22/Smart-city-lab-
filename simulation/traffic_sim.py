import osmnx as ox
import networkx as nx


def get_graph(area):

    points = {
        "Triplicane": (13.055, 80.275),
        "Mylapore": (13.033, 80.268),
        "T Nagar": (13.041, 80.233)
    }

    point = points.get(area, (13.055, 80.275))

    G = ox.graph_from_point(
        point,
        dist=1500,
        network_type="drive"
    )

    return G


def apply_scenario(G, scenario):

    if scenario == "road_closure":
        # simulate congestion increase
        for u, v, k, data in G.edges(keys=True, data=True):
            data["length"] *= 1.3

    elif scenario == "metro_added":
        # simulate reduced travel cost
        for u, v, k, data in G.edges(keys=True, data=True):
            data["length"] *= 0.8

    elif scenario == "bus_lane":
        for u, v, k, data in G.edges(keys=True, data=True):
            data["length"] *= 0.9

    return G


def get_shortest_route(area, scenario):

    G = get_graph(area)
    G = apply_scenario(G, scenario)

    start = (13.0545, 80.2740)
    end = (13.0600, 80.2810)

    start_node = ox.distance.nearest_nodes(G, X=start[1], Y=start[0])
    end_node = ox.distance.nearest_nodes(G, X=end[1], Y=end[0])

    route = nx.shortest_path(
        G,
        start_node,
        end_node,
        weight="length"
    )

    route_coords = []

    for node in route:
        d = G.nodes[node]
        route_coords.append((d["y"], d["x"]))

    distance = nx.shortest_path_length(
        G,
        start_node,
        end_node,
        weight="length"
    )

    # 🧠 IMPACT ANALYSIS (this is your “virtual world” logic)
    impact = {}

    if scenario == "none":
        impact = {
            "message": "Baseline city conditions"
        }

    elif scenario == "road_closure":
        impact = {
            "message": "Road congestion increased due to closure",
            "effect": "Travel cost increased ~30%"
        }

    elif scenario == "metro_added":
        impact = {
            "message": "Metro reduces dependency on roads",
            "effect": "Travel cost reduced ~20%"
        }

    elif scenario == "bus_lane":
        impact = {
            "message": "Bus priority improves efficiency",
            "effect": "Travel cost reduced ~10%"
        }

    return route_coords, round(distance, 2), impact