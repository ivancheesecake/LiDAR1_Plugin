import arcpy

try:

	#generate array of filenames
	#last step ang pag-populate ng attribute table

	rasterIn = arcpy.GetParameterAsText(0)
	featureOut = arcpy.GetParameterAsText(1)

	arcpy.AddMessage(featureOut)

	raster = arcpy.Raster(rasterIn)
	extent = raster.extent

	arr = arcpy.Array()

	arr.add(extent.lowerLeft)	
	arr.add(extent.lowerRight)	
	arr.add(extent.upperRight)	
	arr.add(extent.upperLeft)	
	arr.add(extent.lowerLeft)	

	polygon = arcpy.Polygon(arr)

	arcpy.CopyFeatures_management(polygon, featureOut);

	arcpy.AddField_management(featureOut,"filename","TEXT");
	rows = arcpy.UpdateCursor(featureOut)
	for row in rows:
		row.filename = rasterIn
		rows.updateRow(row)

	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

	newlayer = arcpy.mapping.Layer(featureOut)
	arcpy.mapping.AddLayer(df, newlayer,"BOTTOM")

except: 

	arcpy.AddMessage(arcpy.GetMessages())