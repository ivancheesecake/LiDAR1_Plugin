#	File name: generateIndicesBatch.py
#	Description: Python script for generating indices for raster datasets
#	Author: Phil-LiDAR 1 UPLB

# Directory processing from: http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python

import arcpy
from os import listdir
from os.path import isfile, join

try:

	# Retrieve inputs
	folderIn = arcpy.GetParameterAsText(0)
	featureOut = arcpy.GetParameterAsText(1)
	
	# Initialize variables
	featureList = []
	filenames =[]
	arr = arcpy.Array()
	files = [f for f in listdir(folderIn) if isfile(join(folderIn,f))]

	# Iterate through all files in the directory
	for f in files:
		# Check if the file is a .tif file
		# Allow other raster types for next version
		if f[-3:]=='tif': 
			arcpy.AddMessage("Creating a block for "+f)
			raster = arcpy.Raster(folderIn+"\\"+f)
			extent = raster.extent
			
			# Create a polygon based on the raster's extent
			arr.add(extent.lowerLeft)	
			arr.add(extent.lowerRight)	
			arr.add(extent.upperRight)	
			arr.add(extent.upperLeft)	
			arr.add(extent.lowerLeft)
			polygon = arcpy.Polygon(arr)

			# Append the created polygon in the list of all features
			featureList.append(polygon)
			filenames.append(f)

			arr = arcpy.Array()

	# Prepare the shapefile's spatial reference and attribute table		
	sr = arcpy.Describe(folderIn+"\\"+filenames[0]).spatialReference		
	arcpy.CopyFeatures_management(featureList, featureOut);
	arcpy.AddField_management(featureOut,"filename","TEXT");
	arcpy.DefineProjection_management(featureOut, sr)
	
	rows = arcpy.UpdateCursor(featureOut)
	i =0;

	for row in rows:
	 	row.filename = filenames[i]
	 	rows.updateRow(row)
	 	i = i+1

	# Display the generated shapefile in the current document 	
	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

	newlayer = arcpy.mapping.Layer(featureOut)
	arcpy.mapping.AddLayer(df, newlayer,"BOTTOM")

except: 

	arcpy.AddMessage(arcpy.GetMessages())