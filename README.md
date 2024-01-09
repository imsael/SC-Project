# SC-Project

This GitHub repository sets up a WiFi access point that implements "Time of Day" access control. It is based on a list of MAC addresses and predefined time intervals during which those MAC addresses are allowed to access services. Essentially, it allows only devices with specified MAC addresses to access the WiFi network during specific time periods.

Use Python to run it.

You will need to install hostapd aka SOFT AP and dnsmasq on your system to create the AP and give it an IP. You can install it in the terminal with this command

--$sudo apt-get install hostapd dnsmasq

Create a configuration file: /etc/hostapd/hostapd.conf
--$sudo emacs /etc/hostapd/hostapd.conf
The file contains the following configuration 

interface=wlp1s0 (wlp1s0 is the name of the wireless interface of our laptop.)
driver=nl80211 (Specifies the wireless driver to be used by hostapd. The nl80211 driver is commonly used on Linux systems.)
ssid=Wifi-SC (Is the name of our Wi-Fi network. This is what users will see when they scan for available networks.)
hw_mode=g (Specifies the Wi-Fi mode, such as "g” for 2.4 GHz band or “a” for 5 GHz band.)
channel=6 (Specifies the Wi-Fi channel to be used. We have to choose a channel that is not heavily used in our environment)
macaddr_acl=0 (Controls MAC address filtering. “0” means no filtering, and “1” means allow only MAC addresses specified in the “accept_mac_file”.)
auth_algs=1 (Specifies the authentication algorithms. 1 enables WPA (Wi-Fi Protected Access).)
ignore_broadcast_ssid=0 (Controls whether the SSID should be hidden (1) or broadcasted (0).)
wpa=2 (Specifies the version of WPA to use. 2 indicates WPA2.)
wpa_passphrase=Socrative (Specifies the pre-shared key (password) for WPA-PSK authentication.)
wpa_key_mgmt=WPA-PSK (Specifies the key management protocols used for authentication.)
wpa_pairwise=TKIP (Specifies the pairwise (unicast) cipher suites for WPA.)
rsn_pairwise=CCMP (Specifies the pairwise (unicast) cipher suites for RSN (Robust Security Network), used in WPA2.)
ctrl_interface=/var/run/hostapd (Configurates a parameter that specifies the directory path for the control interface socket.)

Deactivate the NetworkManager
--$sudo service NetworkManager stop
Assign an IP to our interface
--$sudo ip address add 192.168.1.1/24 dev wlp1s0
Activate our wireless interface
--$sudo ip link set wlp1s0

CONFIGURING DNSMASQ
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

“TIME OF DAY” BASED CONTROL
We have created a file named “mac_list.txt” which contains the MAC’S allowed and their time permission. (You can save in the same folder).

Then we look with the following command if there is an user connected with us: 
--$sudo arp -a
We obtain their MAC and IP and we look in that file if he can connected or not

In order to remove a user whose MAC address is not in the list or does not meet the time range we use these two commands:
--$sudo arp -d <IP>
--$sudo hostapd_cli -i wlp1s0 deauthenticate <MAC>
We repeat the control process every 5 seconds, this value can be determined very easily and conveniently









Video demo link: https://www.youtube.com/watch?v=ZqLch0Js73Q
