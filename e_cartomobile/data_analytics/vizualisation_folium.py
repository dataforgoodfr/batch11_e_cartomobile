import folium
from folium import plugins


def plot_basemap_folium_france():
    """
    Fonction basique, simplement pour exemple
    """
    maptest = folium.Map(location=[46.9, 3], zoom_start=6)

    minimap = plugins.MiniMap()
    maptest.add_child(minimap)

    # afficher l'image
    return maptest
