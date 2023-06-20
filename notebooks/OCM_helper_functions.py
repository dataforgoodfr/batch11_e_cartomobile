import pyproj
from shapely.ops import transform

import requests
from requests.adapters import HTTPAdapter
import urllib3
from urllib3 import Retry

session = requests.Session()
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
session.headers.update(headers)
adapter = HTTPAdapter(max_retries=Retry(total=10, backoff_factor=1))
session.mount("http://", adapter)
session.mount("https://", adapter)

def get_(url):
    response = session.get(url.strip())
    return response.json()
# GET COORDINATES FROM CITY NAME

def get_place_polygon(county,city, country):
    url  =  'https://nominatim.openstreetmap.org/search?'
    # url += f'q={adress}%2C+'
    url += f'city={city}&'
    url += f'country={country}&'
    url += f'county={county}&'


    url +=  'format=geojson&polygon_geojson=1'
    return get_(url)

def proj_lambert(geometry, crs, to_crs):
    gdf = gpd.GeoDataFrame(geometry=[geometry], crs=crs)
    # gdf_proj = project_gdf(gdf, to_crs=to_crs, to_latlong=to_latlong)
    gdf_proj = gdf.to_crs(to_crs)

    geometry_proj = gdf_proj["geometry"].iloc[0]
    return geometry_proj

import polyline
from shapely.geometry import Point,Polygon

class ChargingStation:
    def __init__(self, feature_collection, idx=0):
        AddressInfo = feature_collection['AddressInfo']
        Connections = feature_collection['Connections']

        self.AddressInfo = AddressInfo # dict
        self.Connections = Connections # list of dicts

        self.id = feature_collection['ID']
        self.uuid = feature_collection['UUID']
        self.provider = feature_collection['DataProvider']['Title']
        self.address = AddressInfo['AddressLine1']
        self.gps = Point(AddressInfo['Longitude'], AddressInfo['Latitude'])
        self.lmbrt = proj_lambert(self.gps, crs=4326, to_crs=2154)
        self.nbr_connections = len(Connections)
        # try:
        #     self.level = Connections[idx]['Level']['IsFastChargeCapable'] 
        # except:
        #     self.level = None
        # try:
        #     self.power = Connections[idx]['PowerKW'] 
        # except:
        #     self.power = 0
        # try:
        #     self.type = Connections[idx]['CurrentType']['Title']
        # except:
        #     self.type = None



def request_openchargemap(querystring, output=-1):
    url = "https://api.openchargemap.io/v3/poi"
    headers = {"Accept": "application/json"}
    
    with requests.Session() as s:
        response = s.get(url, headers=headers, params=querystring)
    # print(response, end='\r')

    if response.status_code == 200:
        # display(response.content)
        try:
            datas = response.json()
        except:
            datas = {}

        if datas != {}:    
            # list of available infos
            if output > -1:
                for n, data in enumerate(datas):
                    for key in data.keys():
                        if n == output : print(f'[{n}]-key {key} : {data[key]}')
            
            # list of charging stations
            charging_stations = []
            count = 0
            for n, data in enumerate(datas):
                plugs = len(data['Connections'])
                if output > -1: print(f'{n + 1} with {plugs} plugs / {len(datas)} stations')
                if data['DataQualityLevel'] >0:
                    # TODO handle data quality
                    for n in range(plugs):
                        count += 1
                        charging_stations.append(
                            ChargingStation( data, idx=n )
                        )
            # try:
            #     print(f'Number of total plugs: {count}')   
            # except:
            #     raise Exception('No charging stations returned')
            if len(charging_stations) > 0:
                return charging_stations 
            else:
                return []   #raise Exception('No valid charging stations found')
        else:
            return []     #raise Exception(response.text)
    return[]


import time

def get_charging_stations(area, maxresults=5000):

    querystring = {
        "maxresults": f"{maxresults}",
        "countrycode": "80",
        # "latitude": string
        # "longitude": string
        # "distance": f"{distance}",
        # "distanceunit": "km",
        # "opendata": "true",
        # "polyline": google polyline encoded: string
        "key": "42fc0eed-7a1d-49f6-b7a2-724b136adb3b"
        }   

    try:
        # Nominatim coordinates Multi polygons    
        stations = []
        for sub_area in area: 
            for sub in sub_area:
                simplified = Polygon(sub).simplify(0.01, preserve_topology=True)
                simplified_enc = polyline.encode(simplified.exterior.coords, precision=5, geojson=True) 
                querystring['polygon'] = f"{simplified_enc}" 
                stations.extend(request_openchargemap(querystring))
            
    except:        
        # Nominatim coordinates polygon
        # print(area)
        simplified = Polygon(area[0]).simplify(0.01, preserve_topology=True)
        simplified_enc = polyline.encode(simplified.exterior.coords, precision=5, geojson=True) 
        querystring['polygon'] = f"{simplified_enc}" 
        stations = request_openchargemap(querystring)

    print(len(stations))  
    return stations

from shapely.geometry import LineString
import pyproj
dist_meter = lambda x : pyproj.Geod(ellps='WGS84').geometry_length(x)

def split_line(point, linestring):
    best_distance = 999999
    best_idx = -1
    for idx, line_point in enumerate(linestring.coords):
        dist = point.distance( Point(line_point))
        if dist < best_distance:
            best_distance = dist
            best_idx = idx
        else:
            break
    start_line =  linestring.coords[:idx]
    start_line.append(point.coords[0])
    end_line = [point.coords[0]]
    end_line.extend(linestring.coords[idx:])
    return LineString(start_line), LineString(end_line)


