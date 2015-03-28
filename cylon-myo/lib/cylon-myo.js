/*
 * cylon-myo
 * http://cylonjs.com
 *
 * Copyright (c) 2015 Winter Guerra
 * All rights reserved.
*/

// NOTE: Look into driver.js to see where the communication magic happens!

'use strict';

var Adaptor = require('./adaptor'),
		Driver = require('./driver');

module.exports = {
	// Adaptors your module provides, e.g. ['spark']
	// This should provide none since we are offloading all that work to the central.js adapter.
	// adaptors: ['myo'],

	// Drivers your module provides, e.g. ['led', 'button']
	drivers: ['myo'],

	// Modules intended to be used with yours, e.g. ['cylon-gpio']
	// The ollie module that uses cylon-ble did not include this line.
	// dependencies: ['cylon-ble'],

	adaptor: function(opts) {
		return new Adaptor(opts);
	},

	driver: function(opts) {
		return new Driver(opts);
	}
};
