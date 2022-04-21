## CODING CHALLENGE 10
# rasters and NDVI

# this code uses Landsat raster imagery to calculate Normalized Difference Vegetation Index (NDVI) values per month
# for data collected in 2015.
# the input raster data was too large to upload to this repository
# after looking at the input data, we can see each folder corresponds to a month in 2015
# for each month provided (02, 04, 05, 07, 10, 11) NDVI was calculated using the equation:
# (near-infrared - visible-red) / (near-infrared + visible-red)
# or to put it in terms of the Landsat 8 imagery bands:
# (band-5 - band-4) / (band-5 + band-4)

# import all system modules
import arcpy
import os
arcpy.env.overwriteOutput = True

# new users only need to change the input_directory information per individual workspace/file location
input_directory = r"C:\Users\emjha\Documents\python\challenge_10\cc10_data"

# create a directory to hold output files
# this directory will be located within the input data folder
output_directory = os.path.join(input_directory, "output_files")
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

month_list = ["02", "04", "05", "07", "10", "11"]

# create a loop to go through the folders of each month
# list the raster files in each folder
# extract raster files that correspond to bands 4 and 5
for month in month_list:
    arcpy.env.workspace = os.path.join(input_directory, "2015" + month)
    raster_list = arcpy.ListRasters("*", "TIF")
    print("month " + str(month) + " " + "raster files: " + str(raster_list))
    band_4 = [x for x in raster_list if "B4" in x]
    print("month " + str(month) + " band 4 raster file = " + str(band_4))
    band_5 = [x for x in raster_list if "B5" in x]
    print("month " + str(month) + " band 5 raster file = " + str(band_5))

# composite bands 4 and 5 to create a comparative file for future NDVI visualization
    in_rasters = band_4, band_5
    arcpy.management.CompositeBands(in_rasters,
                                    os.path.join(output_directory, str(month) + "_composite.tif"))
    print("composite of bands 4 and 5 for month " + str(month) + " created successfully")

# use the raster calculator to execute the equation (band-5 - band-4) / (band-5 + band-4)
# output NDVI files for each month will be stored in the output_files folder
    arcpy.gp.RasterCalculator_sa('Float("' + band_5[0] +
                                 '"-"' + band_4[0] + '") / Float("' + band_5[0] +
                                 '"+"' + band_4[0] + '")',
                                 os.path.join(output_directory, str(month) + "_NDVI.tif"))
    print("NDVI for month " + str(month) + " created successfully")

