import arcpy

try:
	# Retrieve inputs	
	dem = arcpy.GetParameterAsText(0)
	hillshade = arcpy.GetParameterAsText(1)

	if dem!='':

		arcpy.ApplySymbologyFromLayer_management(dem,"C:\LiDAR1_Plugin_1.4\Models\model_sym.lyr")
	
	if hillshade!='':
		
		arcpy.ApplySymbologyFromLayer_management(hillshade,"C:\LiDAR1_Plugin_1.4\Models\model_hs.lyr")


except:

	arcpy.AddMessage(arcpy.GetMessages()) 

