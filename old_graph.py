from __future__ import annotations
from typing import Dict, List, Optional


class vertex:
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._edges: List[edge] = []

    def get_name(self) -> str: return self._name
    def set_name(self, name: str) -> None: self._name = name

    def add_edge(self, edge_to_add: edge) -> None:
        self._edges.append(edge_to_add)

    def remove_edge(self, edge_name: str) -> None:
        for edge in self._edges:
            if edge.get_name() == edge_name:
                self._edges.remove(edge)
                return

class edge:
    def __init__(self, name: str, destination: vertex) -> None:
        self._name: str = name
        self._destination: Optional[vertex] = destination
        self._is_bi_directional: bool = False

    def get_name(self) -> str: return self._name
    def set_name(self, name:str) -> None: self._name = name


class graph:

    VERTEX_COUNT = 10

    def __init__(self) -> None:
        self._vertices: List[vertex] = []

    def add_vertex(self, name: str) -> None:
        self._vertices.append(vertex(name))

    def add_edge(self, name: str, from_vertex_name: str, to_vertex_name: str) -> None:
        # 1. Find the vertex from object reference
        # 2. Find the vertex to object reference
        from_vertex: Optional[vertex] = None
        to_vertex: Optional[vertex] = None

        for vertex in self._vertices:
            if vertex.get_name() == from_vertex_name:
                from_vertex = vertex

            if vertex.get_name() == to_vertex_name:
                to_vertex = vertex
        
        if from_vertex is None or to_vertex is None:
            raise Exception("One or more of the vertexes do not exist")

        the_edge = edge(name, to_vertex)
        from_vertex.add_edge(the_edge)

        second_edge = edge(name, from_vertex)
        to_vertex.add_edge(second_edge)


        
        pass

        self._adj_list: Dict[str, List[str]] = {}

        # Preallocated
        self._adj_matrix_prepopulated:List[List[int]] = [[int()] * graph.VERTEX_COUNT] * graph.VERTEX_COUNT

        # Run time allocation
        self._adj_matrix_dynamic: List[List[int]] = [[]]




