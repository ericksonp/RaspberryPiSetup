#!/bin/bash

#prepare sensor test program
cd ~/RaspberryPiSetup
chmod 755 sensortest.sh 

#setup automatic time keeping
sudo cp /usr/share/zoneinfo/America/New_York /etc/localtime
sudo apt-get install ntp
sudo sed -i 's/0.debian.pool.ntp.org/ntp1.Virginia.Edu/g; s/1.debian.pool.ntp.org/ntp2.Virginia.Edu/g; s/2.debian.pool.ntp.org/ntp3.Virginia.Edu/g; s/3.debian.pool.ntp.org/ntp4.Virginia.Edu/g' /etc/ntp.conf

#setup the tsl lux detector
cd ~
sudo apt-get install i2c-tools libi2c-dev python-dev
git clone https://github.com/lexruee/tsl2561.git
cd tsl2561
sudo python setup.py install
sudo sed -i '$a dtparam=i2c1=on' /boot/config.txt
sudo sed -i '$a dtparam=i2c-arm=on' /boot/config.txt
sudo echo 'blacklist snd_bcm2835' > /tmp/snd-blacklist.conf
sudo cp /tmp/snd-blacklist.conf /etc/modprobe.d/snd-blacklist.conf

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
sudo pip install cffi
sudo pip install smbus-cffi
cd ~
git clone https://github.com/ericksonp/SHT31_PAE.git
cd ~

#setup the mcp9808
sudo pip install RPi.GPIO
cd ~
git clone https://github.com/adafruit/Adafruit_Python_MCP9808.git
cd Adafruit_Python_MCP9808
sudo python setup.py install

sudo reboot
cd RaspberryPiSetup
sudo ./sensortest.sh
