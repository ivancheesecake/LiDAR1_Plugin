#	File name: calcRMSEV2.py
#	Description: Python script for calibrating the LiDAR derived DTM using the recently calculated RMSE value
#	Author: Phil-LiDAR 1 UPLB

import arcpy

try:
	# Retrieve inputs	
	rasterIn = arcpy.GetParameterAsText(0)
	rasterOut = arcpy.GetParameterAsText(1)

	data = []

	# Read the text file
	text_file = open("C:/LiDAR1_Plugin_1.1/rmse/rmse.txt", "r")

	for line in text_file:
		data.append(float(line))

	# If the average (data[1]) is negative, subtract the RMSE from the DTM, else add the RMSE to the DTM
	if data[1] < 0:
		data[0] *= -1

	calibrated =  arcpy.Raster(rasterIn) + data[0]
	
	# Save the calibrated DTM and display in the current document
	calibrated.save(rasterOut)
	
	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
	newlayer = arcpy.mapping.Layer(rasterOut)
	arcpy.mapping.AddLayer(df, newlayer,"TOP")

except:

	arcpy.AddError("Fail")
	arcpy.AddMessage(arcpy.GetMessages()) 

