# SC-Project

This GitHub repository sets up a WiFi access point that implements "Time of Day" access control. It is based on a list of MAC addresses and predefined time intervals during which those MAC addresses are allowed to access services. Essentially, it allows only devices with specified MAC addresses to access the WiFi network during specific time periods.

Use Python to run it.

You will need to install hostapd aka SOFT AP and dnsmasq on your system to create the AP and give it an IP. You can install it in the terminal with this command

--$sudo apt-get install hostapd dnsmasq
