#!/bin/bash
for i in {1..5}
do
   python worker.py &
done
flask run
