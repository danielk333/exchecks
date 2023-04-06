#!/bin/bash
for i in {1..10}
do
    echo "Iter $i"
    sleep 1
    if [ $i -gt 7 ]
    then
        echo "Something broke"
        exit 1
    fi
done
