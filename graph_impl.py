from __future__ import annotations
from typing import List, Optional, Tuple, TypeVar
import math
import csv
from graph_interfaces import IEdge, IGraph, IVertex

# Implementation definitions
# You should implement the bodies of the methods required by the interface protocols.

T = TypeVar('T')

# class Graph[T](IGraph[T]):
class Graph(IGraph):

    def __init__(self):
        """Initializes the list of vertices"""
        self._vertices = []

    def get_vertices(self) -> List[IVertex]:
        """Returns all the vertices in self._vertices"""
        return list(self._vertices)
        
    def get_edges(self) -> List[IEdge]:
        """Gets the edges from all of the vertices in self._vertices"""
        edges: List[IEdge] = []
        for v in self._vertices: 
            edges += v.get_edges()
        return edges

    def add_vertex(self, vertex: IVertex) -> None:
        """Adds a vertex to self.vertices"""
        self._vertices.append(vertex)
    
    def remove_vertex(self, vertex_name: str) -> None:
        """This removes a vertex if the input name exists then it removes the edges 
        connected to it """
        for vertex in list(self._vertices):
            if vertex.get_name() == vertex_name:
                self._vertices.remove(vertex)
                continue

            # Account for the edges:
            for edge in list(vertex.get_edges()):
                if edge.get_destination().get_name() == vertex_name:
                    vertex.remove_edge(edge.get_name())

    def add_edge(self,edge: IEdge, from_vertex_name: Optional[str] = None) -> None:
        """ Adds an edge between vertices if they are connected to the same 
        destination """
        if from_vertex_name:
            for vertex in self._vertices:
                if vertex.get_name() == from_vertex_name:
                    vertex.add_edge(edge)
                    break

    def remove_edge(self, edge_name: str) -> None:
        """Iterates through the list of vertices and then their edges
           to see if the edge name exists and then removes the edge"""
        for v in self._vertices:
            for e in list(v.get_edges()):
                if e.get_name() == edge_name:
                    v.remove_edge(edge_name)

    def get_vertex_by_name(self,name: str) -> Optional[IVertex]:
        """ Finds a vertex by name """
        for v in self._vertices:
            if v.get_name().lower() == name.lower():
                return v
        return None

    def load_vertices(self, filename: str) -> None:
        """Loads vertices and coordinates from CSV file"""
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['vertex'].strip()
                lat = float(row['latitude'])
                lon = float(row['longitude'])
                vertex = Vertex(name)
                vertex.set_coordinates(lat, lon)
                self.add_vertex(vertex)

    def load_edges(self, filename: str) -> None:
        """Loads edges from CSV file"""
        import csv
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                src = row['source'].strip()
                dest = row['destination'].strip()
                dist = float(row['distance'])
                src_vertex = self.get_vertex_by_name(src)
                dest_vertex = self.get_vertex_by_name(dest)
                if src_vertex and dest_vertex:
                    edge_name = row['highway'].strip()
                    edge = Edge(edge_name, dest_vertex, dist)
                    src_vertex.add_edge(edge)


class Vertex(IVertex):

    def __init__(self, name: str) -> None:
        """Initialization for Vertex class"""
        self.name = name
        self._edges: List[IEdge[T]] = []
        self._visited: bool = False
        self.lat: float = 0.0
        self.lon: float = 0.0
        self._data: Optional[T] = None

    def get_name(self) -> str:
        """Gets the vertex name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Sets the name of a vertex based on input"""
        self.name = name

    def add_edge(self, edge: IEdge[T]) -> None:
        """Appends an edge to list of edges"""
        self._edges.append(edge)

    def remove_edge(self, edge_name: str) -> None:
        """Removes an edge if the edge name exists in the list of edges""" 
        for e in list(self._edges):
            if e.get_name() == edge_name:
                self._edges.remove(e)

    def get_edges(self) -> List[IEdge]:
        """Gets the list of edges"""
        return list(self._edges)

    def set_visited(self, visited: bool) -> None:
        """Sets whether a vertex has been vistited"""
        self._visited = visited 

    def is_visited(self) -> bool:
        """Checks to see if vertex has been visited"""
        return self._visited

    def set_coordinates(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    def get_coordinates(self) -> Tuple[float, float]:
        """ Returns coordinates (lat, lon) """
        return(self.lat, self.lon)

class Edge(IEdge):
    
    def __init__(self, name: str, destination: IVertex, weight: float = 0) -> None:
        """Initialization for Edge class"""
        self._name = name
        self._destination: IVertex = destination
        self._weight = weight

    def get_name(self) -> str:
        "Gets the name of the edge"
        return self._name
    
    def set_name(self, name: str) -> None:
        """Changes/sets the name of an edge"""
        self._name = name

    def get_destination(self) -> IVertex:
        """Gets the destination """
        return self._destination
    
    def get_weight(self) -> float:
        """Gets the weight of edges"""
        return self._weight
    
    def set_weight(self, weight: float) -> None:
        """Can change or set the weight of an edge"""
        self._weight = weight


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
   radius: int = 3959 # Earth's radius in miles
   lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
   delta_lat: float = lat2 - lat1
   delta_lon: float = lon2 - lon1
   # 'a' is the squared half-chord length between the points
   a: float = math.sin(delta_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon/2)**2
   # 'c' is the angular distance in radians (the central angle)
   c: float = 2 * math.asin(math.sqrt(a))
   return radius * c