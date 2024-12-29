The Dijkstra algorithm is a tool used to find the shortest distance between two different vertices, or points, within a graph structure. This is done through calculating different "weights," or distances, back and forth from specific locations. 

Dijkstra's algorithm functions by visiting vertices within the graph starting from the starting vertex. Then, the algorithm selects an unvisited vertex with the shortest distance from the current vertex, checks the other unvisited vertices from that vertex, and constantly updates the neighbor distances if the distance is smaller. Thus, the algorithm essentially repeats this process until the absolute shortest distance between vertices in the graph is found. 

With an established understanding of the Dijkstra algorithm itself, the project implementation utilizes a weighted graph in the form of airport routes. For the purpose of efficiency and reduced wait time, I used the routes-min.csv file, which is a smaller file of airports and flights. 

Each airport has a airport code, id, and city. The airport code is the representational abbreviation of the airport, like SFO for San Francisco, and PDX for Portland. When the program runs, the user is asked to select the airport they want to depart and arrive at, and are prompted to enter the code of the airport (SFO, PDX, PHX, etc). Once both origin and destination airports have been confirmed, the algorithm ensures a route exists within the routes file (if not informs user that route is not available), and then proceeds to use dijkstra's algorithm (as described above) to calculate the shortest route available. It then displays this route to the reader, along with the total distance. Finally, user is asked if they want to find another route, and if no, the game quits. 

Here is an example of the algorithm running: 
Please enter the code of the airport you would like to depart from. PDX
Please enter the code of the airport you would like to arrive at. DFW
The shortest route from PDX to DFW is as follows: 
PDX to EUG
EUG to DEN
DEN to DFW
Total Miles: 1740.88 miles.

And that is a summary of the Dijkstra algorithm project. Thank you for reading. 

