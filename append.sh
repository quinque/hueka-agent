#!/bin/bash

currdate=$(date '+%Y-%m-%d')

if [ ! -e "skyrecords" ]; then
	mkdir skyrecords
fi

if [ ! -e "skyrecords/$currdate" ]; then
	echo "creating $currdate folder"
	mkdir skyrecords/$currdate
	cp now_naive.png skyrecords/${currdate}/${currdate}_naive.png
	cp now_loglightness.png skyrecords/${currdate}/${currdate}_loglightness.png


else 
	echo "skyrecords/$currdate exists, appending.."
	convert +append skyrecords/${currdate}/${currdate}_naive.png now_naive.png PNG24:skyrecords/${currdate}/${currdate}_naive.png
	convert +append skyrecords/${currdate}/${currdate}_loglightness.png now_loglightness.png  PNG24:skyrecords/${currdate}/${currdate}_loglightness.png
	convert +append skyrecords/${currdate}/${currdate}_photo.png now_photo.png PNG24:skyrecords/${currdate}/${currdate}_photo.png

fi  


