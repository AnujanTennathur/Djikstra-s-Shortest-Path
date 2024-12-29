from __future__ import annotations
from typing import Any

from datastructures.array import Array
from datastructures.linked_list import LinkedList
from datastructures.hash_map import HashMap

class Graph:
    """ Class Graph. Represents a graph data structure containing
            vertices and edges.
        Depends on Edge and Vertex classes.
        Stipulations:
        1. Must adhere to the docstring requirements per method, including raising
            raising appropriate exceptions where indicated.
    """
    def __init__(self) -> None:
        """Create an empty graph.
        
        Examples:
            >>> graph = Graph()
            
        Returns:
            None    
        """
        self._vertices: HashMap = HashMap()

    @property
    def vertices(self) -> Array:
        """Return the vertices of the graph.
        
        Examples: 
            >>> graph = Graph()
            >>> graph.add_vertex("Portland")
            >>> graph.vertices
            [Portland]
            
        Returns:
            list[Vertex]: The vertices of the graph.
        """
        vertices = Array(len(self._vertices))
        for i, vertex in enumerate(self._vertices.values()):
            vertices[i] = vertex

        return vertices

    def add_vertex(self, vertex_data: Any) -> None:
        """Add a vertex to the graph.
        
        Examples:
            >>> graph = Graph()
            >>> graph.add_vertex("Portland")
            >>> graph.add_vertex("Salem")
            >>> graph.vertices
            [Portland, Salem]
        
        Args:
            vertex_data (Any): The vertex data for the vertex to add to the graph.
            
        Returns:
            None
            
        """
        self._vertices[vertex_data] = _Vertex(vertex_data)

    def remove_vertex(self, vertex_data: Any) -> None:
        """Remove a vertex from the graph.
        
        Examples:
            >>> graph = Graph()
            >>> graph.add_vertex(Vertex("Portland"))
            >>> graph.add_vertex(Vertex("Salem"))
            >>> graph.remove_vertex(Vertex("Portland"))
            >>> graph.vertices
            [Salem]

        Args:
            vertex (Vertex): The vertex to remove from the graph.

        Returns:
            None

        Raises:
            ValueError: If the vertex is not in the graph.
        """
        del self._vertices[vertex_data]

    def add_edge(self, vertex1_data: Any, vertex2_data: Any, edge_data: Any, weight: Any) -> None:
        """Add an edge between two vertices with the given weight. The vertices will be added if they do not exist.
        
        Examples:
            >>> graph = Graph()
            >>> graph.add_edge("Portland", "Salem", "I-5", 50)
            >>> graph.edges_from("Portland")
            [Salem via I-5 (50)]

        Args:
            vertex1_data (Any): The data of the first vertex.
            vertex2_data (Any): The data of the second vertex.
            edge_data (Any): The data of the edge.
            weight (Any): The weight of the edge.
        """
        vertex1: _Vertex | None = None
        vertex2: _Vertex | None = None

        if vertex1_data not in self._vertices:
            vertex1 = _Vertex(vertex1_data)
            self._vertices[vertex1_data] = vertex1
        else:
            vertex1 = self._vertices[vertex1_data]
        
        if vertex2_data not in self._vertices:
            vertex2 = _Vertex(vertex2_data)
            self._vertices[vertex2_data] = vertex2
        else:
            vertex2 = self._vertices[vertex2_data]
            
        edge = _Edge(vertex2, edge_data, weight)
        vertex1.add_edge(edge)

    def remove_edge(self, vertex1_data: Any, vertex2_data: Any, edge_data:Any) -> None:
        """Remove an edge between two vertices. The vertices will not be removed.
        
        Examples:
            >>> graph = Graph()
            >>> graph.add_edge("Portland", "Salem", "I-5", 50)
            >>> graph.add_edge("Portland", "Salem", "Hwy 99", 59)
            >>> graph.edges_from("Portland")
            [Salem via I-5 (50), Salem via Hwy 99 (59)]
            >>> graph.remove_edge("Portland", "Salem", "I-5")
            >>> graph.edges_from("Portland")
            [Salem via Hwy 99 (59)]

        Args:
            vertex1_data (Vertex): The data of the first vertex.
            vertex2_data (Vertex): The data of the second vertex.
            edge_data (Any): The data of the edge.

        Returns:
            None

        Raises: 
            ValueError: If either vertex does not exist or the edge does not exist between the two vertices.
        """
        vertex1: _Vertex | None = None
        vertex2: _Vertex | None = None
        edge : _Edge | None = None

        for vertex in self._vertices:
            if vertex.data == vertex1_data:
                vertex1 = vertex
            elif vertex.data == vertex2_data:
                vertex2 = vertex
        
        if vertex1 is None or vertex2 is None:
            raise ValueError("Vertex not found")
        
        for e in vertex1.edges:
            if e.destination_vertex == vertex2 and e.data == edge_data:
                edge = e

        if edge is None:
            raise ValueError("Edge not found")
        
        vertex1.remove_edge(edge)

    def edges_from(self, vertex_data: Any) -> Array:
        """Return the edges from the given vertex.
        
        Examples:
            >>> graph = Graph()
            >>> graph.add_vertex("Portland")
            >>> graph.add_vertex("Salem")
            >>> graph.add_edge("Portland", "Salem", "I-5", 50)
            >>> graph.edges_from("Portland")
            [I-5]

        Args:
            vertex_data (Any): The data of the vertex.

        Returns:
            Array[Any]: The data from the edges from the vertex.

        Raises:
            ValueError: If the vertex is not in the graph.
        """

        if vertex_data in self._vertices:
            vertex = self._vertices[vertex_data]
            edges = Array(len(vertex.edges))
            for i, edge in enumerate(vertex.edges):
                edges[i] = edge
            return edges
        
        raise ValueError("Vertex not found")
        
    def get_destination_vertex(self, edge_data: Any) -> Any:
        """Return the destination vertex of the given edge.
        
        Examples:
            >>> graph = Graph()
            >>> graph.add_vertex("Portland")
            >>> graph.add_vertex("Salem")
            >>> graph.add_edge("Portland", "Salem", "I-5", 50)
            >>> graph.get_destination_vertex("I-5")
            Salem

        Args:
            edge_data (Any): The data of the edge.

        Returns:
            Any: The destination vertex of the edge.

        Raises:
            ValueError: If the edge is not found.
        """
        

        for vertex in self._vertices:
            for edge in vertex.edges:
                if edge.edge_data == edge_data:
                    return edge.destination_vertex.vertex_data
        
        raise ValueError("Edge not found")

    def __str__(self) -> str:
        """Return a string representation of the graph.
        
        Examples:
            >>> graph = Graph()
            >>> graph.add_vertex(Vertex("Portland"))
            >>> graph.add_vertex(Vertex("Salem"))
            >>> str(graph)
            [Portland, Salem]
        """

        return f"{self._vertices}"

    def __repr__(self) -> str:
        """Return a string representation of the graph.
        
        Examples:
            >>> graph = Graph()
            >>> graph.add_vertex(Vertex("Portland"))
            >>> graph.add_vertex(Vertex("Salem"))
            >>> repr(graph)
            [Portland, Salem]
        """
        return str(self)

