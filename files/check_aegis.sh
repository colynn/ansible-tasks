#!/bin/bash

ps -aef | grep -q aegis
if [ $? != 0 ];then
    echo -n "no aegis"
    exit 0
fi

cat /usr/local/aegis/aegis_client/aegis_00_79/data/data.2 |grep -i clean | grep /bin
if [ $? != 0 ]; then
    echo -n "no clean"
    exit 0
fi
