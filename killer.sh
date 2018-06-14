#!/bin/bash
process=$(ps aux | grep "python" | tr -s ' ' | cut -d ' ' -f2 | tr '\n' ' ')

for p in $process;
do
    kill -9 $p
done