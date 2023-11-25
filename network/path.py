from network.graph import NeighbourGraphBuilder
from tube.map import TubeMap
import pprint

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide 
      your code into several sub-methods)
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap
        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        self.infinity = float('inf')
        self.undefined = None

    def get_station_id_by_name(self, station_name):
        """
        Get the station id by its name.

        Args:
            station_name (str): The name of the station for which to retrieve the id.

        Returns:
            str: The id of the station with the given name.
            None: If no station is found with the given name.
        """
        
        for station_id, station_obj in self.tubemap.stations.items():
            if station_obj.name == station_name:
                return str(station_id)

        
    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path from start_station_name to end_station_name.
        
        The shortest path is the path that takes the least amount of time.

        For instance, get_shortest_path('Stockwell', 'South Kensington') 
        should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.
        
        You can use the Dijkstra algorithm to find the shortest path from
        start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, 
        e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not 
                exist.
                Returns a list with one Station object (the station itself) if 
                start_station_name and end_station_name are the same.
        """
        # TODO: Complete this method
        start_station_id = self.get_station_id_by_name(start_station_name)
        end_station_id = self.get_station_id_by_name(end_station_name)

        if start_station_id is None or end_station_id is None:
            return None

        if start_station_id == end_station_id:
            return [self.tubemap.stations[start_station_id]]
        
        # Set the distance for the start node to zero and to infinity for all other nodes
        distance = {str(station_id): float('inf') for station_id in self.graph}
        predecessor = {str(station_id): None for station_id in self.graph}
        distance[start_station_id] = 0

        unexplored_nodes = list(self.graph.keys())


        # While there are still nodes to be processed
        while unexplored_nodes:
            current_min_node = min(unexplored_nodes, key= lambda node: distance[node])
            unexplored_nodes.remove(current_min_node)

            if current_min_node == end_station_id:
                break

            for neighbor, connection_data in self.graph[current_min_node].items():
                alt = distance[current_min_node] + min([connection.time for connection in connection_data]) 

                if alt < distance[neighbor]:
                    distance[neighbor] = alt
                    predecessor[neighbor] = current_min_node

        path = []
        station_id = end_station_id

        while start_station_id not in path and station_id is not None:
            path.append(station_id)
            station_id = predecessor[station_id]

        if start_station_id in path:
            return [self.tubemap.stations[p] for p in path[::-1]]
        else:
            #raise ValueError('start_station_id not in path')
            return None 



def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Stockwell", "South Kensington")
    pprint.pp(stations)
    
    station_names = [station.name for station in stations]
    print(station_names)

    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    print(stations)
    
    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected


if __name__ == "__main__":
    test_shortest_path()
