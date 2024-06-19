#!/bin/bash

# Define a variable
export ENVIRONMENT_SELECTION=1

# Check if the variable is equal to a specific value
if [ $ENVIRONMENT_SELECTION -eq 1 ]; then
    PATH_ENVIRONMENT_FILE="$pwd/Maps/MSBuild2018/LinuxNoEditor/MSBuild2018.sh"
    echo "Environmet has been set to MSBuild2018."
elif [ $ENVIRONMENT_SELECTION -eq 2 ]; then
PATH_ENVIRONMENT_FILE="$pwd/Maps/Africa_Savannah/LinuxNoEditor/Africa_001.sh"
    echo "Environmet has been set to Africa_Savannah."
elif [ $ENVIRONMENT_SELECTION -eq 3 ]; then
    PATH_ENVIRONMENT_FILE="$pwd/Maps/LandscapeMountains/LinuxNoEditor/LandscapeMountains.sh"
    echo "Environmet has been set to LandscapeMountains."
elif [ $ENVIRONMENT_SELECTION -eq 4 ]; then
    PATH_ENVIRONMENT_FILE="$pwd/Maps/ZhangJiajie/LinuxNoEditor/ZhangJiajie.sh"
    echo "Environmet has been set to ZhangJiajie."
elif [ $ENVIRONMENT_SELECTION -eq 5 ]; then
    PATH_ENVIRONMENT_FILE="$pwd/Maps/AirSimNH/LinuxNoEditor/AirSimNH.sh"
    echo "Environmet has been set to AirSimNH."
else
    echo "Please provide valid environment setting."
fi

echo $PATH_ENVIRONMENT_FILE

./$PATH_ENVIRONMENT_FILE -./settings.json -WINDOWED -ResX=960 -ResY=720