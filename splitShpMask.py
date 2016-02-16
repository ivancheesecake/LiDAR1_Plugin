import arcpy

try:

	featureIn = arcpy.GetParameterAsText(0)
	folderOut = arcpy.GetParameterAsText(1)
	sliceSize = int(arcpy.GetParameterAsText(2))

	totalPolycount = arcpy.SearchCursor(featureIn, "", "", "", "FID D").next().getValue("FID")
	

	# totalPolycount = int(arcpy.GetCount_management(featureIn)[0])


	lowerBound = 0
	upperBound = sliceSize
	shpIndex = 1

	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

	

	while upperBound < totalPolycount:
		arcpy.Select_analysis(featureIn,folderOut+"\\shp_mask_"+str(shpIndex)+".shp", "FID >= " + str(lowerBound) + "AND FID < "+str(upperBound))	
		lowerBound = upperBound
		upperBound += sliceSize
		newlayer = arcpy.mapping.Layer(folderOut+"\\shp_mask_"+str(shpIndex)+".shp")
		arcpy.mapping.AddLayer(df, newlayer,"TOP")	

		shpIndex +=1	

		


	#last iteration

	upperBound = totalPolycount

	arcpy.Select_analysis(featureIn,folderOut+"\\shp_mask_"+str(shpIndex)+".shp", "FID >= " + str(lowerBound) + "AND FID < "+str(upperBound))	
	newlayer = arcpy.mapping.Layer(folderOut+"\\shp_mask_"+str(shpIndex)+".shp")
	arcpy.mapping.AddLayer(df, newlayer,"TOP")

except:

	arcpy.AddMessage(arcpy.GetMessages())