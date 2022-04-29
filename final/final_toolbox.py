### FINAL
# a functional python toolbox

# The goal of this tool is to select and measure features within a certain distance from RI Public Water Reservoirs
# Spatial data related to the amount of impervious surfaces within reservoir areas
# Helps to inform storm water and related pollutant management at both the city and state level

# PLEASE NOTE**: due to the size restrictions for GitHub files, the sample data for this tool is specific to the East
# Bay region of Rhode Island (i.e., Bristol and Newport County). The RI_roads_EastBay.shp file (included in the
# RI_roads.zip file in this repository) has been previously clipped to these two counties in order to decrease the size
# of the file when uploading to GitHub. Please take this into consideration when testing this tool and specify the
# desired study area county as either Bristol or Newport. **PLEASE NOTE**: due to the size restrictions for GitHub
# files, the sample data for this tool is specific to the East Bay region of Rhode Island
# (i.e., Bristol and Newport County).
# The RI_roads_EastBay.shp file (included in the RI_roads.zip file in this repository) has been previously clipped
# to these two counties in order to decrease the size of the file when uploading to GitHub. Please take this into
# consideration when testing this tool and specify the desired study area county as either Bristol or Newport.

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Final Toolbox"
        self.alias = ""

        # list of tool classes associated with this toolbox
        self.tools = [SelectStudyArea,
                      ClipReservoirs,
                      BufferReservoirs,
                      IntersectRoads]


