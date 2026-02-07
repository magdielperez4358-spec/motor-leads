#!/data/data/com.termux/files/usr/bin/bash

while true
do
    pgrep -f main.py > /dev/null
    if [ $? -ne 0 ]; then
        echo "Motor caído — reiniciando..."
        cd ~/motor-leads
        python main.py &
    fi
    sleep 15
done

