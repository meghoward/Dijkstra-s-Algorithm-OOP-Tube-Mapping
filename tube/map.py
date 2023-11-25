import json
from .components import Station, Connection, Line
from math import ceil, floor

class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id 
      (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id 
      (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap 
      (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances

    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During the import process, the `stations`, `lines` and `connections` 
        attributes should be updated.

        You can use the `json` python package to easily load the JSON file at 
        `filepath`

        Note: when the indicated zone is not an integer (for instance: "2.5"), 
            it means that the station belongs to two zones. 
            For example, if the zone of a station is "2.5", 
            it means that the station is in both zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to 
                import. If filepath is invalid, no attribute should be updated, 
                and no error should be raised.

        Returns:
            None
        """
        # TODO: Complete this method
        with open(filepath, "r") as json_file: 
            data = json.load(json_file)

            for line in data['lines']:
                self.lines[line['line']] = Line(id = str(line['line']), name = str(line["name"]))

            for station in data['stations']:
                try:
                    station['zone'] = {int(station['zone'])}
                    self.stations[station['id']] = Station(str(station["id"]), str(station["name"]), station["zone"])
                
                except:
                    station_zones = {int(floor(float(station['zone']))), int(ceil(float(station['zone'])))}
                    self.stations[station['id']] = Station(str(station["id"]), str(station["name"]), station_zones)

            for connection in data['connections']:
                self.connections.append(Connection(stations = [self.stations[connection['station1']],
                                                           self.stations[connection["station2"]]],
                                                           line = self.lines[connection["line"]], 
                                                           time =int(connection["time"])))

    

def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print("stations", tubemap.stations[list(tubemap.stations)[0]])
    print("272, Vauxhall: ", tubemap.stations['272'] )
    
    # # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # # view the first Connection
    print(tubemap.connections[0])
    
    # # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])
    print("Station 11: ", tubemap.stations["11"], "Station 163: ", tubemap.stations["163"])


if __name__ == "__main__":
    test_import()

