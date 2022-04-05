## CODING CHALLENGE 7
# heatmap generation with temporary folders


# import libraries
import csv
import os
import glob
import arcpy
arcpy.env.overwriteOutput = True

# define the file location and specific data file
# the input_directory should be altered per individual user
input_directory = r"C:\Data\Students_2022\Hamel\challenge_7"
data_file = "albatross_data.csv"

# create new file locations for results data
# intermediate files will be stored in the temporary_files folder and output_files will contain the final results
if not os.path.exists(os.path.join(input_directory, "temporary_files")):
    os.mkdir(os.path.join(input_directory, "temporary_files"))
if not os.path.exists(os.path.join(input_directory, "output_files")):
    os.mkdir(os.path.join(input_directory, "output_files"))


# populate the empty species_list with information from the .csv file
# this task will print the names of all unique species from the input dataset
species_list = []
with open(os.path.join(input_directory, data_file)) as species_csv:
    csv_reader = csv.reader(species_csv, delimiter=',')
    next(species_csv)
    for row in csv_reader:
        if row[0] not in species_list:
            species_list.append(row[0])
print("observed species include: " + str(species_list))


# loop through the original .csv file to create files specific to each unique species
# this task uses the .write and .join functions to ascribe data from the original file to species specific files
for individual in species_list:
    with open(os.path.join(input_directory, data_file)) as species_csv:
        csv_reader = csv.reader(species_csv, delimiter=',')
        new_csv = open(os.path.join(input_directory, "temporary_files", individual + ".csv"), "w")
        new_csv.write("common_name, scientific_name, latitude, longitude, date_time\n")
        for row in csv_reader:
            if row[0] == individual:
                new_csv.write(",".join(row) + "\n")
        new_csv.close()
    print("individual species file created: " + individual + ".csv")


# convert the newly created .csv files into .shp files
os.chdir(os.path.join(input_directory, "temporary_files"))  # same as env.workspace
arcpy.env.workspace = os.path.join(input_directory, "temporary_files")
species_file_list = glob.glob("*.csv")  # Find all CSV files

# begin a loop to create shape, fishnet, and heatmap .shp files for each unique species

# convert each individual .csv to a .shp file
for individual in species_file_list:
    in_Table = individual
    x_coords = "longitude"
    y_coords = "latitude"
    z_coords = ""
    out_Layer = "species_point"
    saved_Layer = individual.replace(".", "_") + ".shp"

# set the spatial reference
    spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
# define the XY layer file
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
# save to a layer file
    arcpy.CopyFeatures_management(lyr, os.path.join(input_directory, "temporary_files", saved_Layer))
    if arcpy.Exists(saved_Layer):
        print(individual + " shapefile created successfully")

# extract the Extent of the generated shapefile
# i.e. XMin, XMax, YMin, YMax
    desc = arcpy.Describe(os.path.join(input_directory, "temporary_files", saved_Layer))
    print(desc)
    print(os.path.join(input_directory, "temporary_files", saved_Layer))
    XMin = desc.extent.XMin  # ERROR...method extent does not exist
    XMax = desc.extent.XMax
    YMin = desc.extent.YMin
    YMax = desc.extent.YMax
    print(YMax)

#
# # generate a fishnet with a cell size of 0.25 degrees
#     arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)
#     # name of output fishnet
#     outFeatureClass = individual + "_Fishnet.shp"
#
# # set the origin of the fishnet
#     originCoordinate = str(XMin) + " " + str(YMin)  # bottom left of the point data
#     yAxisCoordinate = str(XMin) + " " + str(YMin + 1)  # sets the orientation on the y-axis, north-orientation
#     cellSizeWidth = "0.25"
#     cellSizeHeight = "0.25"
#     numRows = ""  # leave blank, cellSize previously set
#     numColumns = ""  # leave blank, cellSize previously set
#     oppositeCorner = str(XMax) + " " + str(YMax)  # i.e. max x and max y coordinate
#     labels = "NO_LABELS"
#     templateExtent = "#"
#     geometryType = "POLYGON"  # create a polygon
#
#     arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
#                                    cellSizeWidth, cellSizeHeight, numRows, numColumns,
#                                    oppositeCorner, labels, templateExtent, geometryType)
#     if arcpy.Exists(individual + "_Fishnet.shp"):
#         print(individual + " fishnet file created successfully")
#
#
# # undertake a Spatial Join to join the fishnet to the observed point locations in the .shp files
#     target_features = individual + "_Fishnet.shp"
#     join_features = individual + ".shp"
#     out_feature_class = os.path.join(input_directory, "output_files", individual + "_HeatMap.shp")
#     join_operation = "JOIN_ONE_TO_ONE"
#     join_type = "KEEP_ALL"
#     field_mapping = ""
#     match_option = "INTERSECT"
#     search_radius = ""
#     distance_field_name = ""
#
#     arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
#                                join_operation, join_type, field_mapping, match_option,
#                                search_radius, distance_field_name)
#
#
# # check that the heatmap is created
#     if arcpy.Exists(os.path.join(input_directory, "output_files", individual + "_HeatMap.shp")):
#         print(individual + " heatmap file created successfully")
# # delete the intermediate files (i.e. species shapefile and fishnet)
#         print("deleting the temporary folder")
#         arcpy.Delete_management(os.path.join(input_directory, "temporary_files"))
