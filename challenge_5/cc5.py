## CODING CHALLENGE 5
# heatmap generation

# this code is intended to create individual heatmaps based on species observation data
# based on a single .csv file with locational data for more than one species
# for this example I chose to work with data representing foraging locations of Black-footed and Laysan Albatross
# both species occupy similar breeding grounds throughout the main and northwestern Hawaiian Islands
# data obtained from: https://obis.org/dataset/3f845a8d-536a-4630-8d16-31d8ed1e29a6

# this code is written to accommodate the end user
# change the workspace and file_name accordingly to fit individual machines or new datasets
# distinguishing species names should be located in row[0] of the starting .csv file


# import libraries
import csv
import os
import arcpy
arcpy.env.overwriteOutput = True

# specify workspace environment - should be altered per individual user
arcpy.env.workspace = r"C:\Users\emjha\Documents\python\challenge_5"

# saving the file_name and location in this format provides ease of use for different users or new files
file_name = "albatross_data.csv"
file_location = arcpy.env.workspace


# populate the empty species_list with information from the .csv file
# this task will print the names of all unique species from the input dataset
species_list = []
with open(os.path.join(file_location, file_name)) as species_csv:
    csv_reader = csv.reader(species_csv, delimiter=',')
    next(species_csv)
    for row in csv_reader:
        if row[0] not in species_list:
            species_list.append(row[0])
print("observed species include: " + str(species_list))


# loop through the original .csv file to create files specific to each unique species
# this task uses the .write and .join functions to ascribe data from the original file to species specific files
for individual in species_list:
    with open(os.path.join(file_location, file_name)) as species_csv:
        csv_reader = csv.reader(species_csv, delimiter=',')
        new_csv = open(individual + ".csv", "w")
        new_csv.write("common_name, scientific_name, latitude, longitude, date_time\n")
        for row in csv_reader:
            if row[0] == individual:
                new_csv.write(",".join(row) + "\n")
        new_csv.close()
    print("individual species file created: " + individual + ".csv")

# continue this loop to create shape, fishnet, and heatmap .shp files for each unique species

# set the spatial reference
# 4326 == WGS 1984
    spRef = arcpy.SpatialReference(4326)
# convert each individual .csv to a .shp file
    in_Table = individual + ".csv"
    x_coords = "longitude"
    y_coords = "latitude"
    z_coords = ""
    out_Layer = "species_point"
    saved_Layer = individual + ".shp"
# define the XY layer file
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
# save to a layer file
    arcpy.CopyFeatures_management(lyr, saved_Layer)
    if arcpy.Exists(saved_Layer):
        print(individual + " shapefile created successfully")


# extract the Extent of the generated shapefile
# i.e. XMin, XMax, YMin, YMax
    desc = arcpy.Describe(saved_Layer)
    XMin = desc.extent.XMin
    XMax = desc.extent.XMax
    YMin = desc.extent.YMin
    YMax = desc.extent.YMax


# generate a fishnet with a cell size of 0.25 degrees
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)
    # name of output fishnet
    outFeatureClass = individual + "_Fishnet.shp"

# set the origin of the fishnet
    originCoordinate = str(XMin) + " " + str(YMin)  # bottom left of the point data
    yAxisCoordinate = str(XMin) + " " + str(YMin + 1)  # sets the orientation on the y-axis, north-orientation
    cellSizeWidth = "0.25"
    cellSizeHeight = "0.25"
    numRows = ""  # leave blank, cellSize previously set
    numColumns = ""  # leave blank, cellSize previously set
    oppositeCorner = str(XMax) + " " + str(YMax)  # i.e. max x and max y coordinate
    labels = "NO_LABELS"
    templateExtent = "#"
    geometryType = "POLYGON"  # create a polygon

    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                   cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                   oppositeCorner, labels, templateExtent, geometryType)
    if arcpy.Exists(outFeatureClass):
        print(individual + " fishnet file created successfully")


# undertake a Spatial Join to join the fishnet to the observed point locations in the .shp files
    target_features = individual + "_Fishnet.shp"
    join_features = individual + ".shp"
    out_feature_class = individual + "_HeatMap.shp"
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    field_mapping = ""
    match_option = "INTERSECT"
    search_radius = ""
    distance_field_name = ""

    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                               join_operation, join_type, field_mapping, match_option,
                               search_radius, distance_field_name)

# check that the heatmap is created
    if arcpy.Exists(out_feature_class):
        print(individual + " heatmap file created successfully")
# delete the intermediate files (i.e. species shapefile and fishnet)
        print("deleting intermediate files")
        arcpy.Delete_management(target_features)
        arcpy.Delete_management(join_features)
