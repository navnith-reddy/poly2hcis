# -----------------------------------------------------------
# ---- Hierarchial Cell Identifier Scheme (HCIS) Library ----
# -----------------------------------------------------------
# Australian Communications Media Authority
# Navnith Reddy, October 2022

# The HCIS library contains functions critical to geospatial
# analysis using the ACMA's HCIS system of geographic 
# referencing.

import geopandas as gpd
import contextily as cx
import pandas as pd
import requests
import os
import zipfile
from matplotlib import pyplot as plt

def getASMG():
    """Downloads Australian Spectrum Map Grid shapefiles"""
    
    # Create ASMG folder if it doesn't exist
    if not os.path.exists("./ASMG"):
        os.mkdir("./ASMG")
    
    # Download ASMG shapefiles
    response = requests.get("https://channelfinder.acma.gov.au/webwr/spectrum-maps/ASMG_2012_GDA94.zip")
    open('ASMG/ASMG_2012_GDA94.zip', 'wb').write(response.content)
    
    # Extract zip file
    with zipfile.ZipFile("ASMG/ASMG_2012_GDA94.zip", 'r') as zip_ref:
        zip_ref.extractall("./ASMG")
    
    return

def getExtASMG0():
    """Downloads Extension Australian Spectrum Map Grid shapefiles"""
    
    # Create ASMG folder if it doesn't exist
    if not os.path.exists("./ASMG"):
        os.mkdir("./ASMG")
    
    # Download ASMG shapefiles
    response = requests.get("https://channelfinder.acma.gov.au/webwr/spectrum-maps/ExtASMG_2012_GDA94_L0.zip")
    open('ASMG/ExtASMG_2012_GDA94_L0.zip', 'wb').write(response.content)
    
    # Extract zip file
    with zipfile.ZipFile("ASMG/ExtASMG_2012_GDA94_L0.zip", 'r') as zip_ref:
        zip_ref.extractall("./ASMG")
    
    return

def buildASMG():
    """Build and save geodataframe of ASMG for EVERY HCIS ID as csv file.

    """
    
    l1 = gpd.read_file("ASMG/ASMG_2012_GDA94_L1.shp")
    l1.rename(columns={'HCI_Level1':'HCIS_ID'}, inplace=True)
    l1.drop(columns=['HCI_Level2', 'HCI_Level3', 'HCI_Level4'], inplace=True)

    l2 = gpd.read_file("ASMG/ASMG_2012_GDA94_L2.shp")
    l2.rename(columns={'HCI_Level2':'HCIS_ID'}, inplace=True)
    l2.drop(columns=['HCI_Level3', 'HCI_Level4'], inplace=True)

    l3 = gpd.read_file("ASMG/ASMG_2012_GDA94_L3.shp")
    l3.rename(columns={'HCI_Level3':'HCIS_ID'}, inplace=True)
    l3.drop(columns=['HCI_Level4'], inplace=True)

    l4 = gpd.read_file("ASMG/ASMG_2012_GDA94_L4.shp")
    l4.rename(columns={'HCI_Level4':'HCIS_ID'}, inplace=True)

    asmg = pd.concat([l1, l2, l3, l4])
    asmg.to_file('ASMG')
    
    return

def buildLevels():
    
    """Using ASMG files, builds HCIS Level geodataframes.

    Returns:
        l0, l1, l2, l3, l4: Five geodataframes.
    """
    
    l1 = gpd.read_file("ASMG/ASMG_2012_GDA94_L1.shp")
    l1.rename(columns={'HCI_Level1':'HCIS_ID'}, inplace=True)
    l1.drop(columns=['HCI_Level2', 'HCI_Level3', 'HCI_Level4'], inplace=True)

    l2 = gpd.read_file("ASMG/ASMG_2012_GDA94_L2.shp")
    l2.rename(columns={'HCI_Level2':'HCIS_ID'}, inplace=True)
    l2.drop(columns=['HCI_Level3', 'HCI_Level4'], inplace=True)

    l3 = gpd.read_file("ASMG/ASMG_2012_GDA94_L3.shp")
    l3.rename(columns={'HCI_Level3':'HCIS_ID'}, inplace=True)
    l3.drop(columns=['HCI_Level4'], inplace=True)

    l4 = gpd.read_file("ASMG/ASMG_2012_GDA94_L4.shp")
    l4.rename(columns={'HCI_Level4':'HCIS_ID'}, inplace=True)
    
    return l1, l2, l3, l4

def buildLevel0():
    
    """Using ASMG files, builds Extension HCIS Level 0 geodataframe.

    Returns:
        l0 : geodataframes.
    """
    
    l0 = gpd.read_file("ASMG/ExtASMG_2012_GDA94_L0.shp")
    l0.rename(columns={'HCI_Level0':'HCIS_ID'}, inplace=True)
    l0.drop(columns=['HCI_Level1', 'HCI_Level2', 'HCI_Level3', 'HCI_Level4'], inplace=True)
    
    return l0

def hcis2gdf (hcisList):
    """Convert list of HCIS identifiers into a geodataframe.

    Args:
        hcisList (list): List of HCIS identifier strings

    Returns:
        gdf (geodataframe): Geodataframe of input HCIS identifiers
    """
    
    asmg = gpd.read_file("ASMG/ASMG.shp")
    hcisList = pd.Series(hcisList)
    gdf = asmg[asmg['HCIS_ID'].isin(hcisList)]
    gdf.reset_index(inplace=True)
    
    return gdf

def poly2level (level, poly):
    
    """Convert polygon into HCIS geodataframe

    Args:
        level (geodataframe): HCIS Level geodataframe
        poly (geodataframe): Input polygon dataframe

    Returns:
        gdf (geodataframe): Geodataframe of HCIS polygons
    """
    
    gdf = gpd.overlay(level, poly, how="intersection")
    hcisList = gdf['HCIS_ID'].to_list()
    gdf = hcis2gdf(hcisList)
    
    return gdf

def preview (gdf, name):
    """

    Args:
        gdf (Geodataframe): Australian Geodataframe
        name (string): Filename of result

    Returns:
        result (plot): Plot of gdf
    """
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ax = world[world.name == 'Australia'].plot(color='white', edgecolor='black')
    result = gdf.plot(ax=ax, color='teal')
    plt.savefig(name + '.png')
    
    return result