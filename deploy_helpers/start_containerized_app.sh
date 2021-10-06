echo "Creating containers and starting app..."
set -x

unzip -o stonk-monitor.zip
cd stonk-monitor

# check if running from correct dir
if [[ "$PWD" != *stonk-monitor ]]; then
    echo "Containerized app not started!"
    echo "Please run this script from the project's base directory (stonk-monitor/)"
    exit 0
fi

# for more info, see "up" definition in stonk-monitor/Makefile
make up

if !(docker ps -a | grep warehouse); then
     echo “ERROR: warehouse container failed to start”
     exit 1
fi

if !(docker ps -a | grep pipeliner); then
     echo “ERROR: pipeliner container failed to start”
     exit 1
fi

if !(docker ps -a | grep warehouse); then
     echo “ERROR: visualizer container failed to start”
     exit 1
fi

echo ""
echo "Containers up and running!"
echo "Visit $(curl -s ifconfig.me):8050 to view Dashboard."
