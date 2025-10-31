# --------------------------------------------------
PART A: Program Usage Instructions
# --------------------------------------------------

    # --------------------------------------------------
    1. How to compile/run this program:

        Hit the run button, or enter  "python2 program.py" into the terminal. You will then be prompted to select a search algorithm by entering 1, 2, or 3, with 1 corresponding to Dijkstra's Algorithm, 2 with Greedy Best-First Search, and 3 with A* Search. Then, enter the start city and goal city. After doing so, the program will display the found path, total distance, number of vertices explroed, number edges evaluated, and execution time. These results will also be saved in the results.txt file. You will be asked if you would like to search another route, in which you can enter "y" for yes or "n" to exit.

    # --------------------------------------------------
    2. Dependencies and setup instructions:

        This program was written in Python. 
        
        The files include:
            - program.py: the main program that has the Dijkstra's Algorithm, Greedy Best-First Search, and A* Search implemenations 
            - graph_impl.py: the implementation of our graph structure
            - graph_interfaces.py: has the interface defintions we use in our implementation
            - vertices_v1.txt: the list of cities and coordinates
            - graph_v2.txt: the edge connections and distances

    # --------------------------------------------------
    3. Example commands showing how to use each algorithm

        Example 1: Dijsktra's Algorithm
            Enter choice (1/2/3): 1
            Enter start city: Portland
            Enter goal city: Eugene

        Examples 2: Greedy Best-First Search
            Enter choice (1/2/3): 2
            Enter start city: Portland
            Enter goal city: Medford

        Example 3: A* Search
            Enter choice (1/2/3): 3
            Enter start city: Portland
            Enter goal city: Burns

    # --------------------------------------------------
    4. At least 3 example runs with different algorithm/route combinations

        You can see many examples of results printed in results.txt,
        but here are the results of the 3 example runs pasted below: 

        Example 1:
            Algorithm: Dijkstra
            Start: Portland
            Goal: Eugene
            Path: Eugene -> Salem -> Portland
            Total distance: 111.00 miles
            Vertices explored: 7
            Edges evaluated: 17
            Execution time: 0.000639 seconds

        Example 2:
            Algorithm: Greedy Best-First Search
            Start: Portland
            Goal: Medford
            Path: Portland -> Newport -> Florence -> Coos_Bay -> Roseburg -> Medford
            Total distance: 397.00 miles
            Vertices explored: 6
            Edges evaluated: 15
            Execution time: 0.000689 seconds

        Example 3:
            Algorithm: A* Search
            Start: Portland
            Goal: Burns
            Path: Portland -> Hood_River -> The_Dalles -> Madras -> Redmond -> Bend -> Burns
            Total distance: 351.00 miles
            Vertices explored: 10
            Edges evaluated: 27
            Execution time: 0.000725 seconds


# --------------------------------------------------
PART B: Algorithm Analysis 
# --------------------------------------------------

    # --------------------------------------------------
    1. Empirical Observations:

        Dijsktra's Algorithm always found the optimal path (the shortest path). However, it always explored more vertices and edges. Greedy Best-First Search was faster and explored fewer vertices, but it sometimes was less optimal by taking a longer route. A* peformed the best overall out of the three algorithms, combining the efficiency from Greedy Best-First Search and the accuracy of Dijkstra's Algorithm. A* was always optimal with fewer vertex explorations for this reason. 

        When it came to shorter routes, such as from Portland to Salem, all three algooirthms gave the same path and similar performances. For longer or diagonal routes though, A* was significantly more efficient due to the heuristic guidance built into its implementation. 

    # --------------------------------------------------
    2. Use Case Analysis:

        Each algorithm is most useful for different cases. Dijkstra's Algorithm is best for smaller maps, or when accuracy is critcial and computation time is not as much of a concern. Greedy Best-First Search is best when it comes to quick, approximate paths where speed is preferred over precision. A* search is likely best for real-world navigation due to its balance of both speed and accuracy.

    # --------------------------------------------------
    3. Runtime Complexity Analysis:

        Dijkstra's Algoirthm has a time complexity of O((V+E) log V), where V is the number of vertices (number of cities) in the dataset, and E is the number of connecting edges (roads). This algorithm explores vertices using a priority queue. Each vertex is insertetd and extracted once, then each edge is relaxed once. Thus, the overall run time is O((V+E) log V).

        A* Search has the same time complexity as Dijkstra's Algorithm, which is O((V+E( log V))). A* uses a priority queue as well, but it adds a heuristic function to help guide its search. In the best case, when the heuristic is more accurate, A* explroes far fewer nodes than Dijkstra does. In the worst case, when the heruistic is poor, A* bhaves more similarly to Dijkstra. 

        Greedy Best-First Search has a time complexity of O(E log V). This algorithm uses a priority queue as well, but it only ranks nodes based on the heuristic, not the total path cost. This makes it much faster for each iteration but it is also less relaible: it may explore fewer vertices but it does not necessairly find the optimal path.

    # --------------------------------------------------
    4. Heuristic Discussion

        The heuristic used in A* and Greedy Best-First Search is the Haversine distance between cities. This is a formula that caculates the great-circle distance between two points on the Earth's surface, using their latitutde and longitude coordinates.

        This heuristic is admissable, meaning that it never overestimeates the true cost from the curent node to the goal. The heuristic's guess is always less than or equal to the actual road distance between two cities. This is a property that guarentees A* will always find the shortest possible path. It also ensures that once A* visists a city, it has already found the shortest path to it and therfore the algorithm does not need to revisit nodes and runs more efficiently. 

        Overall, the Haversine heuristic helps A* prioritize cities that are geographically closer the goal destination. This in turn reduces unnecessary exploration and improves runtime efficiency as compared to Dijkstra's Algorithm, all while still guarenteeing the optimal path.