### MIDTERM
# toolbox challenge

# the tool created within this code is intended to identify residential buildings that exist within 100m of RI wetlands
# understanding the impact of human disturbance on wetland areas is important when considering factors such as
# pollutant inflow, light and sound disturbance (especially during migration and breeding seasons), sedimentation, etc.

# input datasets include:
# .shp file of RI town boundaries
# .shp file of land cover data specific towns East of the Narragansett Bay

# the output files (i.e., those remaining following the removal of intermediate files):
# .shp file of the extracted residential areas
# .shp file of the defined study area (which was left to allow for the option of a boundary display)

# this analysis was achieved by selecting wetlands and residential buildings within a desired study area (which was the
# town of Tiverton in this example), buffering selected wetlands by the desired distance, and intersecting these buffers
# with previously selected residential buildings
# alterations could be made to this code to account for different study areas, buffer distances, levels of residential
# development, desired natural areas, among other specifications
# if the end user does not intend to make specifications to the selection parameters only the workspace needs to be
# altered to represent the file location on an individual machine

# import libraries
import arcpy
import os
arcpy.env.overwriteOutput = True

# set individual workspace (should be changed to per individual user)
# the folders containing the input data files is included in this repository as RI_towns.zip and RI_LandCover.zip
arcpy.env.workspace = r"C:\Users\emjha\Documents\python\midterm"

# create a folder within the workspace to store/separate output files from the input data
outputDirectory = os.path.join(arcpy.env.workspace, "output_files")
if not os.path.exists(outputDirectory):
    os.mkdir(outputDirectory)

# specify the input data
RI_towns = os.path.join(arcpy.env.workspace, r"RI_towns\RI_towns.shp")
RI_land_cover = os.path.join(arcpy.env.workspace, r"RI_LandCover\RI_land_cover.shp")


# select the study area
study_area = os.path.join(outputDirectory, "study_area.shp")
arcpy.analysis.Select(in_features=RI_towns,
                      out_feature_class=study_area,
                      where_clause="NAME = 'TIVERTON'")

# clip the land cover dataset to the study area
LandCover_StudyArea = os.path.join(outputDirectory, "LandCover_StudyArea.shp")
arcpy.analysis.Clip(in_features=RI_land_cover,
                    clip_features=study_area,
                    out_feature_class=LandCover_StudyArea,
                    cluster_tolerance="")

# select wetlands within the clipped land cover data
wetland = os.path.join(outputDirectory, "wetland.shp")
arcpy.analysis.Select(in_features=LandCover_StudyArea,
                      out_feature_class=wetland,
                      where_clause="DESCRIPTIO = 'Wetland'")

# buffer the selected wetlands by 100m
wetland_buffer = os.path.join(outputDirectory, "wetland_buffer.shp")
arcpy.analysis.Buffer(in_features=wetland,
                      out_feature_class=wetland_buffer,
                      buffer_distance_or_field="100 Meters",
                      line_side="FULL",
                      line_end_type="ROUND",
                      dissolve_option="NONE",
                      dissolve_field=[],
                      method="PLANAR")

# select residential areas within the clipped land cover data, all levels of residential development were selected
residential = os.path.join(outputDirectory, "residential.shp")
arcpy.analysis.Select(in_features=LandCover_StudyArea,
                      out_feature_class=residential,
                      where_clause="DESCRIPTIO = 'High Density Residential (<1/8 acre lots)' "
                                   "Or DESCRIPTIO = 'Low Density Residential (>2 acre lots)' "
                                   "Or DESCRIPTIO = 'Medium Density Residential (1 to 1/4 acre lots)' "
                                   "Or DESCRIPTIO = 'Medium High Density Residential (1/4 to 1/8 acre lots)' "
                                   "Or DESCRIPTIO = 'Medium Low Density Residential (1 to 2 acre lots)'")

# intersect the residential areas with the buffered wetlands to select developed areas that fall within 100m of wetlands
# the resulting .shp file will show the residential areas within this 100m wetland buffer and will exclude areas that
# exist outside that area
residential_wetland = os.path.join(outputDirectory, "residential_wetland.shp")
arcpy.analysis.Intersect(in_features=[[wetland_buffer, ""], [residential, ""]],
                         out_feature_class=residential_wetland,
                         join_attributes="ALL",
                         cluster_tolerance="",
                         output_type="INPUT")


# confirm the creation of the intersected layer and delete intermediate files
if arcpy.Exists(residential_wetland):
    print("residential features of interest selected successfully!")
    print("deleting intermediate files")
    arcpy.Delete_management(residential)
    arcpy.Delete_management(wetland_buffer)
    arcpy.Delete_management(wetland)
    arcpy.Delete_management(LandCover_StudyArea)
else:
    print("error")
