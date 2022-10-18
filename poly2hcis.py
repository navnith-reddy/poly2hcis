import pandas as pd
import geopandas as gpd
import HCIS

# Verify ASMG files

# Initialise ASMG variables
l1,l2,l3,l4 = HCIS.buildLevels()
asmg = gpd.read_file("ASMG/ASMG.shp")

# Recieve User Input

# Read KML and Reproject
kml = gpd.read_file(filename , driver='KML')
kml = kml.to_crs(epsg=4283)

if level == 0:
    
    hcisKML = HCIS.poly2level(l1, kml)

elif level == 1:
        
    hcisKML = HCIS.poly2level(l1, kml)

elif level == 2:
        
    hcisKML = HCIS.poly2level(l2, kml)

elif level == 3:
        
    hcisKML = HCIS.poly2level(l3, kml)

elif level == 4:
        
    hcisKML = HCIS.poly2level(l4, kml)

else:
    
    raise Exception("Invalid HCIS Level Number")