# Commands used to free mac bluetooth on yosemite

#!/bin/bash

# disable bluetooth
# OS X 10.8.2
# 2012-10-08

home=$HOME
bk=$home/backup-bluetooth-extentions
mkdir $bk

# sudo reboot with Shift Key # Safty Boot
# Login as Admin usert.

#---------------------------------------------------------------------
# Local Backup OFF
#---------------------------------------------------------------------
# sudo tmutil disable
# sudo tmutil disablelocal

#---------------------------------------------------------------------
# Agnet
#---------------------------------------------------------------------
# bluetooth
launchctl unload -w /System/Library/LaunchAgents/com.apple.bluetoothUIServer.plist
launchctl unload -w /System/Library/LaunchAgents/com.apple.bluetoothAudioAgent.plist

#---------------------------------------------------------------------
# Daemon
#---------------------------------------------------------------------
sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.blued.plist
sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.bnepd.plist
sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.IOBluetoothUSBDFU.plist

#---------------------------------------------------------------------
# Extentions
#---------------------------------------------------------------------
# Driver
sudo mv /System/Library/Extensions/AppleBluetoothMultitouch.kext $bk
sudo mv /System/Library/Extensions/IOBluetoothFamily.kext $bk
sudo mv /System/Library/Extensions/IOBluetoothHIDDriver.kext $bk

# Bluetooth Mouns & Keyboard
sudo mv /System/Library/Extensions/AppleHIDKeyboard.kext/Contents/PlugIns/AppleBluetoothHIDKeyboard.kext $bk
sudo mv /System/Library/Extensions/AppleHIDMouse.kext/Contents/PlugIns/AppleBluetoothHIDMouse.kext $bk

#---------------------------------------------------------------------
# touch
sudo touch /System/Library/Extensions

echo 'Shut Down & Restart'


## Reversed
home=$HOME
bk=$home/backup-bluetooth-extentions
#mkdir $bk

# sudo reboot with Shift Key # Safty Boot
# Login as Admin usert.

#---------------------------------------------------------------------
# Local Backup OFF
#---------------------------------------------------------------------
# sudo tmutil disable
# sudo tmutil disablelocal

#---------------------------------------------------------------------
# Agnet
#---------------------------------------------------------------------
# bluetooth
launchctl load -w /System/Library/LaunchAgents/com.apple.bluetoothUIServer.plist
launchctl load -w /System/Library/LaunchAgents/com.apple.bluetoothAudioAgent.plist

#---------------------------------------------------------------------
# Daemon
#---------------------------------------------------------------------
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.blued.plist
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.bnepd.plist
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.IOBluetoothUSBDFU.plist

#---------------------------------------------------------------------
# Extentions
#---------------------------------------------------------------------
# Driver
sudo cp $bk/AppleBluetoothMultitouch.kext /System/Library/Extensions/AppleBluetoothMultitouch.kext
sudo cp $bk/IOBluetoothFamily.kext /System/Library/Extensions/IOBluetoothFamily.kext
sudo cp $bk/IOBluetoothHIDDriver.kext /System/Library/Extensions/IOBluetoothHIDDriver.kext

# Bluetooth Mouns & Keyboard
sudo cp -R $bk/AppleBluetoothHIDKeyboard.kext /System/Library/Extensions/AppleHIDKeyboard.kext/Contents/PlugIns/AppleBluetoothHIDKeyboard.kext

sudo cp -R $bk/AppleBluetoothHIDMouse.kext /System/Library/Extensions/AppleHIDMouse.kext/Contents/PlugIns/AppleBluetoothHIDMouse.kext

#---------------------------------------------------------------------
# touch
sudo touch /System/Library/Extensions

echo 'Shut Down & Restart'
