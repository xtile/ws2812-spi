# raspberry_ws2812 #
This module contains python routines to program the WS2812 RGB LED chips on the raspberry,
using the hardware SPI MOSI (so no other hardware is needed)

As the WS2812 communication needs strict timing, the DIN line cannot be driven from
a normal GPIO line with python (an interrupt on the raspberry would screw things up).
Thats' why this module uses the hardware SPI MOSI line, this does confirm to the
timing requirements.

More info on the WS2812: https://wp.josh.com/2014/05/13/ws2812-neopixels-are-not-so-finicky-once-you-get-to-know-them/

# Wiring of WS2812-Raspberry #
Connections from the Raspberry to the WS2812:
```
WS2812     Raspbery
GND   --   GND. At least one of pin 6, 9, 14, 20, 25
DIN   --   MOSI, Pin 19, GPIO 10
VCC   --   5V. At least one of pin 2 or 4
```

Of course the WS2812 can (should) be chained, the DOUT of the first
connected to the DIN of the next, and so on.


# Setup SPI on Raspberry #
First, enable the SPI hardware module on the SPI, using raspi-config, in
Advanced Options / SPI, and enabeling the SPI interface and the module loading:
    sudo raspi-config


Then, get the python spidev module:
```
git clone https://github.com/doceme/py-spidev.git
cd py-spidev
make
make install
```




Sample program that uses the module:
```

import ws2812
m = Matrix2812()
leds = [[10,0,0], [0,10,0], [0,0,10], [10, 10, 0]]
m.ws2812(leds)


#write 4 WS2812's, with the following colors: red, green, blue, yellow
ws2812.write2812(spi, [[10,0,0], [0,10,0], [0,0,10], [10, 10, 0]])
```
    
# Notes #
Note: this module tries to use numpy, if available.
Without numpy it still works, but is *really* slow (more than a second
to update 300 LED's on a Raspberry Pi Zero).
So, if possible, do:


```

sudo apt install python3-pip
sudo apt install libatlas3-base
sudo pip3 install numpy



```


TODO: 

1. увеличить размер буфера
https://www.raspberrypi.org/forums/viewtopic.php?t=39384
https://stackoverflow.com/questions/16427996/increase-spi-buffer-size-in-raspbian
https://raspberrypi.stackexchange.com/questions/65595/spi-transfer-fails-with-buffer-size-greater-than-4096
2. done



3. работа с матрицей, подбор таймингов

4. make changes to spidev

add spidev.bufsiz=32768 to the line in /boot/cmdline.txt and reboot sometime
test with cat /sys/module/spidev/parameters/bufsiz
git clone https://github.com/doceme/py-spidev.git
cd py-spidev/
nano spidev_module.c
change #define SPIDEV_MAXPATH 4096
make PYTHON=python3
sudo python3 setup.py install
rm -rf py-spidev/
