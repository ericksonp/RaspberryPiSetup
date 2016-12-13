#!/bin/bash

#setup the tsl lux detector
cd ~
sudo apt-get install i2c-tools libi2c-dev python-dev
git clone https://github.com/lexruee/tsl2561.git
cd tsl2561
sudo python setup.py install
sudo sed -i '$a dtparam=i2c1=on' /boot/config.test
sudo sed -i '$dtparam=i2c-arm=on' /boot/config.test
#sudo echo 'blacklist snd_bcm2835' >  ~/Desktop/blacklisttest.txt
sudo echo 'blacklist snd_bcm2835' >  /etc/modprobe.d/snd-blacklist.conf

#setup the neopixels
cd ~
sudo apt-get install build-essential python-dev git scons swig
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install

#setup the code needed for SHT31
cd ~
sudo apt-get install build-essential libi2c-dev i2c-tools python-dev libffi-dev
pip install cffi
pip install smbus-cffi
cd ~
git clone https://github.com/ericksonp/SHT31_PAE.git

#setup the mcp9808
sudo pip install RPi.GPIO
cd ~
git clone https://github.com/adafruit/Adafruit_Python_MCP9808.git
cd Adafruit_Python_MCP9808
sudo python setup.py install
