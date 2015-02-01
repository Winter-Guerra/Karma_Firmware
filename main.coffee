"use strict"

child_process = require 'child_process'

console.log "Hello World"

# Starting python script
child_process.spawn('python', ['./myo-raw/myo_raw.py'], {stdio: 'inherit'})


# # Connnect to a specific MYO using cylon.js
# cylon = require("cylon")
# cylon.robot(

# 	connections:
# 		bluetooth:
# 			adaptor: "ble"
# 			uuid: "80fba7af42c841bda5cfa139cd0640c8"

# 	devices:
# 		myo:
# 			driver: "myo"

# 	work: (robot) ->

# 		every 5.seconds(), () ->
# 			robot.myo.getFirmwareVersion (err, data) ->
# 				if err
# 					console.log "Error: ", err
# 					return
# 				else
# 					console.log "FirmwareVersion: ", data

# # Start the robot			
# ).start()