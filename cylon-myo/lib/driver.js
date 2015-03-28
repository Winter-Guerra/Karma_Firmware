/*
 * cylon-myo driver
 * http://cylonjs.com
 *
 * Copyright (c) 2015 Winter Guerra
 * Licensed under the Apache 2.0 license.
*/

// NOTE: This driver uses the myo ble protocol as defined by thalmic labs on 3/27/2015. A copy of the specification can be found under myo-bluetooth-reference-headers. It can also be found at 'http://developerblog.myo.com/myo-bluetooth-spec-released/'.

"use strict";

var Cylon = require('cylon');

var Driver = module.exports = function Driver(opts) {
  Driver.__super__.constructor.apply(this, arguments);

  opts = opts || {};

  // Include a list of commands that will be made available to the API.
  this.commands = {
    // This is how you register a command function for the API;
    // the command should be added to the prototype, see below.
    hello: this.hello
  };
};

Cylon.Utils.subclass(Driver, Cylon.Driver);

Driver.prototype.start = function(callback) {
  callback();
};

Driver.prototype.halt = function(callback) {
  callback();
};

Driver.prototype.hello = function() {
  Cylon.Logger.info('Hello World!');
}
