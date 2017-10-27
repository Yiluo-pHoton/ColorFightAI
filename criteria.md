Some important things to check:

How safe is this cell? (how many layers of empty cells around it?)

How close is this area to my closest cell? (How much time does it take for me to get there?)

Is there other cells around this area that will require very long time to occupy? (that is, they might be coming to this place as well)

How many neighbors in this area? (Don't get more than three neighbors)

Try to move along the wall

Do an injection style to invade the area

(coordinate), (value)
sort value high to low

priority:
- empty
	- close to my land
	- free spaces around
	- no neighbor (demote to 'occupied' if more than two different neighbors or if neighbor is fresh)
	- lower priority if there are close neighbors with long take over time
- occupied
	- low take over time (if lower than certain level, promote to 'empty')
	- if surrounded by my cells:
		- compare: time(renew my cells around) and time(take over)


evaluation:
global: where are the places with highest values
local: what is the highest value that is adjacent to my cells
	- compare value(path to globally highest) + value(globally highest) and value(local combined)
	- if i aim at globally highest, how likely will i lose my local land
path: what is the most efficient path to get to globally high value regions
	- compare time(path to globally highest value) and time(globally second highest)
