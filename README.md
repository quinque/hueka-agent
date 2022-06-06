# hueka-agent
## Publish data
The data to be published should be having following format:
```
timestamp , naivecolor , light , rgbhex , latitude , longitude , description
```
Since the order of the fields matters, new fields shall be only appended.

The publishing itself can be achieved like that:

```
4metadata.py | publish.sh
```
