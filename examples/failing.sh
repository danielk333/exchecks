#!/bin/bash
for i in {1..30}
do
    echo "Iter $i"
    sleep 1
    if [ $i -gt 15 ]
    then
        echo "Something broke"
        exit 1
    fi
done
