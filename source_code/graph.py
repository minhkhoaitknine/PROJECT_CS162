import get_paths
import get_routes
import get_stops
import math
from pyproj import Transformer

def transform_coordinates(lat, lng):
    transformer = Transformer.from_crs('epsg:4326', 'epsg:3405')
    x, y = transformer.transform(lng, lat)
    return x, y


def calculate_distance(lat1, lng1, lat2, lng2):
    x1, y1 = transform_coordinates(lat1, lng1)
    x2, y2 =transform_coordinates(lat2, lng2)
    return (math.sqrt((x1-x2)**2+(y1-y2)**2))

def Find_Name_Attributes(data,String,Attribute):
    list=[]
    list=data.searchByAttributes(Name=String)
    return getattr(list[0],Attribute)




class Brigde:
    def __init__(self, next_vertex, time, distance):
        self.next = next_vertex
        self.time = time
        self.distance = distance

class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = [[] for _ in range(100000)]

    def add_vertex(self, vertex):
        self.vertices[vertex.StopId] = vertex

    def add_edge(self, start_stop_id, end_stop_id, weight_time, weight_distance):
        self.edges[start_stop_id].append(Brigde(end_stop_id, weight_time, weight_distance))

    
 
def build_graph(stops_data, routes_data):
    graph = Graph()
    for stop_data in stops_data.searchByAttributes():
        graph.add_vertex(stop_data)
        
    for vt in graph.vertices:
        Edges=[]
        for route_no in graph.vertices[vt].GetRoute():
            Edges = routes_data.searchByAttributes(RouteNo=route_no, StartStop=graph.vertices[vt].Name)
        
        for Edge in Edges:
            
            displacement=calculate_distance(graph.vertices[vt].Lat, graph.vertices[vt].Lng,
                                            Find_Name_Attributes(stops_data,Edge.EndStop,'Lat'),
                                            Find_Name_Attributes(stops_data,Edge.EndStop,'Lng'))
            graph.add_edge(vt,Find_Name_Attributes(stops_data,Edge.EndStop,'StopId'),
                           Edge.RunningTime*(displacement/Edge.Distance),Edge.Distance)
        
    return graph



build_graph(get_stops.StopQuery('D:/study/term_2/CS162/Lab/repository/PROJECT_CS162/source_code/stops.json'),
            get_routes.RouteVarQuery('D:/study/term_2/CS162/Lab/repository/PROJECT_CS162/source_code/vars.json'))

    