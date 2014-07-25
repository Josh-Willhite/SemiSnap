#!/bin/bash
while [ true ]; do
	rsync -t images/*.png work-laptop:~/class_stuff/SemiSnap/images/
	sleep 2s
done
