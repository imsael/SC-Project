# SC-Project

This GitHub repository sets up a WiFi access point that implements "Time of Day" access control. It is based on a list of MAC addresses and predefined time intervals during which those MAC addresses are allowed to access services. Essentially, it allows only devices with specified MAC addresses to access the WiFi network during specific time periods.

You will need to install hostapd aka SOFT AP and dnsmasq on your system to create the AP and give it an IP. You can install it in the terminal with this command
```bash
--$sudo apt-get install hostapd dnsmasq
```

Create a configuration file: /etc/hostapd/hostapd.conf
```bash
--$sudo emacs /etc/hostapd/hostapd.conf
The file contains the following configuration
``` 

````python
interface=wlp1s0
driver=nl80211                                                           
ssid=Wifi-SC 
hw_mode=g 
channel=6 
macaddr_acl=0 
auth_algs=1 
ignore_broadcast_ssid=0 
wpa=2 
wpa_passphrase=Socrative
wpa_key_mgmt=WPA-PSK 
wpa_pairwise=TKIP 
rsn_pairwise=CCMP 
ctrl_interface=/var/run/hostapd 
````

Deactivate the NetworkManager
--$sudo service NetworkManager stop
Assign an IP to our interface
--$sudo ip address add 192.168.1.1/24 dev wlp1s0
Activate our wireless interface
--$sudo ip link set wlp1s0

#CONFIGURING DNSMASQ
In order to dynamically assign IP addresses to the different users that connect to our AP we use the same dnsmasq.
To do this you need to add this in the configuration file /etc/dnsmasq.conf:
interface = wlp1s0
dhcp-range=192.168.1.2, 192.168.1.10, 12h
And we reset the tool to be able to apply the changes made.

--$sudo service dnsmasq restart

We can check for possible errors by doing:
systemctl status dnsmasq.service

Activate the AP
--$sudo hostapd /etc/hostapd/hostapd.conf

#“TIME OF DAY” BASED CONTROL
We have created a file named “mac_list.txt” which contains the MAC’S allowed and their time permission. (You can save in the same folder).

Then we look with the following command if there is an user connected with us: 
--$sudo arp -a
We obtain their MAC and IP and we look in that file if he can connected or not

In order to remove a user whose MAC address is not in the list or does not meet the time range we use these two commands:
--$sudo arp -d <IP>
--$sudo hostapd_cli -i wlp1s0 deauthenticate <MAC>
We repeat the control process every 5 seconds, this value can be determined very easily and conveniently




Use file Python to run it.

Video demo link: https://www.youtube.com/watch?v=ZqLch0Js73Q