class _Vertex:
    """A vertex in a graph."""
    def __init__(self, vertex_data: Any=None):
        """Create a vertex with the given value.
        
        Examples:
            >>> vertex = Vertex("Portland")
            >>> vertex.vertex_data
            Portland
            >>> vertex.edges
            []
            
        Args:
            vertex_data (Any): The data of the vertex.

        Returns:
            None
        """
        self._vertex_data = vertex_data
        self._edges = LinkedList()

    @property
    def vertex_data(self) -> Any:
        """Return the data of the vertex.
        
        Examples:
            >>> vertex = Vertex("Portland")
            >>> vertex.vertex_data
            Portland
            
        Returns:
            Any: The data of the vertex.
        """
        return self._vertex_data
    
    @vertex_data.setter
    def vertex_data(self, vertex_data) -> None:
        """Set the data of the vertex.
        
        Examples:
            >>> vertex = Vertex("Portland")
            >>> vertex.vertex_data = "Salem"
            >>> vertex.vertex_data
            Salem

        Args:
            vertex_data (Any): The data of the vertex.

        Returns:
            None
        """
        self._vertex_data = vertex_data

    @property
    def edges(self) -> LinkedList:
        """Return the edges of the vertex.
        
        Examples:
            >>> vertex = Vertex("Portland")
            >>> vertex.edges
            []

        Returns:
            Array[Edge]: The edges of the vertex.
        """
        return self._edges

    def add_edge(self, edge: _Edge) -> None:
        """Add an edge to the vertex.
        
        Examples:
            >>> vertex = Vertex("Portland")
            >>> vertex.add_edge(Edge(Vertex("Salem"), 100))
            >>> vertex.edges

        Args:
            edge (Edge): The edge to add to the vertex.

        Returns:
            None
        """
        self._edges.append(edge)

    def remove_edge(self, edge: _Edge) -> None:
        """Remove an edge from the vertex.
        
        Examples:
            >>> vertex = Vertex("Portland")
            >>> vertex.add_edge(Edge(Vertex("Salem"), 100))

        Args:
            destination_vertex (Vertex): The destination vertex of the edge.

        Returns:
            None

        Raises:
            ValueError: If the edge is not found.
        """
        if edge not in self._edges:
            raise ValueError("The edge is not in the Vertex")

        self._edges.extract(edge)
        
    
    def get_edge(self, destination_vertex: _Vertex) -> _Edge:
        """Return the edge to the given destination vertex.
        
        Examples:   
            >>> vertex = Vertex("Portland")
            >>> vertex.add_edge(Edge(Vertex("Salem"), 100))
            >>> vertex.get_edge(Vertex("Salem"))
            Edge(Vertex("Salem"), 100)

        Args:
            destination_vertex (Vertex): The destination vertex of the edge.

        Returns:
            Edge: The edge to the given destination vertex.

        Raises: 
            ValueError: If the edge is not found.
        """
        for edge in self._edges:
            if edge.destination_vertex == destination_vertex:
                return edge
        
        raise ValueError("Edge not found")

    def __str__(self) -> str:
        """Return a string representation of the vertex.
        
        Examples:
            >>> vertex = Vertex("Portland")
            >>> print(vertex)
            Vertex with value Portland
            
        Returns:
            str: A string representation of the vertex.
        """
        return f"Vertex with value {self._vertex_data}"

    def __repr__(self) -> str:
        """Return a string representation of the vertex.
        
        Examples:
            >>> vertex = Vertex("Portland")
            >>> repr(vertex)
            Vertex with value Portland
            
        Returns:
            str: A string representation of the vertex.    
        """
        return f"Vertex({self._vertex_data})"
    
