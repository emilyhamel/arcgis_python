## CODING CHALLENGE 9
# partitioning with the arcpy.da module

# this code works with an invasive species .shp file from the Forest Health Works dataset from RI GIS
# the goal of this script is to create counts of relevant data records and new files based on these specific records

# import all system modules
import arcpy
import os
arcpy.env.overwriteOutput = True

# set workspace as cc9_data folder, present in this repository as a .zip file
# new users only need to change the arcpy.env.workspace information per individual workspace/file location
# the input .shp file is located within the cc9_data folder
arcpy.env.workspace = r"C:\Users\emjha\Documents\python\challenge_9\cc9_data"
input_shp = r"RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp"

# the site and photo files in the .shp attribute table are most relevant to this code's overall goals
fields = ['Site', 'photo', 'Species']

# count how many individual invasive species records have photos associated with them:
# create an empty count to specific to photos
# set a search cursor to find attribute rows populated with y - which indicate that a photo is associated with a record
count_photos = 0
expression_photos = arcpy.AddFieldDelimiters(input_shp, "photo") + " = 'y'"
with arcpy.da.SearchCursor(input_shp, fields, expression_photos) as cursor:
    for row in cursor:
        print(u'Record at Site: {0}, with invasive species photo: {1}, Species = {2}'.format(row[0], row[1], row[2]))
        count_photos += 1

# count how many individual invasive species records do not have photos associated with them:
# create an empty count to specific to photos
# set a search cursor to find attribute rows populated without (<>) a y - which indicate the absence of a photo
count_NoPhotos = 0
expression_NoPhotos = arcpy.AddFieldDelimiters(input_shp, "photo") + " <> 'y'"
with arcpy.da.SearchCursor(input_shp, fields, expression_NoPhotos) as cursor:
    for row in cursor:
        print(u'Record at Site: {0}, without invasive species photo {1}, Species = {2}'.format(row[0], row[1], row[2]))
        count_NoPhotos += 1

# total counts can also be printed after each search cursor,
# but grouping the final print statements makes things easier to read for the end user
print(str(count_photos) + " invasive species records contain photos")
print(str(count_NoPhotos) + " invasive species records do not contain photos")

# count how many unique species are in the dataset:
unique_species = []
with arcpy.da.SearchCursor(input_shp, fields) as cursor:
    for row in cursor:
        if row[2] not in unique_species:
            unique_species.append(row[2])
print("this .shp file contains records of " + str(len(unique_species)) + " unique species")

# generate two new .shp files:
# the select tool will create new vector files based on set parameters
# I chose to store these newly created files in their own folder within the cc9_data folder
if not os.path.exists(os.path.join(arcpy.env.workspace, "output_shp")):
    os.mkdir(os.path.join(arcpy.env.workspace, "output_shp"))

# a new .shp file containing invasive species records with photos:
photo_file = os.path.join(arcpy.env.workspace, "output_shp", "Points_Invasives_Photos.shp")
select_photo = "photo = 'y'"
arcpy.Select_analysis(input_shp, photo_file, select_photo)
if arcpy.Exists(photo_file):
    print(".shp file with species photos created")

# a new .shp file containing invasive species records without photos:
NoPhoto_file = os.path.join(arcpy.env.workspace, "output_shp", "Points_Invasives_NoPhotos.shp")
select_NoPhoto = "photo <> 'y'"
arcpy.Select_analysis(input_shp, NoPhoto_file, select_NoPhoto)
if arcpy.Exists(NoPhoto_file):
    print(".shp file without species photos created")

# can also confirm successful file creation by comparing the counts of records with the new files' attribute tables
