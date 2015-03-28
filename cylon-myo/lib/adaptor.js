/*
 * cylon-myo adaptor
 * http://cylonjs.com
 *
 * Copyright (c) 2015 Winter Guerra
 * Licensed under the Apache 2.0 license.
*/

// NOTE: Most of the functions here are boilerplate. The cylon.js bluetooth central.js adapter will handle the bluetooth connection to the Myo. However, there should probably be a function here to force a reconnect to another specific or random connection.

"use strict";

var Cylon = require('cylon');

var Adaptor = module.exports = function Adaptor(opts) {
	Adaptor.__super__.constructor.apply(this, arguments);


	// Grab the options given to the adapter constructor
	opts = opts || {};

};

Cylon.Utils.subclass(Adaptor, Cylon.Adaptor);


// Connect to the Myo. Note, this is already handled by the cylon.js bluetooth central.js adapter.
Adaptor.prototype.connect = function(callback) {

	callback();
};


// Disconnect from the myo. Note, this is already handled by the cylon.js bluetooth central.js adapter.
Adaptor.prototype.disconnect = function(callback) {
	callback();
};
