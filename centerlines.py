#Default geodatabase ang diretso
#make O(n) and O(n^2) versions, pag di umunra yung O(n), gamitin yung O(n^2)
#gawing feature layer!
import arcpy
from arcpy import env
import math

arcpy.env.overwriteOutput = True
 

def euclideanDistance2D(x1,y1,x2,y2):

	return math.sqrt((y2-y1)*(y2-y1) + (x2-x1)*(x2-x1))

def closestPoint(primaryPoint, secondaryPoints):

	currDist = minDist = euclideanDistance2D(primaryPoint[0],primaryPoint[1],secondaryPoints[0][0],secondaryPoints[0][1])
	minIndex = index = 0 
	for secondaryPoint in secondaryPoints:
		currDist = euclideanDistance2D(primaryPoint[0],primaryPoint[1],secondaryPoints[index][0],secondaryPoints[index][1])
		if  currDist < minDist:
			minDist = currDist
			minIndex = index
		index = index+1

	return secondaryPoints[minIndex] 

try:
	arcpy.AddMessage("THIS")
	#retrieve inputs
	river1In = arcpy.GetParameterAsText(0)
	river2In = arcpy.GetParameterAsText(1)
	#arcpy.env.workspace = arcpy.GetParameterAsText(2) #no need for this, derive this from output file to lessen inputs
	centerlineOut= arcpy.GetParameterAsText(2) 
	
	dotIndex = centerlineOut.find(".")
	leftCenterLineOut = centerlineOut[:dotIndex]+"_left"+centerlineOut[dotIndex:]
	rightCenterLineOut = centerlineOut[:dotIndex]+"_right"+centerlineOut[dotIndex:]

	arcpy.env.workspace = centerlineOut[:centerlineOut.find("\\",-dotIndex)]

	sr = arcpy.Describe(river1In).spatialReference
	#initialize variables
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
	
	#extract vertices
	arcpy.FeatureVerticesToPoints_management(river1In,arcpy.env.workspace+"\\river1_points.shp");
	arcpy.FeatureVerticesToPoints_management(river2In,arcpy.env.workspace+"\\river2_points.shp");

	#create arrays of points
	arcpy.AddMessage("Initialize Array of points")
	for row in arcpy.da.SearchCursor(arcpy.env.workspace+"\\river1_points.shp", ["SHAPE@XY"]):
		points.append(row[0]);
		# arcpy.AddMessage(row[0])

	for row in arcpy.da.SearchCursor(arcpy.env.workspace+"\\river2_points.shp", ["SHAPE@XY"]):
		points2.append(row[0]);

	if len(points) < len(points2):
		primary = points
		secondary = points2
	else:
		primary = points2
		secondary = points

	maxLength = len(primary)
	
	arcpy.AddMessage("Computing Centerline Vertices...")	
	for i in range(0,maxLength-1):
		pt = closestPoint(primary[i],secondary)
		x = (primary[i][0]+pt[0])/2
		y = (primary[i][1]+pt[1])/2
		centerLineVertices.append(arcpy.Point((primary[i][0]+pt[0])/2,(primary[i][1]+pt[1])/2))
		pointsCenter.append([x,y])
	
	if len(points) < len(pointsCenter):
		primary = points
		secondary = pointsCenter
	else:
		primary = pointsCenter
		secondary = points

	maxLength = len(primary)
	
	# arcpy.AddMessage(maxLength)	
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

	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

	newlayer = arcpy.mapping.Layer(centerlineOut)
	arcpy.mapping.AddLayer(df, newlayer,"BOTTOM")

	newlayer2 = arcpy.mapping.Layer(leftCenterLineOut)
	arcpy.mapping.AddLayer(df, newlayer2,"BOTTOM")

	newlayer3 = arcpy.mapping.Layer(rightCenterLineOut)
	arcpy.mapping.AddLayer(df, newlayer3,"BOTTOM")

	arcpy.Delete_management(arcpy.env.workspace+"\\river1_points.shp","")
	arcpy.Delete_management(arcpy.env.workspace+"\\river2_points.shp","")

except: 

	arcpy.AddError("Fail")
	arcpy.AddMessage(arcpy.GetMessages())
