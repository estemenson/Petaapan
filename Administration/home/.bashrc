# This file is sourced
#
# Manage the environment for Eclipse and Python
# We remember the last Eclipse workspace used and the last version
# of Python that was set in the PATH

# Parse the command line arguments 
while getopts ":w:p:" Option "$AGIMAN_PARM1" "$AGIMAN_PARM2" "$AGIMAN_PARM3" "$AGIMAN_PARM4"
do
    case $Option in 
      w ) AGIMAN_WORKSPACE=$OPTARG;;
      p ) AGIMAN_PYTHON=$OPTARG;;
      * ) echo "Unrecognised option -$Option with value $OPTARG";;
    esac
done


# Run the script that sets up the environment
if [[ "$AGIMAN_STARTUP" == "1" ]]
then
    # First load up keys into ssh-agent
    ssh-add ~/.ssh/*_rsa
    
    # Start SmartGit
    "/c/Program Files (x86)/SmartGit 1.5/bin/smartgit.exe" &
    
    # Start Eclipse
    /d/Users/jonathan/Downloads/Eclipse/eclipse-rcp-helios-win32/eclipse/eclipse.exe &
fi
