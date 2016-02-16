#	File name: loadIndices.py
#	Description: Python script for loading rasters using the generated indices
#	Author: Phil-LiDAR 1 UPLB

#http://gis.stackexchange.com/questions/12464/arcpy-add-raster-layer-layer-without-lyr-file

import arcpy
from os import listdir
from os.path import isfile, join

try:
	
	# Retrieve inputs
	folderIn = arcpy.GetParameterAsText(0)
	featureIn = arcpy.GetParameterAsText(1)
	
	# Initialize variables
	filenames =[]
	rows = []

	# Prepare the document
	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
	rows = arcpy.SearchCursor(featureIn)
	
	# Iterate through the shapefile's attribute table, and load the raster file
	for row in rows:
		
		filename = row.getValue("filename")
		arcpy.AddMessage("Loading "+filename+"...")
		filenames.append(row.getValue("filename"))
		result = arcpy.MakeRasterLayer_management(folderIn+"\\"+filename,filename)
		layer = result.getOutput(0)
		arcpy.mapping.AddLayer(df, layer,"TOP")

except:
	arcpy.AddMessage("HUHU")