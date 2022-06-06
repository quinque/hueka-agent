#!/bin/sh 

sed "s/ , /,/g" | \
	jq -R '(. | split(",")) as $vals | [[["timestamp","naivecolor","light","rgbhex","latitude","longitude","description"], $vals] | transpose[] | {key:.[0],value:.[1]}] | from_entries' | \
	curl -s -X POST -H 'Content-Type: application/json' -d @- https://api.himmelueberkarlsruhe.de/