class _Edge:
    """An edge in a graph."""
    def __init__(self, destination_vertex: _Vertex, edge_data: Any, weight: Any) -> None:
        """Create an edge to the given vertex with the given weight.

        Examples:
            >>> edge = Edge(Vertex("Portland"), 100)
            >>> edge.destination_vertex
            Portland
            >>> edge.weight
            100
        
        Args:
            destination_vertex (Vertex): The destination vertex of the edge.
            weight (Any): The weight of the edge.
            
        Returns:
            None
        """
        self._destination_vertex: _Vertex = destination_vertex
        self._edge_data: Any = edge_data
        self._weight: Any = weight

    @property
    def destination_vertex(self) -> _Vertex:
        """Return the destination vertex of the edge.
        
        Examples:
            >>> edge = Edge(Vertex("Portland"), 100)
            >>> edge.destination_vertex
            Portland
            
        Returns:
            Vertex: The destination vertex of the edge.
        """
        return self._destination_vertex

    @property
    def weight(self) -> Any:
        """Return the weight of the edge.
        
        Examples:
            >>> edge = Edge(Vertex("Portland"), 100)
            >>> edge.weight
            100
            
        Returns:
            Any: The weight of the edge.
        """
        return self._weight

    @destination_vertex.setter
    def destination_vertex(self, destination_vertex: _Vertex) -> None:
        """Set the destination vertex of the edge.
        
        Examples:
            >>> edge = Edge(Vertex("Portland"), 100)
            >>> edge.destination_vertex = Vertex("Salem")
            >>> edge.destination_vertex
            Salem

        Args:
            destination_vertex (Vertex): The destination vertex of the edge.

        Returns:
            None
        """
        self._destination_vertex = destination_vertex

    @weight.setter
    def weight(self, weight: Any) -> None:
        """Set the weight of the edge.
        
        Examples:
            >>> edge = Edge(Vertex("Portland"), 100)
            >>> edge.weight = 200
            >>> edge.weight
            200
            
        Args:
            weight (Any): The weight of the edge.
        """
        self._weight = weight
    
    @property
    def edge_data(self) -> Any:
        """Return the edge data of the edge.

        Examples:
            >>> edge = Edge(Vertex("Portland"), 100, "I-5")
            >>> edge.edge_data
            I-5

        Returns:
            Any: The edge data of the edge.
        """
        return self._edge_data
    
    @edge_data.setter
    def edge_data(self, edge_data) -> None:
        """Set the edge data of the edge.
        
        Examples:
            >>> edge = Edge(Vertex("Portland"), 100, "I-5")
            >>> edge.edge_data = "I-205"
            >>> edge.edge_data
            I-205

        Args:
            edge_data (Any): The edge data of the edge.

        Returns:
            None
        """
        self._edge_data = edge_data

    def __str__(self) -> str:
        """Return a string representation of the edge.
        
        Examples:
            >>> edge = Edge(Vertex("Portland"), 100)
            >>> str(edge)
            Edge to Portland with weight 100
        
        Returns:
            str: A string representation of the edge.
        """
        return f"Edge to {self._destination_vertex} with weight {self._weight}"

    def __repr__(self) -> str:
        """Return a string representation of the edge.
        
        Examples:
            >>> edge = Edge(Vertex("Portland"), 100)
            >>> repr(edge)
            Edge to Portland with weight 100
            
        Returns:
            str: A string representation of the edge.
        """
        return str(self)
