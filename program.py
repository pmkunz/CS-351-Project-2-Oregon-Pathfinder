from typing import Optional, List, Tuple
from graph_impl import Graph, Vertex, Edge, haversine_distance
from graph_interfaces import IGraph, IVertex, IEdge

import time
import itertools
import heapq
import csv
import os


def build_graph() -> Graph:
    """ loads vertices and edges from files into a Graph object """
    graph = Graph()
    graph.load_vertices("vertices_v1.txt")
    graph.load_edges("graph_v2.txt")
    return graph

def dijkstra(graph: Graph, start_name: str, goal_name: str) -> Tuple[List[str], float]:
    """ Finds the shortest path using Dijkstra's algorithm """
    
    start_time = time.perf_counter()
    start = graph.get_vertex_by_name(start_name)
    goal = graph.get_vertex_by_name(goal_name)
    if not start or not goal:
        return [], float('inf'), 0, 0, 0.0

    distances = {v.get_name(): float('inf') for v in graph.get_vertices()}
    previous = {v.get_name(): None for v in graph.get_vertices()}
    distances[start.get_name()] = 0

    counter = itertools.count()
    pq = [(0, next(counter), start)]  #(distance, vertex)
    vertices_explored = 0
    edges_evaluated = 0

    while pq:
        current_dist, _, current_vertex = heapq.heappop(pq)
        vertices_explored += 1

        if current_vertex.get_name() == goal.get_name():
            break

        for edge in current_vertex.get_edges():
            edges_evaluated += 1
            neighbor = edge.get_destination()
            new_dist = current_dist + edge.get_weight()

            if new_dist < distances[neighbor.get_name()]:
                distances[neighbor.get_name()] = new_dist
                previous[neighbor.get_name()] = current_vertex.get_name()
                heapq.heappush(pq, (new_dist, next(counter), neighbor))

    # Reconstruct path:
    path = []
    current = goal.get_name()
    while current:
        path.insert(0, current)
        current = previous[current]
    path.reverse()

    end_time = time.perf_counter()

    return path, distances[goal.get_name()], vertices_explored, edges_evaluated, end_time - start_time


def greedy_best_first(graph: Graph, start_name: str, goal_name: str) -> Tuple[List[str], float]:
    """ Finds a path using Greedy Best-First Search """
    
    start_time = time.perf_counter()
    start = graph.get_vertex_by_name(start_name)
    goal = graph.get_vertex_by_name(goal_name)
    if not start or not goal:
        return [], float('inf'), 0, 0, 0.0

    counter = itertools.count()
    came_from = {start.get_name(): None}
    visited = set()
    vertices_explored = 0
    edges_evaluated = 0

    # straight-line distance to goal
    goal_lat, goal_lon = goal.get_coordinates()
    start_lat, start_lon = start.get_coordinates()
    start_h = haversine_distance(start_lat, start_lon, goal_lat, goal_lon)

    pq = [(start_h, next(counter), start)] # priority queue stores (heuristic, count, vertex)

    while pq:
        _, _, current = heapq.heappop(pq)
        vertices_explored += 1

        if current.get_name() == goal.get_name():
            break

        visited.add(current.get_name())

        for edge in current.get_edges():
            edges_evaluated += 1
            neighbor = edge.get_destination()
            if neighbor.get_name() not in visited:
                lat, lon = neighbor.get_coordinates()
                h = haversine_distance(lat, lon, goal_lat, goal_lon)
                came_from[neighbor.get_name()] = current.get_name()
                heapq.heappush(pq, (h, next(counter), neighbor))

    # Reconstruct path:
    path = []
    current = goal.get_name()
    while current:
        path.append(current)
        current = came_from.get(current)
    path.reverse()

    # Compute the total distance (actual path edges):
    total_dist = 0.0
    for i in range(len(path) - 1):
        v1 = graph.get_vertex_by_name(path[i])
        v2 = graph.get_vertex_by_name(path[i + 1])
        for e in v1.get_edges():
            if e.get_destination().get_name() == v2.get_name():
                total_dist += e.get_weight()
                break

    end_time = time.perf_counter()
    return path, total_dist, vertices_explored, edges_evaluated, end_time - start_time


