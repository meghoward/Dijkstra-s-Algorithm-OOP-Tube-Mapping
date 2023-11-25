class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code 
      into several sub-methods, if needed)
    """

    def __init__(self):
        pass

    def build(self, tubemap):
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building 
                the graph.

        Returns:
            graph (dict) : as described above. 
                If the input data (tubemap) is invalid, 
                the method should return an empty dict.
        """
        # TODO: Complete this method

        # I need to create a dictionary entry for each station id.
        master_dictionary = {}
        
        # For station obj in my tubemap
        for station_id, station_obj in tubemap.stations.items():
            station_connections = {}

            # For each connection in tubemap.connections
            for connection in tubemap.connections:

                # Ok so first I want to find all of the connection instances that include this station id
                if station_obj in connection.stations:
                    station_1, station_2 = connection.stations
                    if station_1 == station_obj:
                        station_neighbor = station_2
                    else:
                        station_neighbor = station_1

                    if station_neighbor.id not in station_connections.keys():
                        station_connections[station_neighbor.id] = []
                    else:
                        station_connections[station_neighbor.id].append(connection) 

            master_dictionary[station_id] = station_connections
        return master_dictionary                            
 
def test_graph():
    try:
        from tube.map import TubeMap
    except:
        import sys
        sys.path.append('..')
        from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print('\n\n', graph['110'], '\n\n')




if __name__ == "__main__":
    test_graph()
