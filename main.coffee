"use strict"

child_process = require 'child_process'

console.log "Hello World"

# Starting 

# # Starting python script
# child_process.spawn('python', ['./myo-raw/myo_raw.py'], {stdio: 'inherit'})

# console.log "test over"


# Connnect to a specific MYO using cylon.js
cylon = require("cylon")
cylon.robot(

	connections:
		edison: 
			adaptor: 'intel-iot'

	devices:
		servo:
			driver: 'servo'
			pin: 0

	work: (my) ->
		angle = 45
		my.servo.angle angle
		every 1.second(), ->
			angle = angle + 45
			if angle > 135
				angle = 45
			my.servo.angle angle
			return
		return

# Start the robot			
).start()