def a_star(graph: Graph, start_name: str, goal_name: str) -> Tuple[List[str], float]:
    """ Finds the optimal path using A* search """
    
    start_time = time.perf_counter()
    start = graph.get_vertex_by_name(start_name)
    goal = graph.get_vertex_by_name(goal_name)
    if not start or not goal:
        return [], float('inf'), 0, 0, 0.0

    goal_lat, goal_lon = goal.get_coordinates()
    
    counter = itertools.count()
    pq = [(0, next(counter), start)]
    g_scores = {v.get_name(): float('inf') for v in graph.get_vertices()}
    g_scores[start.get_name()] = 0
    came_from = {start.get_name(): None}

    vertices_explored = 0
    edges_evaluated = 0

    while pq:
        _, _, current = heapq.heappop(pq)
        vertices_explored += 1

        if current.get_name() == goal.get_name():
            break

        for edge in current.get_edges():
            edges_evaluated += 1
            neighbor = edge.get_destination()
            tentative_g = g_scores[current.get_name()] + edge.get_weight()

            if tentative_g < g_scores[neighbor.get_name()]:
                came_from[neighbor.get_name()] = current.get_name()
                g_scores[neighbor.get_name()] = tentative_g
                neighbor_lat, neighbor_lon = neighbor.get_coordinates()
                f_score = tentative_g + haversine_distance(neighbor_lat, neighbor_lon, goal_lat, goal_lon)
                heapq.heappush(pq, (f_score, next(counter), neighbor))

    # Reconstruct path:
    path = []
    current = goal.get_name()
    while current:
        path.append(current)
        current = came_from.get(current)
    path.reverse()

    end_time = time.perf_counter()
    return path, g_scores[goal.get_name()], vertices_explored, edges_evaluated, end_time - start_time


def main() -> None:
    graph = build_graph()

    while True: 
        print("Select search algorithm:")
        print("1. Dijkstra's Algorithm")
        print("2. Greedy Best-First Search")
        print("3. A* Search")
        choice = input("Enter choice (1/2/3): ").strip()

        start = input("Enter start city: ").strip()
        goal = input("Enter goal city: ").strip()

        if choice == '1':
            algoname = "Dijkstra"
            path, dist, v_count, e_count, elapsed = dijkstra(graph, start, goal)
        elif choice == '2':
            algoname = "Greedy Best-First Search"
            path, dist, v_count, e_count, elapsed = greedy_best_first(graph, start, goal)
        elif choice == '3':
            algoname = "A* Search"
            path, dist, v_count, e_count, elapsed = a_star(graph, start, goal)
        else:
            print("Invalid choice.")
            return

        if not path:
            print("No path found.")
        else:
            print("\nPath found:")
            print(" -> ".join(path))
            print(f"Total distance: {dist:.2f} miles")
            print(f"Vertices explored: {v_count}")
            print(f"Edges evaluated: {e_count}")
            print(f"Execution time: {elapsed:.6f} seconds")

        # Save results to text file:
        results_file = "results.txt"
        with open(results_file, "a") as f:
            f.write(f"Algorithm: {algoname}\n")
            f.write(f"Start: {start}\n")
            f.write(f"Goal: {goal}\n")
            f.write(f"Path: {' -> '.join(path)}\n")
            f.write(f"Total distance: {dist:.2f} miles\n")
            f.write(f"Vertices explored: {v_count}\n")
            f.write(f"Edges evaluated: {e_count}\n")
            f.write(f"Execution time: {elapsed:.6f} seconds\n")
            f.write("-" * 50 + "\n")

        again = input("\nSearch another route? (y/n): ").strip().lower()
        if again != 'y':
            print("Thank you for using the Oregon Pathfinder!")
            break

if __name__ == "__main__":
    main()