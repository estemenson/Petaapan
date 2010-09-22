rem This script starts up a SSH enabled environment
rem It expects that Msysgit will be found in the path
rem It expects that Msys will be found in the path after msysgit
rem This script is expected to run at startup to provide an
rem environment where SSH keys have been preloaded so that no prompts
rem are necessary when using SSH, either alone or in conjunction
rem with Git
rem It works in conjunction with scripts to Eclipse and set the
rem current version of Python
cmd /c ssh-agent /bin/bash -i