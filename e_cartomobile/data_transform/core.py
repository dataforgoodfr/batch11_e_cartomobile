import pyproj

def get_lat_lon_from_x_y(x1, y1):
    
    transformer = pyproj.Transformer.from_crs("EPSG:2154","EPSG:4326")
    # 2154 : lambert 93
    # 4326 : WGS84

    return transformer.transform(x1,y1)

def get_x_y_from_lat_lon(lat1, lon1):
    
    transformer = pyproj.Transformer.from_crs("EPSG:4326","EPSG:2154")

    return transformer.transform(lat1, lon1)
