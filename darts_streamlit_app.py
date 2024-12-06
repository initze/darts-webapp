# load data
import os

import branca
import geopandas as gpd
import leafmap.foliumap as leafmap
import requests
import streamlit as st
from streamlit_folium import st_folium


def download_and_load_parquet(url, filename):
    """
    Downloads a Parquet file from the specified URL if it does not already exist,
    and loads it into a GeoDataFrame.

    Parameters:
        url (str): The URL to download the Parquet file from.
        filename (str): The local filename to save the downloaded Parquet file.

    Returns:
        gpd.GeoDataFrame: The loaded GeoDataFrame from the Parquet file.
    """
    # Check if the file already exists
    if not os.path.exists(filename):
        print(f"{filename} does not exist. Downloading...")

        # Send a GET request to download the file
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"{filename} downloaded successfully.")
        else:
            raise Exception(
                f"Failed to download {filename}. Status code: {response.status_code}"
            )
    else:
        print(f"{filename} already exists. Loading from disk.")

    # Load the Parquet file into a GeoDataFrame
    gdf = gpd.read_parquet(filename)

    # Display the GeoDataFrame (optional)
    print(gdf.head())

    return gdf


# Example usage
url = "https://arcticdata.io/metacat/d1/mn/v2/object/urn%3Auuid%3A3a44d9bc-daa8-417e-a15e-5c983dda591a"
filename = "DARTS_NitzeEtAl_v1_features_2018_2023_level2.parquet"
# Call the function
gdf = download_and_load_parquet(url, filename)
# get coverage
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

# Create the map with the GeoDataFrame layer
m = create_map()
m.add_gdf(
    gdf_footprints,
    layer_name="DARTS maximum extent",
    style_function=lambda x: style_footprints,
)
m.add_gdf(gdf, layer_name="DARTS v1 level2", style_function=style_function)

# Display the map in Streamlit using st_folium and capture clicked features
clicked_feature = st_folium(m, width="100%", returned_objects=["last_object_clicked"])
