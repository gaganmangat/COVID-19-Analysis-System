#!/bin/bash
for execution in 0 1 2 3 4
do
	for P in 16 36 49 64
	do	
		for N in 16^2, 32^2, 64^2, 128^2, 256^2, 512^2, 1024^2
		do
			echo "$P$N"
		done
	done
done