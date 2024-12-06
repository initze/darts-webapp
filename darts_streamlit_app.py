import branca
import geopandas as gpd
import leafmap
import streamlit as st
from streamlit_folium import st_folium

# load data
def create_map(gdf, gdf_footprints):
    m = leafmap.Map(zoom=9)
    # Add ESRI World Imagery basemap
    # m.add_basemap("Esri.WorldImagery")

    m.add_gdf(gdf_footprints, layer_name="DARTS maximum extent", style_function=lambda x: style_footprints)
    # m.add_gdf(gdf[:20000], layer_name="DARTS level 2", zoom_to_layer=True, style_function=style_function)
    return m


def style_function(feature):
    # Initialize the style dictionary
    style = {
        "fillColor": None,  # No fill color for lines
        "color": "white",  # Default color for lines (for year 2018)
        "weight": 1,
        "fillOpacity": 0.1,
    }

    # Get the drainage year from feature properties
    year = feature["properties"]["year"]

    if year in range(2018, 2024):
        # Create a color palette for years 2019-2022
        palette = branca.colormap.linear.Reds_09.scale(2018, 2023)
        style["color"] = palette(year)

    return style


style_footprints = {
    "fillColor": "green",
    "color": "white",  # Default color for lines (for year 2018)
    "weight": 1,
    "fillOpacity": 0.1,
}


# load data
# fpath = "data/DARTS_NitzeEtAl_v1_features_2018_2023_level2.parquet"
fpath_union = "DARTS_NitzeEtAl_v1_coverage_2018_2023_union.parquet"
# gdf = gpd.read_parquet(fpath)
gdf_footprints = gpd.read_parquet(fpath_union)

# Streamlit app layout
st.title("DARTS")
# m = leafmap.Map(zoom=9)
m = create_map(None, gdf_footprints)

folium_map = m.to_folium()
st_folium(folium_map, width='100%', returned_objects=['last_object_clicked'])
