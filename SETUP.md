# Setup Guide

My personal guide to set up the photobox on a Raspberry Pi 2 Model B with a TP-Link WiFi dongle.

## Preparations

1. Copy the latest rasbian image to the SD card
1.1. Create file named `ssh` in the boot partition to allow ssh connections
1. Connect the pi to the network (via ethcernet cable is totally fine)
1. Connect to the pi via ssh

```bash
sudo apt-get update && sudo apt-get upgrade  # udpate pi
mkdir ~/code  # create working directory
sudo apt-get install git  # install git
```

## Setup photobox

```bash
cd ~/code
git clone https://github.com/mathebox/photobox/
pip3 install -r requirements.txt
sudo apt install gphoto2 python3-pip
```

### Install epeg

```bash
sudo apt-get install autoconf libtool libjpeg-dev libexif-dev
cd ~/code
git clone https://github.com/mattes/epeg.git
cd epeg/
autoreconf -i
./autogen.sh
make
sudo make install
sudo ldconfig
```

### Autostart photobox

```bash
sudo vim.tiny /lib/systemd/system/photobox.service
```

<details>
  <summary>New content of /lib/systemd/system/photobox.service</summary>

```
[Unit]
Description=Photobox
After=multi-user.target

[Service]
User=pi
Type=idle
ExecStart=/usr/bin/python3 /home/pi/code/photobox/run.py

[Install]
WantedBy=multi-user.target
```
</details>

```bash
sudo chmod 644 /lib/systemd/system/photobox.service
sudo systemctl daemon-reload
sudo systemctl enable photobox
```

## Host Wifi Access point

### Create WiFi

Useful resources:
- https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/
- https://www.elektronik-kompendium.de/sites/raspberry-pi/2002171.htm

```bash
sudo apt-get install hostapd 
```

#### Fix driver for TP-Link WiFi dongle

Only applicable if `lsusb` yields "Realtek Semiconductor Corp. RTL8188EUS 802.11n Wireless Network Adapter"

- https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=54946&p=1427675#p1427675
- https://www.raspberrypi.org/forums/viewtopic.php?uid=81098&f=28&t=62371&start=0#p462982


```bash
sudo apt purge firmware-realtek
mkdir ~/code/wifi-driver
cd ~/code/wifi-driver
uname -a  # to get kernel and build number
wget http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-[kernel]-[biuild].tar.gz  # to get patched kernel (see example below)
tar xzf 8188eu-5.10.11-v7-1399.tar.gz
./install.sh
```

#### Example

- `uname -a` => Linux raspberrypi 5.10.11-v7+ #1399 SMP Thu Jan 28 12:06:05 GMT 2021 armv7l GNU/Linux
  - Kernel: 5.10.11-v7
  - Build: 1399
- `wget http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-5.10.11-v7-1399.tar.gz`


### Configure Hostapd

```bash
sudo vim.tiny /etc/hostapd/hostapd.conf
```

<details>
  <summary>Content of /etc/hostapd/hostapd.conf</summary>

```
interface=wlan0
ssid=[NETWORK-NAME]
channel=1
hw_mode=g
ieee80211n=1
ieee80211d=1
country_code=DE
wmm_enabled=1
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=[PASSWORD]
```
</details>

```bash
sudo vim.tiny /etc/default/hostapd
```

<details>
  <summary>Lines to be added to /etc/default/hostapd</summary>

```
RUN_DAEMON=yes
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```
</details>

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl enable hostapd
```

### DHCP

```bash
sudo vim.tiny /etc/dhcpcd.conf
```

<details>
  <summary>Lines to be added to the end of /etc/dhcpcd.conf</summary>

```
interface wlan0
static ip_address=192.168.1.1/24
sudo systemctl daemon-reload
sudo systemctl restart dhcpcd
```
</details>

### DNS Server

```bash
sudo apt-get install dnsmasq
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf_orig
sudo vim.tiny /etc/dnsmasq.conf
```

<details>
  <summary>New content of /etc/dnsmasq.conf</summary>

```bash
interface=wlan0  # DHCP-Server only for WiFi,
no-dhcp-interface=eth0  # not for ethernet

dhcp-range=192.168.1.100,192.168.1.200,255.255.255.0,24h  # IPv4 range and lease time
dhcp-option=option:dns-server,192.168.1.1  # DNS
```
</details>

```bash
dnsmasq --test -C /etc/dnsmasq.conf  # test dns config
sudo systemctl restart dnsmasq
sudo systemctl status dnsmasq  # check status
sudo systemctl enable dnsmasq  # enable autostart
```
