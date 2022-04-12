## CODING CHALLENGE 8
# creating functions

# import all system modules
import arcpy
import os
arcpy.env.overwriteOutput = True

# set workspace as cc8_data folder, present in this repository as a .zip file
# new users only need to change the data_folder information, unless making a selection from a new .shp file
data_folder = r"C:\Users\emjha\Documents\python\challenge_8\cc8_data"
data_file = "Municipalities__1997_.shp"

# this code converts Coding Challenge 4 into a function and provides relevant information about the input .shp file
# to use this function call: select_tool()
# with this function, the end user can specify a specific county and create a new .shp file of the area of interest
# this function is written for use at a county-level but can be edited to select for other data in the attribute table
# print statements are provided to view feature descriptions, coordinate systems, and confirm successful file creation
def select_tool(input, selection):
    arcpy.env.workspace = input
    if arcpy.Exists(input):
        desc = arcpy.Describe(input)
        print("Describing: " + str(input))
        if desc.dataType == "ShapeFile":
            print("Feature Type:  " + desc.shapeType)
            print("Coordinate system: " + desc.SpatialReference.name)
            print("Coordinate system type: " + desc.SpatialReference.type)
        else:
            print("Input data is not a ShapeFile")
    else:
        print("Dataset not found")
    for data_file in input:
        input_features = input
        output_feature_class = os.path.join(data_folder, "county_" + selection + ".shp")
        where_clause = '"COUNTY" = \'' + selection + "'"
        arcpy.Select_analysis(input_features, output_feature_class, where_clause)
    print(selection + " county selected")
    print("county_" + selection + ".shp created")

# set the function specifications
# an input and selection parameters are required for this function
# the input refers to the folder and file specifications set on lines 11 and 12
# the selection refers to the desired county of interest
input = os.path.join(data_folder, data_file)
selection = "BRISTOL"

# run the function
select_tool(input, selection)