class CustomException(Exception):
    """ my custom exception class """
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2
        display(value1, value2)

    def __str__(self):
        print(self.value1)    
        print(self.value2)

def print_edges(graph,closest_node,next_node,new):
    print('='*50)
    print('closest_node edges',graph.edges(closest_node))
    print('next_node edges',graph.edges(next_node))
    print('new node edges',graph.edges(new))

    print('-'*50)
    print(f'{closest_node} < {graph.has_edge(closest_node,next_node)} > {next_node}')
    print(f'{closest_node} < {graph.has_edge(closest_node,new)} > {new}')
    print(f'{new} < {graph.has_edge(new,next_node)} > {next_node}')

''' if station within 10 meters radius from a node,
    make this node a station to avoid node inflation
    
    else project the station on closest edge and split edges to 
    connect new station node'''    

def plug_between(graph,closest_node,next_node, key,station, debug=False):

    station_idx = f"station_{station.AddressInfo['ID']}"      #id of new node

    # get edge attributes
    edge_attrs = graph.edges[closest_node, next_node, key] # dict of edge attributes
    # display(edge_attrs)
    edge_linestring = edge_attrs['geometry']

    closest_point = edge_linestring.interpolate(edge_linestring.project(station.lmbrt))
    if closest_point.within(Point(graph.nodes('x')[closest_node],graph.nodes('y')[closest_node]).buffer(10)):
        print(f'plug {station_idx} to closest node {closest_node}')#,end='\r')
        attr_ = graph.nodes()[closest_node]
        attr_.update(
            {
            'real_gps':  Point(station.gps.x, station.gps.y),
            'real_lmbrt': Point(station.lmbrt.x, station.lmbrt.y), 
            'color' : (1.,0.,0.,1.),
            'infos' : station.__dict__  
            }
        )
        graph.add_node(closest_node, **attr_)
        graph = nx.relabel_nodes(graph, {closest_node: station_idx})

    elif closest_point.within(Point(graph.nodes('x')[next_node],graph.nodes('y')[next_node]).buffer(10)):
        print(F'Plug {station_idx} to next node {next_node}')#,end='\r') 
        attr_ = graph.nodes()[next_node]
        attr_.update(
            {
            'real_gps':  Point(station.gps.x, station.gps.y),
            'real_lmbrt': Point(station.lmbrt.x, station.lmbrt.y), 
            'color' : (1.,0.,0.,1.),
            'infos' : station.__dict__  
            }
        )
        graph.add_node(next_node, **attr_)
        graph = nx.relabel_nodes(graph, {next_node: station_idx})
    else:
        try:
            closest_node_line, next_node_line = split_line(closest_point, edge_linestring)
        except :
            raise CustomException(closest_point, edge_linestring)
    
        # create new node for station
        graph.add_node(station_idx, 
                        y= closest_point.y, 
                        x= closest_point.x, 
                        real_gps= Point(station.gps.x, station.gps.y),
                        real_lmbrt = Point(station.lmbrt.x, station.lmbrt.y), 
                        street_count = 2,
                        color = (1.,0.,0.,1.),
                        infos = station.__dict__
        )
        if debug: 
            print('before',end=' ')
            print_edges(graph,closest_node,next_node,station_idx)

        # link closest and new
        edge_attrs.update(
            dict(
            length = closest_node_line.length,      #dist_meter(closest_node_line),
            geometry = closest_node_line,
            )
        )
        graph.add_edge(closest_node, station_idx, key,**edge_attrs)
        #TODO reverse geometry ?
        # graph.add_edge(station_idx, closest_node, key,**edge_attrs)

        # link new and next
        edge_attrs.update(
            dict(
            length = next_node_line.length,      # dist_meter(next_node_line),
            geometry = next_node_line,
            )
        )
        graph.add_edge(next_node, station_idx, key,**edge_attrs)
        #TODO reverse geometry ?
        # graph.add_edge(station_idx, next_node, key,**edge_attrs)
        if debug: 
            print('after',end=' ')
            print_edges(graph,closest_node,next_node,station_idx)


        # remove old links
        graph.remove_edge(closest_node, next_node, key)
        # graph.remove_edge(next_node, closest_node, key)
        
        if debug: 
            print('removed old edges',end=' ')
            print_edges(graph,closest_node,next_node,station_idx)

    return graph

def duplicate_node(graph, node, idx):
    # TODO : create node idx with node edges
    return graph    




def graph_add_stations(graph, stations):
    duplicates = 0
    for n, station in enumerate(tqdm(stations)):
        # print(f'{n+1}/{len(stations)}', end='\r')

        point = station.lmbrt
        # point, _ = proj_geo(point, '4326', '2154')      # TODO: check if it works

        # Get from/to id of closest edge
        (closest_node, next_node, key), dist = ox.distance.nearest_edges(graph, X=point.x, Y=point.y, return_dist=True)
        # print(closest_node)
        if type(closest_node) == str:
            # set same edges as closest node:
            duplicates += 1
            station_idx = f"station_{station.AddressInfo['ID']}"      #id of new node
            duplicate_node(graph, closest_node, station_idx)
        elif type(next_node) == str:    
            # set same edges as next node:
            duplicates += 1
            station_idx = f"station_{station.AddressInfo['ID']}"      #id of new node
            duplicate_node(graph, next_node, station_idx)
        else:
            # create a new node between closest_node and next_node
            graph = plug_between(graph,closest_node,next_node, key,station, debug=False)

    return graph, duplicates
