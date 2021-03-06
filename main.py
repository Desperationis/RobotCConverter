from SettingParser import *
from Writer import *
from FileConverter import *
from ConfigPlugin import *
from MainPlugin import *
from CopyPlugin import *
from IncludePlugin import *
from TaskPlugin import *
from GlobalVariableTracker import *
from PythonFileLibrary.RecursiveScanner import *


settingParser = SettingParser()
recursiveScanner = RecursiveScanner(settingParser.inputFolder, ['.c', '.h'])
writer = Writer(settingParser.outputFolder)

globalIncludes = []
globalIncludes.append("#include \"../RobotC.h\"\n")
globalIncludes.append("#include \"../stdafx.h\"\n")
globalIncludes.append("using namespace RobotC::Types;\n")
globalIncludes.append("using namespace RobotC::Threads;\n")
globalIncludes.append("using namespace RobotC::Types;\n")
globalIncludes.append("using namespace RobotC::Peripherals;\n")
globalIncludes.append("using namespace RobotC::Functions;\n")

globalVariableTracker = GlobalVariableTracker(settingParser.outputFolder, globalIncludes)

globalIncludes.append("#include \"Externs.h\"\n")

for file in recursiveScanner.files:

    fileConverter = FileConverter(file)

    # Convert the '#include's as well as add the global includes.
    includePlugin = fileConverter.AddPlugin(IncludePlugin)
    includePlugin.SetGlobalIncludes(globalIncludes)

    # Make all tasks exitable.
    fileConverter.AddPlugin(TaskPlugin)

    if 'main.c' in file:
        # Only main.c has a task main() and the configuration for the motors and sensors.
        fileConverter.AddPlugin(ConfigPlugin)
        fileConverter.AddPlugin(MainPlugin)

    # Copy the rest of the file.
    fileConverter.AddPlugin(CopyPlugin)

    # Compile all plugins to an array of strings.
    fileConverter.Convert()

    writer.WriteFile(fileConverter)

    # Record all global variables.
    globalVariableTracker.ScanConverter(fileConverter)
