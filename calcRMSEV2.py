#	File name: calcRMSEV2.py
#	Description: Python script for calculating the Root Mean Square Error of ground validation points and the LiDAR derived DTM
#				 to be used in calibrating the DTM	
#	Author: Phil-LiDAR 1 UPLB
#       Developer notes: For version 1.2, change outlier removal criterion from R^2 to STDEV

import arcpy
import numpy
import math
import matplotlib
import pylab

# 	Function for calculating the sum of squares in an array
# 	got help from http://stackoverflow.com/questions/16367823/python-sum-of-squares-function
def sum_of_squares(arr):
	return sum(c ** 2 for c in arr)

#	Function for calculatating the statistics needed for the user's interpretation
def calculateStatistics(tuples,difference):
	
	rmse = 0		
	rmse = math.sqrt(sum_of_squares(difference)/len(difference))
	avg = numpy.average(difference)
	stdev = numpy.std(difference)
	minus_sd = avg - 2*stdev
	plus_sd = avg + 2*stdev	

	# compute R^2
	sumXY = 0
	sumX = 0
	sumY = 0
	sumX2 =0
	sumY2 = 0
	n = len(tuples)
	for t in tuples:
		sumXY += t[0]*t[1]
		sumX += t[0]
		sumY +=t[1]
		sumX2 += t[0]**2
		sumY2 += t[1]**2

	rsq = ((n*sumXY - sumX*sumY)/(math.sqrt((n*sumX2 - sumX*sumX)*(n*sumY2 -sumY*sumY))))**2 	

	output = (rmse,avg,stdev,minus_sd,plus_sd,rsq)

	return output

#	Function for neatly displaying the computed statistics, also outputs a text file with the same content
def showStats(title, stats, fileName):

	msg = "\n============= "+title+" =============\n" + "RMSE: " + str(stats[0]) +"\n" + "AVG: "+str(stats[1]) + "\n" +"STDEV: "+str(stats[2]) + "\n" +"AVG-2*SD: "+str(stats[3]) + "\n" +"AVG_2*SD: "+str(stats[4]) + "\n" +"R^2 "+str(stats[5]) + "\n" +"====================================================>\n"
	arcpy.AddMessage(msg)
	text_file = open("C:/LiDAR1_Plugin_1.4/rmse/"+fileName+".txt", "w")
	text_file.write(msg)
	text_file.close()

#	Function that outputs a text file containing the logs of removed outliers
def outlierLog(msg):
	text_file = open("C:/LiDAR1_Plugin_1.4/rmse/outlierLog.txt", "w")
	text_file.write(msg)
	text_file.close()

#	Function that creates a scatterplot for the user's interpretation
def renderScatterplot(orthoList, rasterList, filename):
	arcpy.AddMessage("Generating scatterplot...")
	matplotlib.pyplot.scatter(orthoList,rasterList)
	matplotlib.pyplot.savefig("C:/LiDAR1_Plugin_1.4/rmse/"+filename+".png")
	matplotlib.pyplot.close()

try:
	
	# Fetch user inputs
	featureIn = arcpy.GetParameterAsText(0)
	rasterIn = arcpy.GetParameterAsText(1)
	rsqThresh = float(arcpy.GetParameterAsText(2))
	featureOut = "C:/LiDAR1_Plugin_1.4/rmse/val_lidar.shp"

	# Initialize variables
	rows = []
	tuples = []
	difference = []
	tuplesCleaned = []
	differenceCleaned = []
	orthoList = []
	rasterList =[]
	orthoListCleaned = []
	rasterListCleaned =[]

	# Extract values to points, self documenting code kuno. :))
	arcpy.AddMessage("Extracting raster values to points...")
	arcpy.sa.ExtractValuesToPoints(featureIn,rasterIn,featureOut)

	# Read data from attribute table
	arcpy.AddMessage("Reading data from attribute table...")
	rows = arcpy.SearchCursor(featureOut)
	for row in rows:
		
		ortho = row.getValue("BMOrtho")
		rastervalu = row.getValue("RASTERVALU")
		diff = ortho-rastervalu
		
		# Ensure that rows with a rastervalu of -9999 or 0 are not included
		if(rastervalu > -9998 and rastervalu !=0 ):	
			tuples.append((ortho,rastervalu,diff))
			orthoList.append(ortho)
			rasterList.append(rastervalu)
			difference.append(diff)		

	# Remove temporary data		
	arcpy.Delete_management(featureOut)		

	# Calculate initial statistics and provide to user
	stats = calculateStatistics(tuples,difference)
	showStats("Initial Data",stats,"InitialStats")

	# Create a scatterplot for initial data
	renderScatterplot(orthoList,rasterList,"initialScatter")

	# Duplicate the list and sort it
	tuplesCleaned = list(tuples)
	tuplesCleaned = sorted(tuplesCleaned, key=lambda tup: tup[2])
	
	for t in tuplesCleaned:
		differenceCleaned.append(t[2])

	# Get rid of outliers
	arcpy.AddMessage("Removing outliers...")	
	removeFirst = True
	msg =""
	iterations = 0
	tempDiff = 0

	maxIterations = math.floor(len(tuples) *.10)
	#while (stats[2] > 0.2 and stats[5] < rsqThresh) and iterations< maxIterations:
	# Please try this condition thoroughly
	while stats[2] > 0.2 or stats[5] < rsqThresh:

		if removeFirst and (tuplesCleaned[0][2] <= stats[3] or tuplesCleaned[0][2] >= stats[4]):
			tempDiff = tuplesCleaned[0][2]
			del tuplesCleaned[0]
			del differenceCleaned[0]
	
		if not removeFirst and (tuplesCleaned[-1][2] <= stats[3] or tuplesCleaned[-1][2] >= stats[4]):
			tempDiff = tuplesCleaned[-1][2]
			del tuplesCleaned[-1]
			del differenceCleaned[-1]
	
		removeFirst = not removeFirst
		stats = calculateStatistics(tuplesCleaned,differenceCleaned)
		
		msg += "Removed : "+str(tempDiff) +"\n" + "RMSE: " + str(stats[0]) +"\n"+ " AVG: "+str(stats[1]) + "\n"+ " STDEV: "+str(stats[2]) + "\n"+" AVG-2*SD: "+str(stats[3]) +"\n"+" AVG_2*SD: "+str(stats[4]) + "\n"+"R^2: "+str(stats[5]) + "\n\n"
		iterations +=1

	# Generate statistics and provide it to the user
	outlierLog(msg)
	
	stats = calculateStatistics(tuplesCleaned,differenceCleaned)
	showStats("Cleaned Data",stats,"CleanedStats")

	percent = (1-(len(tuplesCleaned)/float(len(tuples))))*100
	arcpy.AddMessage(str(percent)+"% of rows were removed.")
	
        arcpy.AddMessage("Initial: "+str(len(tuples)))
        arcpy.AddMessage("Cleaned: "+str(len(tuplesCleaned)))                 
	# Render scatterplot for cleaned data
	for t in tuplesCleaned:
		orthoListCleaned.append(t[0])
		rasterListCleaned.append(t[1])

	renderScatterplot(orthoListCleaned,rasterListCleaned,"scatterCleaned")

	# Write calculated RMSE and AVG into a text file
	text_file = open("C:/LiDAR1_Plugin_1.4/rmse/rmse.txt", "w")
	text_file.write(str(stats[0])+"\n"+str(stats[1]))
	text_file.close()

except:

	arcpy.AddError("Fail")
	arcpy.AddMessage(arcpy.GetMessages())
	
