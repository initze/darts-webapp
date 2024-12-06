import branca
import geopandas as gpd
import leafmap.foliumap as leafmap
import streamlit as st
from streamlit_folium import st_folium

# load data
# fpath = "data/DARTS_NitzeEtAl_v1_features_2018_2023_level2.parquet"
fpath = 'https://arcticdata.io/metacat/d1/mn/v2/object/urn%3Auuid%3A91b12042-18fb-4ded-8854-124ff3be6a11'
gdf = gpd.read_file(fpath)
# gdf = gpd.read_parquet(fpath)
fpath_union = "DARTS_NitzeEtAl_v1_coverage_2018_2023_union.parquet"
gdf_footprints = gpd.read_parquet(fpath_union)

style_footprints = {
    "fillColor": "green",
    "color": "white",  # Default color for lines (for year 2018)
    "weight": 1,
    "fillOpacity": 0.1,
}

# load data
def create_map():
    m = leafmap.Map(zoom=5)
    # Add ESRI World Imagery basemap
    m.add_basemap("Esri.WorldImagery")
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

# Streamlit app layout
st.title("DARTS")

# Streamlit app layout
st.title("Dynamic Polygon Dashboard")

# Create the map with the GeoDataFrame layer
m = create_map()
m.add_gdf(gdf_footprints, layer_name="DARTS maximum extent", style_function=lambda x: style_footprints)
m.add_gdf(gdf, layer_name='DARTS v1 level2', style_function=style_function)

# Display the map in Streamlit using st_folium and capture clicked features
clicked_feature = st_folium(m, width='100%', returned_objects=['last_object_clicked'])