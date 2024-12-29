# Collaborators: Aadem Isai, Jenna Hopkins

import csv
from typing import Any, NamedTuple
from haversine import haversine, Unit
from datastructures.array import Array
from datastructures.graph import Graph
from datastructures.hash_map import HashMap
from datastructures.list_stack import ListStack

class Airport(NamedTuple): 
    """
    Class of the Airport, which contains the airport code, name, id, city, country, latitude, and longitude.
    """
    airport_code : str
    name: str
    id: int
    city: str
    country: str
    latitude: float
    longitude: float

class Flight(NamedTuple):
    """
    Class of the Flight which contains the origin and destination airports. 
    """
    origin: Airport
    destination: Airport

    @property
    def distance(self) -> float:
        """
        Function that calculates the distance between the origin and destination airports.

        Args: None

        Returns:
            float: The distance between the origin and destination airports.
        """
        origin = (self.origin.latitude, self.origin.longitude)
        destination = (self.destination.latitude, self.destination.longitude)
        return haversine(origin, destination, unit = Unit.MILES)

class Dijkstra:
    """
    Class of the primary Dijkstra algorithm that finds the shortest path between two airports.
    """
    def __init__(self, graph: Graph):
        """
        Constructor for the Dijkstra class.

        Args: 
            graph (Graph): The graph of the airports and flights.
        
        Returns:
            None
        """
        self._graph = graph
        self._distances_from_origin = HashMap()
        self._route_connections = HashMap()
        self._shortest_route = ListStack()
        self._airports = HashMap()

        for airport in self._graph.vertices:
            self._airports[airport.vertex_data.airport_code] = airport.vertex_data

        for vertex in self._graph.vertices:
            self._distances_from_origin[vertex.vertex_data] = -1
            self._route_connections[vertex.vertex_data] = None

    def run(self):
        """
        Primary function that runs the Dijkstra algorithm to find the shortest path between two airports.
        Displays the shortest route to the user, and asks if they would like to find another route.

        Args: 
            None
        
        Returns: 
            None
        """
        origin_airport = self.ask_origin_airport()
        destination_airport = self.ask_destination_airport()

        self.find_shortest_paths(origin_airport)

        route = True
        vertex = destination_airport
        while vertex != origin_airport:
            self._shortest_route.push(vertex.airport_code)
            if self._route_connections[vertex] == None:
                print(f"There is no complete route from {origin_airport.airport_code} to {destination_airport.airport_code} exists.")
                route = False
                break
            else:
                vertex = self._route_connections[vertex]

        if route:
            print(f"The shortest route from {origin_airport.airport_code} to {destination_airport.airport_code} is: ")
            previous_airport = origin_airport.airport_code
            while not self._shortest_route.empty:
                next_airport = self._shortest_route.pop()
                print(f"{previous_airport} to {next_airport}")
                previous_airport = next_airport
            print(f"Total Miles: {round(self._distances_from_origin[destination_airport], 2)} miles.")

        play_again = input("Do you want to find another route? (yes or no) ")
        if play_again.lower() == "yes":
            self.run()

        return None
    
    def ask_origin_airport(self) -> Airport:
        """
        Function to ask the user for the origin airport.
        Asks the user for the code of the airport they are going to depart from.

        Args: 
            None
        
        Returns:
            Airport: The origin airport.
        """
        found_origin = False
        while not found_origin:
            origin_airport = input("Please enter the code of the airport you would like to depart from: ").upper()
            if origin_airport in self._airports:
                found_origin = True
                origin_airport = self._airports[origin_airport]
                break
            if not found_origin:
                print(f"{origin_airport} is not available in the chosen route system.")

        return origin_airport
    
    def ask_destination_airport(self) -> Airport:
        """
        Function that asks the user for the destination airport.
        Asks the user for the code of the airport they are going to arrive at.

        Args: 
            None

        Returns:
            Airport: The destination airport.
        """
        found_destination = False
        while not found_destination:
            destination_airport = input("Enter the code of the airport you are going to arrive at. ").upper()
            if destination_airport in self._airports:
                found_destination = True
                destination_airport = self._airports[destination_airport]
                break
            if not found_destination:
                print(f"{destination_airport} is not available in the chosen route system.")

        return destination_airport


    def find_shortest_paths(self, origin):
        """
        Function that finds the shortest path between two airports.

        Args:
            origin (Airport): The origin airport.
        
        Returns: 
            None
        """
        vertex_array = Array(len(self._airports))
        self._route_connections[origin] = None

        self._distances_from_origin[origin] = 0
        index = 0
        for vertex in self._airports.values():
            if vertex != origin:
                self._distances_from_origin[vertex] = -1
            vertex_array[index] = vertex
            index += 1

        while len(vertex_array) != 0:
            minimum_distance_vertex = None
            for vertex in vertex_array:
                if self._distances_from_origin[vertex] > -1:
                    if minimum_distance_vertex == None:
                        minimum_distance_vertex = vertex
                    elif self._distances_from_origin[vertex] < self._distances_from_origin[minimum_distance_vertex]:
                        minimum_distance_vertex = vertex

            for i in range(len(vertex_array)):
                if vertex_array[i] == minimum_distance_vertex:
                    del vertex_array[i]
                    break
            if minimum_distance_vertex == None:
                break

            routes_array = self._graph.edges_from(minimum_distance_vertex)
            for route in routes_array:
                path = self._distances_from_origin[minimum_distance_vertex] + route.weight
                if self._distances_from_origin[route.destination_vertex.vertex_data] == -1 or path < self._distances_from_origin[route.destination_vertex.vertex_data]:
                    self._distances_from_origin[route.destination_vertex.vertex_data] = path
                    self._route_connections[route.destination_vertex.vertex_data] = minimum_distance_vertex



def read_csv(filename: str) -> Graph:
    """
    Function to read the CSV file and create a graph of the airports and flights.

    Args: 
        filename (str): The name of the CSV file.
    
    Returns; 
        Graph: The graph of the airports and flights.
    """
    csv_reader = csv.DictReader(open(filename, encoding = 'utf-8-sig'))
    graph = Graph()
    for row in csv_reader:
        origin_airport = Airport(row["origin_airport_code"], row["origin_airport"], int(row["origin_airport_id"]), row["origin_city"], 
                                 row["origin_country"], float(row["origin_airport_latitude"]),float(row["origin_airport_longitude"]))
        destination_airport = Airport(row["destination_airport_code"], row["destination_airport"], int(row["destination_airport_id"]), row["destination_city"], 
                                      row["destination_country"], float(row["destination_airport_latitude"]), float(row["destination_airport_longitude"]))
        
        flight = Flight(origin_airport, destination_airport)
        weight = flight.distance
        graph.add_edge(origin_airport, destination_airport, flight, weight)

    return graph


def main():
    """
    Function to run the Dijkstra algorithm to find the shortest path between two airports.

    Args: 
        None

    Returns: 
        None
    """
    graph = read_csv("Projects/dijkstra/routes-min.csv")
    shortest_path = Dijkstra(graph)
    shortest_path.run()


if __name__ == "__main__":
    main()






