import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import osmnx as ox
import networkx as nx
import pyproj
from shapely.ops import transform




def _get_graph(place, custom_filter):
    ''' Returns a graph of the place'''
    
    graph = ox.graph_from_place(
        place+', Metropolitan France',
        network_type='drive',
        simplify=False,
        clean_periphery=True,
        # retain_all=True,
        # truncate_by_edges=True,
        buffer_dist = 1e3,       
        custom_filter= f'["highway"~"^({custom_filter})$"]',

        # custom_filter='["ref"~"^(D [0-9]|A [0-9]|N [0-9])$"]',
        # custom_filter='["ref"~"^(\s*[A]\s*[0-9]*\s*)$"]',
        # custom_filter='["ref"~"^(\s*[D]\s*[0-9]*\s*)$"]',
        # custom_filter='["ref"~"^(\s*[ADN]\s*[0-9]*\s*[a-zA-Z]*\s*[0-9]*\s*)$"]',
        # custom_filter='["highway"!~"^(tertiary|tertiary_link)$"]',

        # custom_filter='["ref"~"^D [0-9]+$"|"ref"~"A [0-9]+$"|"ref"~"N [0-9]+$"|"highway"~"motorway"]',
        )
    # graph =  ox.utils_graph.get_largest_component(graph, strongly=True)
    # graph =  ox.utils_graph.remove_isolated_nodes(graph)
    print('add speed', end='')
    graph = ox.speed.add_edge_speeds(graph)
    print(', distances', end='')
    graph = ox.distance.add_edge_lengths(graph)
    print(', travel time', end='')
    graph = ox.speed.add_edge_travel_times(graph)
    print(', simplify', end='')
    graph = ox.simplification.simplify_graph(graph, 
                                               strict=True, 
                                               remove_rings=True, 
                                               track_merged=False)
    print('... done. ')
    print(f'> {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges', end=', ')
    return graph

def get_graph(selection, custom_filter='|motorway'):
    '''custom_filter = (
                        '|motorway'
                        '|motorway_link'
                        '|trunk'
                        '|trunk_link'
                        '|primary',
                        '|primary_link',
                        '|secondary_link'
    )
    '''
    try:
        # print(selection)
        # print(custom_filter)
        ox.settings.cache_only_mode=True 
        G_ = _get_graph(selection, custom_filter)
    except:
        print('All requests done, building graph...', end=' ')
        ox.settings.cache_only_mode=False 
        G_ = _get_graph(selection, custom_filter)
    return G_    


from shapely import LineString
def fill_missing_edge_geometry(graph):
    corrected = 0
    for u, v, key, data in graph.edges(keys=True, data=True):
        try:
            edge_geometry = data["geometry"]
        except:
            corrected +=1
            data.update({'geometry': LineString([
                (graph.nodes[u]['x'], graph.nodes[u]['y']),
                (graph.nodes[v]['x'], graph.nodes[v]['y'])
            ])})
            graph.add_edge(u, v, key, **data)
    print(f' {corrected} edges geometries corrected.')
    return graph  

import folium
from folium.plugins import MarkerCluster


def graph2folium(graph, viz=True):
    alone = {}
    single = {}
    # dual = {}

    node_dict = graph.nodes('infos')
    for node in graph.nodes():
        # edges = G1.edges(node)
        # print(len(edges))
        if len(graph.edges(node))==0:
            alone[node] = node_dict[node]
        elif len(graph.edges(node))==1:
            single[node] = node_dict[node]    
        # break
    
    if viz:
        m = ox.folium.plot_graph_folium(graph, tiles='OpenStreetMap')
        Agroup = MarkerCluster(name="Alone nodes")
        Sgroup = MarkerCluster(name="Single nodes")

        for  n in alone.keys():
            x = nx.get_node_attributes(graph,'x')[n]
            y = nx.get_node_attributes(graph,'y')[n]
            Agroup.add_child(
                folium.Marker(
                    location=[y, x],
                    popup=n, icon=folium.Icon(color='red')
                    )
                )
        for  n in single.keys():
            x = nx.get_node_attributes(graph,'x')[n]
            y = nx.get_node_attributes(graph,'y')[n]
            Sgroup.add_child(
                folium.Marker(
                    location=[y, x],
                    popup=n, icon=folium.Icon(color='blue')
                    )
                )
        Agroup.add_to(m)
        Sgroup.add_to(m)
        folium.LayerControl().add_to(m) 

        display(m)
        del m
        print('Alones: ',len(alone),alone) 
        print('Singles : ',len(single),single)  

    return alone, single




import pandas as pd
from matplotlib import pyplot as plt

def graphplot(graph, edg_attr, nd_attr=None, title=''):
    # graph todataframe
    edges = ox.graph_to_gdfs(graph, nodes=False)
    try:
        edges[edg_attr].fillna(0, inplace=True)
    except:
        return print(f"Graph as no attribute '{edg_attr}'")
    # count attributes values
    edge_types = edges[edg_attr].value_counts()
    print('Color number:', len(edge_types))
    # get a colormap
    color_list = ox.plot.get_colors(n=len(edge_types), cmap='plasma_r',  alpha=0.7)
    # make a color mapper dict
    color_mapper = dict(
        zip(
        [l[0]  if type(l) == list else l for l in edge_types.index], 
        color_list
        )
    )
    # set the color for attribute less edges
    color_mapper[0.0] = (1.0,1.0,1.0,0.1)
    # get the color for each edge based on its attribute
    attr = [ d.get(edg_attr, 0) for u, v, k, d in graph.edges(keys=True, data=True)]
    attr = [ l[0] if type(l) == list else l for l in attr]
    ec = [color_mapper[l] for l in attr]
    # set nodes color
    # nc = [(0,0,1.0,0.9) for _ in graph.nodes()] if nd_attr==None else [d.get(nd_attr,(0,0,1.0,.9)) for _, d in graph.nodes(data=True)]
    nc =[ d.get('color', (.0,1.0,.0,.5)) for u, d in graph.nodes( data=True)]
    # plot graph
    fig, ax = plt.subplots()
    fig.suptitle(f'{title} {edg_attr}')
    ox.plot_graph(graph, 
                  edge_color=ec, 
                  node_color=nc,
                  node_size=2 if nd_attr==None else 10, 
                  ax=ax)
    
