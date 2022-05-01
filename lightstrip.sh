#!/bin/bash

cd images



echo ""
echo "==== ALL THE JPEGS ===="
JPEGS=*.jpg
for i in $JPEGS
do
	
    	echo "Processing $i file..."
 		convert $i  -resize 1x100\!  $i

done

convert +append *.jpg ../out.png

cd ..
