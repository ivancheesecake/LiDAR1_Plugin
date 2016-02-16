#	File name: centerlinesV2.py
#	Description: Python script for generating a the centerline and flow paths of a river with its banks as inputs
#	Author: Phil-LiDAR 1 UPLB

import arcpy
from arcpy import env
import math

arcpy.env.overwriteOutput = True

# Function for calculating the euclidean distance between two points 
def euclideanDistance2D(x1,y1,x2,y2):

	return math.sqrt((y2-y1)*(y2-y1) + (x2-x1)*(x2-x1))

# Function for determining the closest point in the secondary dataset from a certain point in the primary dataset
def closestPoint(primaryPoint, secondaryPoints):

	# Initialize values
	currDist = minDist = euclideanDistance2D(primaryPoint[0],primaryPoint[1],secondaryPoints[0][0],secondaryPoints[0][1])
	minIndex = index = 0 
	
	# Go through all points in the secondary dataset
	for secondaryPoint in secondaryPoints:
		# Compute for the euclidean distance between the point in the primary dataset and the current point in the secondary dataset
		# eventually select the closest point 
		currDist = euclideanDistance2D(primaryPoint[0],primaryPoint[1],secondaryPoints[index][0],secondaryPoints[index][1])
		if  currDist < minDist:
			minDist = currDist
			minIndex = index
		index = index+1

	return secondaryPoints[minIndex] 

try:
	
	# Retrieve inputs
	river1In = arcpy.GetParameterAsText(0)
	river2In = arcpy.GetParameterAsText(1)
	centerlineOut= arcpy.GetParameterAsText(2) 
	
	# Prepare filenames for outputs
	dotIndex = centerlineOut.find(".")
	leftCenterLineOut = centerlineOut[:dotIndex]+"_left"+centerlineOut[dotIndex:]
	rightCenterLineOut = centerlineOut[:dotIndex]+"_right"+centerlineOut[dotIndex:]
	river1In_simple = centerlineOut[:dotIndex]+"_lbtemp"+centerlineOut[dotIndex:]
	river2In_simple = centerlineOut[:dotIndex]+"_rbtemp"+centerlineOut[dotIndex:]

	arcpy.env.workspace = centerlineOut[:centerlineOut.find("\\",-dotIndex)]

	sr = arcpy.Describe(river1In).spatialReference
	
	# Initialize variables
	index1 = index2 = 0
	leftCenterLineVertices = arcpy.Array()
	rightCenterLineVertices = arcpy.Array()
	centerLineVertices = arcpy.Array()
	featureList =[]
	featureList2 =[]
	featureList3 =[]
	points = list()
	points2 = list()
	primary = list()
	secondary =list()
	pointsCenter = list();

	primaryArr = arcpy.Array()
	secondaryArr = arcpy.Array()

	# Simplify lines for less iterations
	arcpy.cartography.SimplifyLine(river1In,river1In_simple,"BEND_SIMPLIFY","1 meters","RESOLVE_ERRORS","NO_KEEP")
	arcpy.cartography.SimplifyLine(river2In,river2In_simple,"BEND_SIMPLIFY","1 meters","RESOLVE_ERRORS","NO_KEEP")


	# Extract vertices
	arcpy.FeatureVerticesToPoints_management(river1In_simple,arcpy.env.workspace+"\\river1_points.shp");
	arcpy.FeatureVerticesToPoints_management(river2In_simple,arcpy.env.workspace+"\\river2_points.shp");

	# Create arrays of points
	arcpy.AddMessage("Initialize Array of points")
	for row in arcpy.da.SearchCursor(arcpy.env.workspace+"\\river1_points.shp", ["SHAPE@XY"]):
		points.append(row[0]);

	for row in arcpy.da.SearchCursor(arcpy.env.workspace+"\\river2_points.shp", ["SHAPE@XY"]):
		points2.append(row[0]);

	# Decide which list is going to be the primary and the secondary dataset	
	if len(points) < len(points2):
		primary = points
		secondary = points2
	else:
		primary = points2
		secondary = points

	maxLength = len(primary)
	
	# Compute for the centerline vertices
	arcpy.AddMessage("Computing Centerline Vertices...")	
	
	# Go through all points in the primary dataset
	# Locate the closest point from the secondary dataset, and generate the midpoint
	# Append the computed midpoint in the list of center line vertices 
	for i in range(0,maxLength-1):
		pt = closestPoint(primary[i],secondary)
		x = (primary[i][0]+pt[0])/2
		y = (primary[i][1]+pt[1])/2
		centerLineVertices.append(arcpy.Point((primary[i][0]+pt[0])/2,(primary[i][1]+pt[1])/2))
		pointsCenter.append([x,y])
	
	# Repeat the process for the flow paths 

	if len(points) < len(pointsCenter):
		primary = points
		secondary = pointsCenter
	else:
		primary = pointsCenter
		secondary = points

	maxLength = len(primary)
	arcpy.AddMessage("Computing Left Centerline Vertices...")	
	for i in range(0,maxLength-1):
		pt = closestPoint(primary[i],secondary)
		leftCenterLineVertices.append(arcpy.Point((primary[i][0]+pt[0])/2,(primary[i][1]+pt[1])/2))	

	if len(points2) < len(pointsCenter):
		primary = points2
		secondary = pointsCenter
	else:
		primary = pointsCenter
		secondary = points2

	maxLength = len(primary)
		
	arcpy.AddMessage("Computing Right Centerline Vertices...")	
	for i in range(0,maxLength-1):
		pt = closestPoint(primary[i],secondary)
		rightCenterLineVertices.append(arcpy.Point((primary[i][0]+pt[0])/2,(primary[i][1]+pt[1])/2))	
	
	# Generate the shapefiles for the computed centerline and flow paths
	featureList = []
	centerLine = arcpy.Polyline(centerLineVertices)
	featureList.append(centerLine)
	arcpy.CopyFeatures_management(featureList, centerlineOut)
	arcpy.DefineProjection_management(centerlineOut, sr)

	featureList = []
	leftCenterLine = arcpy.Polyline(leftCenterLineVertices)
	featureList.append(leftCenterLine)
	arcpy.CopyFeatures_management(featureList, leftCenterLineOut)
	arcpy.DefineProjection_management(leftCenterLineOut, sr)

	featureList = []
	rightCenterLine = arcpy.Polyline(rightCenterLineVertices)
	featureList.append(rightCenterLine)
	arcpy.CopyFeatures_management(featureList, rightCenterLineOut)
	arcpy.DefineProjection_management(rightCenterLineOut, sr)

	# Display the results in the current document
	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

	newlayer = arcpy.mapping.Layer(centerlineOut)
	arcpy.mapping.AddLayer(df, newlayer,"BOTTOM")

	newlayer2 = arcpy.mapping.Layer(leftCenterLineOut)
	arcpy.mapping.AddLayer(df, newlayer2,"BOTTOM")

	newlayer3 = arcpy.mapping.Layer(rightCenterLineOut)
	arcpy.mapping.AddLayer(df, newlayer3,"BOTTOM")

	# Delete the generated temporary files
	arcpy.Delete_management(arcpy.env.workspace+"\\river1_points.shp","")
	arcpy.Delete_management(arcpy.env.workspace+"\\river2_points.shp","")
	arcpy.Delete_management(river1In_simple,"")
	arcpy.Delete_management(river2In_simple,"")

except: 

	arcpy.AddError("Fail")
	arcpy.AddMessage(arcpy.GetMessages())
