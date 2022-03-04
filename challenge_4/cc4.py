## CODING CHALLENGE 4
# arcpy tool: select

# the select tool is often used to create a new feature class based on input vector features
# this tool is useful in extracting data specific to an area of interest, vegetation classes, land cover types, etc.
# in this example we use a .shp file of RI towns to define and extract a certain county as a study area
# when working in arcpy the select tool is referred to as:
#   arcpy.Select_analysis()

# import all system modules
import arcpy


# set workspace as cc4_data folder, present in this repository as a .zip file
data_folder = r"C:\Users\emjha\Documents\python\challenge_4\cc4_data"


# set local variables
# all variables in this tool are required, missing variables will return an error
# the input features are simply the RI_towns.shp file
# input and output features for this tool are always vector data
input_features = data_folder + r"\Municipalities__1997_.shp"

# this tool will create a new feature class/.shp file representing just the selected area
# all the data associated with the selected features will be present in the new file's attribute table
output_feature_class = data_folder + r"\bristol_county.shp"

# the where_clause defines our selection
#   this action is looking within the "county" attribute for all towns within Bristol County
#   attributes for this file are in all caps and the tool would not run properly when the capitalization did not match
where_clause = '"COUNTY" = \'BRISTOL\''
# the where_clause can contain And/Or to include more than one attribute in the query


# execute the Select tool
# the resulting feature class files should appear in the cc4_data folder
arcpy.Select_analysis(input_features, output_feature_class, where_clause)
