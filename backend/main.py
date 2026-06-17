from fastapi import FastAPI
import osmnx as ox
import networkx as nx

app = FastAPI()

locations = {
    "Triplicane": (13.058, 80.275),
    "Mylapore": (13.033, 80.269),
    "T Nagar": (13.041, 80.234)
}

print("Loading Chennai road network...")

# Chennai central region
G = ox.graph_from_point(
    (13.045, 80.260),
    dist=12000,
    network_type="drive"
)

print("Road network loaded!")

@app.get("/")
def home():
    return {"status": "Backend Running"}

@app.get("/simulate")
def simulate(from_loc: str, to_loc: str, scenario: str = "none"):

    try:

        graph = G.copy()

        for u, v, k, d in graph.edges(keys=True, data=True):

            base_length = d.get("length", 1)

            if scenario == "road_closure":
                d["length"] = base_length * 2

            elif scenario == "metro_added":
                d["length"] = base_length * 0.7

            elif scenario == "bus_lane":
                d["length"] = base_length * 0.85

        lat1, lon1 = locations[from_loc]
        lat2, lon2 = locations[to_loc]

        origin = ox.distance.nearest_nodes(
            graph,
            X=lon1,
            Y=lat1
        )

        destination = ox.distance.nearest_nodes(
            graph,
            X=lon2,
            Y=lat2
        )

        path = nx.shortest_path(
            graph,
            origin,
            destination,
            weight="length"
        )

        route_coords = []

        # Extract actual road geometry
        for u, v in zip(path[:-1], path[1:]):

            edge_data = graph.get_edge_data(u, v)

            if edge_data:

                edge = list(edge_data.values())[0]

                if "geometry" in edge:

                    xs, ys = edge["geometry"].xy

                    for lat, lon in zip(ys, xs):
                        route_coords.append(
                            [float(lat), float(lon)]
                        )

                else:

                    route_coords.append([
                        float(graph.nodes[u]["y"]),
                        float(graph.nodes[u]["x"])
                    ])

        distance = 0

        for u, v in zip(path[:-1], path[1:]):

            edge_data = graph.get_edge_data(u, v)

            if edge_data:

                edge = list(edge_data.values())[0]

                distance += edge.get("length", 0)

        return {
            "route": route_coords,
            "distance": round(distance, 2),
            "message": f"{scenario} applied successfully"
        }

    except Exception as e:

        return {
            "error": str(e),
            "route": [],
            "distance": 0,
            "message": "Simulation failed"
        }