#!/usr/bin/bash
#01:00.0 RAM memory: Xilinx Corporation Device 6014 (rev 06)

echo 0 > /sys/bus/pci/slots/0000:03:00.0/power
insmod pciDriver/src/driver/pciDriver.ko
#${IPYTHON} notebook --port 8889 --no-browser
#rmmod pciDriver