class SelectStudyArea(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Select Study Area"
        self.description = "This tool will select and create a new feature layer based on a user-selected county."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_towns = arcpy.Parameter(name="input_towns",
                                      displayName="Input Towns ",
                                      datatype="DEFeatureClass",
                                      parameterType="Required",
                                      direction="Input")
        # this is a default value that can be over-ridden in the toolbox
        input_towns.value = r"C:\Users\emjha\Documents\python\final\RI_towns\RI_towns.shp"
        params.append(input_towns)
        # this allows the user to select a desired county within RI as their study area
        county_selection = arcpy.Parameter(name="county_selection",
                                           displayName="Desired County Selection",
                                           datatype="Field",
                                           parameterType="Required",
                                           direction="Input")
        county_selection.columns = [['GPString', 'Field']]
        county_selection.values = [['']]
        county_selection.filters[0].list = ['BRISTOL', 'KENT', 'NEWPORT', 'PROVIDENCE', 'WASHINGTON']
        params.append(county_selection)
        output_study_area = arcpy.Parameter(name="output_study_area",
                                            displayName="Output Study Area",
                                            datatype="DEFeatureClass",
                                            parameterType="Required",
                                            direction="Output")
        # this is a default value that can be over-ridden in the toolbox
        output_study_area.value = r"C:\Users\emjha\Documents\python\final\study_area.shp"
        params.append(output_study_area)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_towns = parameters[0].valueAsText
        county_selection = parameters[1].valueAsText
        output_study_area = parameters[2].valueAsText

        arcpy.Select_analysis(in_features=input_towns,
                              out_feature_class=output_study_area,
                              where_clause="COUNTY = " + county_selection)
        return


class ClipReservoirs(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Clip Reservoirs"
        self.description = "This tool will clip the reservoirs to the study area."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_features = arcpy.Parameter(name="input_features",
                                         displayName="Input Reservoirs Features",
                                         datatype="DEFeatureClass",
                                         parameterType="Required",
                                         direction="Input")
        # this is a default value that can be over-ridden in the toolbox
        input_features.value = r"C:\Users\emjha\Documents\python\final\RI_public_reservoirs\Public_Water_Reservoirs.shp"
        params.append(input_features)
        clip_features = arcpy.Parameter(name="clip_features",
                                        displayName="Clip to Study Area Features",
                                        datatype="DEFeatureClass",
                                        parameterType="Required",
                                        direction="Input")
        # this is a default value that can be over-ridden in the toolbox
        clip_features.value = r"C:\Users\emjha\Documents\python\final\study_area.shp"
        params.append(clip_features)
        reservoirs_study_area = arcpy.Parameter(name="reservoirs_study_area",
                                                displayName="Study Area Reservoirs",
                                                datatype="DEFeatureClass",
                                                parameterType="Required",
                                                direction="Output")
        # this is a default value that can be over-ridden in the toolbox
        reservoirs_study_area.value = r"C:\Users\emjha\Documents\python\final\reservoirs_study_area.shp"
        params.append(reservoirs_study_area)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_features = parameters[0].valueAsText
        clip_features = parameters[1].valueAsText
        reservoirs_study_area = parameters[2].valueAsText

        arcpy.Clip_analysis(in_features=input_features,
                            clip_features=clip_features,
                            out_feature_class=reservoirs_study_area,
                            cluster_tolerance="")
        return


class BufferReservoirs(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Buffer Reservoirs"
        self.description = "This tool will buffer the reservoirs within the study area by a user-selected distance."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        buffer_input = arcpy.Parameter(name="buffer_input",
                                       displayName="Input Featureclass of reservoirs within the study area",
                                       datatype="DEShapeFile",
                                       parameterType="Required",
                                       direction="Input")
        # this is a default value that can be over-ridden in the toolbox
        buffer_input.value = r"C:\Users\emjha\Documents\python\final\reservoirs_study_area.shp"
        params.append(buffer_input)
        # the user will be able to enter the desired buffer distance
        buffer_distance = arcpy.Parameter(name="buffer_distance",
                                          displayName="Size of Buffer (in Meters or Feet)",
                                          datatype="Field",
                                          parameterType="Required",
                                          direction="Input")
        params.append(buffer_distance)
        # the user will be able to select either Meters or Feet as the desired buffer unit
        buffer_unit = arcpy.Parameter(name="buffer_unit",
                                      displayName="Buffer Unit (select Meters or Feet)",
                                      datatype="Field",
                                      parameterType="Required",
                                      direction="Input")

        buffer_unit.columns = [['GPString', 'Field']]
        buffer_unit.values = [['']]
        buffer_unit.filters[0].list = ['Meters', 'Feet']
        params.append(buffer_unit)
        buffer_output = arcpy.Parameter(name="buffer_output",
                                        displayName="Buffered Reservoir Output",
                                        datatype="DEFeatureClass",
                                        parameterType="Required",
                                        direction="Output")
        buffer_output.value = r"C:\Users\emjha\Documents\python\final\reservoirs_buffered.shp"
        params.append(buffer_output)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        buffer_input = parameters[0].valueAsText
        buffer_distance = parameters[1].valueAsText
        buffer_unit = parameters[2].valueAsText
        buffer_output = parameters[3].valueAsText

        arcpy.Buffer_analysis(in_features=buffer_input,
                              out_feature_class=buffer_output,
                              buffer_distance_or_field=buffer_distance + " " + buffer_unit,
                              line_side="FULL",
                              line_end_type="ROUND",
                              dissolve_option="ALL",
                              dissolve_field=[],
                              method="PLANAR")
        return


class IntersectRoads(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Intersect Roads Tool"
        self.description = "This tool will create a new shapefile of roads that fall within the reservoirs buffer zones"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        buffered_area = arcpy.Parameter(name="buffered_area",
                                        displayName="Shapefile with Buffered Reservoir Features",
                                        datatype="DEFeatureClass",
                                        parameterType="Required",
                                        direction="Input")
        # this is a default value that can be over-ridden in the toolbox
        buffered_area.value = r"C:\Users\emjha\Documents\python\final\reservoirs_buffered.shp"
        params.append(buffered_area)
        input_roads = arcpy.Parameter(name="input_roads",
                                      displayName="Road Features to be Intersected",
                                      datatype="DEFeatureClass",
                                      parameterType="Required",
                                      direction="Input")
        # this is a default value that can be over-ridden in the toolbox
        input_roads.value = r"C:\Users\emjha\Documents\python\final\RI_roads\RI_roads_EastBay.shp"
        params.append(input_roads)
        roads_reservoirs = arcpy.Parameter(name="roads_reservoirs",
                                                displayName="Roads that Intersect with Buffered Reservoir Features",
                                                datatype="DEFeatureClass",
                                                parameterType="Required",
                                                direction="Output")
        # This is a default value that can be over-ridden in the toolbox
        roads_reservoirs.value = r"C:\Users\emjha\Documents\python\final\roads_reservoirs.shp"
        params.append(roads_reservoirs)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        buffered_area = parameters[0].valueAsText
        input_roads = parameters[1].valueAsText
        roads_reservoirs = parameters[2].valueAsText

        arcpy.analysis.Intersect(in_features=[[buffered_area, ""], [input_roads, ""]],
                                 out_feature_class=roads_reservoirs,
                                 join_attributes="ALL",
                                 cluster_tolerance="",
                                 output_type="INPUT")
        arcpy.AddMessage("Intersected Roads FeatureClass Created!")
        arcpy.AddMessage("Final Toolbox Challenge = Complete!")
        return
