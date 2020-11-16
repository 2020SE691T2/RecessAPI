#!/bin/sh

venv_name="db_venv"
os=$(uname -s)
os_v=$(uname -v)

if [ -d ${venv_name} ]; then
    # activate the virtual environment
    echo "Activating ${venv_name}"
    case ${os} in
        Darwin|Linux)
            echo "${os} detected."
            echo "Version: ${os_v}" 
            activate() { . $PWD/${venv_name}/bin/activate; }
            ;;
    
        CYGWIN*|MINGW32*|MINGW64*|MSYS*|MINGW*)
            echo "Windows operating system detected."
            echo "Version: ${os_v}"
            activate() { . $PWD/${venv_name}/Scripts/activate; }
            ;;
        
        *)
            echo "Operating system unknown"
            exit
            ;;
    esac
    activate
    
    echo "Building database"
    python main.py
else
    echo "virtual environment does not exist"
    echo "run create_and_update_venv.sh first"
fi