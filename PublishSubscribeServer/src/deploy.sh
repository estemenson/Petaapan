#!/bin/bash
# Script to prepare Publish/Subscribe server for deployment to Google
# and optionally do the deployment
# The script will run in the src directory of the
# PublishSubscribe Eclipse project
#
# Usage: deploy [-c] [-t] [-u] [root]
# Options:  -c   Clear the deployment directory before starting
#           -t   Run tests from deployment directory
#           -u   Do the upload to Google
#           root Is the parent directory of the deployment directory
#                It defaults to the CWD which should be the src
#                directory of the Petaapan PublishSubscribeServer
#                Eclipse project

# Parse the command line arguments
Clear=0
Upload=0
Runtest=0
Gp="/C/Program Files (x86)/Google/google_appengine"
while getopts ":ctu" Option
do
    case $Option in
      c) Clear=1;;
      t) Runtest=1;;
      u) Upload=1;;
      *) echo "Unrecognized option -$Option";
         echo "Usage:  deploy -c -u";;
     esac
done
shift $(($OPTIND - 1))
if [[ $# > 0 ]]
then
    Root="$1"
else
    Root=`pwd`
fi

# Set the initial condition of the deployment directory
# If -c specified it is cleared and re-created
# If it does not exist it is created

cd "$Root" # Put ourselves in the root directory of the project

# Get rid of the existing deployment directory if necessary
if [[ -d ../deploy ]]
then
    if [[ $Clear == 1 ]]
    then
        rm -rf ../deploy
        if [[ $? != 0 ]]; then exit 1; fi
    fi
fi

# Create the deployment tree
mkdir -p ../deploy/petaapan/utilities
mkdir -p ../deploy/petaapan/publishsubscribeserver
if [[ $? != 0 ]]; then exit 1; fi
mkdir -p ../deploy/static/images
if [[ $? != 0 ]]; then exit 1; fi

# Get the control files
cp -dpu *.yaml ../deploy
if [[ $? != 0 ]]; then exit 1; fi

# Get favicon.ico
cp -pu ../../Administration/home/WebContent/favicon.ico ../deploy/static/images
if [[ $? != 0 ]]; then exit 1; fi

cd ../../Utilities/src/petaapan
if [[ $? != 0 ]]; then exit 1; fi
#cp -dpu __init__.py ../../../PublishSubscribeServer/deploy/petaapan
echo "" >../../../PublishSubscribeServer/deploy/petaapan/__init__.py
if [[ $? != 0 ]]; then exit 1; fi
cd utilities
if [[ $? != 0 ]]; then exit 1; fi
cp -dpu __init__.py reportException.py sendJsonMsg.py console_logger.py\
        ../../../../PublishSubscribeServer/deploy/petaapan/utilities
if [[ $? != 0 ]]; then exit 1; fi

# Copy main server application files
cd ../../../../PublishSubscribeServer/src/petaapan/publishsubscribeserver
if [[ $? != 0 ]]; then exit 1; fi
cp -dpu *.py ../../../deploy/petaapan/publishsubscribeserver
if [[ $? != 0 ]]; then exit 1; fi
cd ../../..

# Now we need to test the deployment to verify that it
# is complete
# Launch the development server running our application
if [[ $Runtest == 1 ]]
then
    python "$Gp/dev_appserver.py" --clear_datastore --address=0.0.0.0\
           "$Root/../deploy" &
    App_pid=$!

    # Launch the Agiman application
    
    cd ../../CMAP/CMAP/src
    sleep 5s
    echo "Loading Agiman application to test deployment"
    export PYTHONPATH="\
D:\\Users\\jonathan\\EclipseWorkspaces\\Repositories\\Petaapan\\Utilities\\src;\
D:\\Users\\Jonathan\\EclipseWorkspaces\\Repositories\\pymt"
    python storyboot.py --collaburl="localhost/subscribe"\
                        --repopath="D:\\Users\\jonathan\\EclipseWorkspaces\\Repositories\\CMAP-Data" \
                        --responseurl="localhost" --testserver \
                        --loglevel="info" --gitsub="github/estemenson/CMAP-Data"
    kill $App_pid
fi


# Upload the deployment to Google
if [[ $Upload == 1 ]]
then
    echo "Pushing PublishSubscribeServer to Google"
    python "$Gp/appcfg.py" --email=jgossage@gmail.com  update deploy/
    if [[ $? != 0 ]]; then exit 1; fi
fi

# Restore original directory
cd "$Root"
exit 0