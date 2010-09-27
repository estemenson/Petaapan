#!/bin/bash -v
# Script to prepare Publish/Subscribe server for deployment to Google
# and optionally do the deployment
# The script will run in the root directory of the
# PublishSubscribe Eclipse project
#
# Usage: deploy [-c] [-t] [-u] root
# Options:  -c   Clear the deployment directory before starting
#           -t   Run tests from deployment directory
#           -u   Do the upload to Google
#           root Is the deployment directory

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
if [[ $? != 0 ]]; then exit 1; fi
mkdir -p ../deploy/static/images
if [[ $? != 0 ]]; then exit 1; fi

# Get the control files
cp -dpu *.yaml ../deploy
if [[ $? != 0 ]]; then exit 1; fi

# Get the application python files
cp -dpu *.py ../deploy
if [[ $? != 0 ]]; then exit 1; fi

# Get favicon.ico
cp -pu ../../Administration/home/WebContent/favicon.ico ../deploy/static/images
if [[ $? != 0 ]]; then exit 1; fi

# Copy utility python files
cp -dpu petaapan/*.py ../deploy/petaapan
if [[ $? != 0 ]]; then exit 1; fi
cd petaapan/utilities
cp -dpu __init__.py reportException.py sendJsonMsg.py ../../../deploy/petaapan/utilities
if [[ $? != 0 ]]; then exit 1; fi
cd ../..

# Now we need to test the deployment to verify that it
# is complete
# Launch the development server running our application
if [[ $Runtest == 1 ]]
then
    python "$Gp/dev_appserver.py" --clear_datastore --address=0.0.0.0\
           "$Root" &
    App_pid=$!

    # Launch our HTTP server that listens for notifications from Google
    sleep 5s
    python tests/testNotification.py &
    Notification_pid=$!

    # Run the subscription process to subscribe to the collaborative session
    python tests/launchSubscription.py http://poseidon:8080/ jgossage@gmail.com
    ret=$?
    if [[ $ret != 0 ]]
    then
        echo "Subscription process failed with error $ret"
        kill $Notification_pid
        kill $App_pid
        exit 1
    fi

    # Tell user to make Github talk to us
    if [[ $Upload == 1 ]]
    then
        read -p "Please tell Github to talk to us. When test is complete type 'y' if you still want to upload: "
        if [[ ! ($Var -eq 'y' || $Var -eq 'Y' || $Var -eq 'yes') ]]; then Upload=0; fi
    fi 
    # Kill the test apps
    kill $Notification_pid
    kill $App_pid
fi


# Upload the deployment to Google
if [[ $Upload == 1 ]]
then
    python "$Gp/appcfg.py" --email=jgossage@gmail.com  update ../deploy/
    if [[ $? != 0 ]]; then exit 1; fi
fi

# Restore original directory
cd "$Root"
exit 0