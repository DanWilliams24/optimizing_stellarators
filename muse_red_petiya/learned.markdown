# The Red Petiya - FPGA Board


## Setting Up Operating System
The Red Petiya is a board that can be used for a variety of tasks given the right attachments. 

Lets first talk about setup. The Red Petiya is a small board that uses a custom operating system etched onto an SD card. Instructions for this process can be found on the ReadtheDocs for Red Petiya here: 

 I used BalenaEtcher to install after downloading the correct OS from this link:


## Connecting to the Red Petiya

After inserting the formatted SD into the device, I moved to initial connection and setup. I used the following guide: https://redpitaya.readthedocs.io/en/latest/quickStart/connect/connect.html#direct-ethernet-cable-connection

You will find that they offer multiple ways to connect to the device: connection over LAN, connection over WiFi network, and direct ethernet. However upon examination, its clear that for setting this device up at PPPL, a direct ethernet connection method is the quickest way to get started. Along with following the guide, I implemented the following settings changes on my computer (MacOS Ventura) to get enable access:

Its important to note, I used an adapter to get ethernet port access on my machine, so your 'USB LAN 100' may be named differently. Most importantly, navigate to your machine's ethernet port settings once you have connected the Red Petiya and enabling DHCP, which Red Petiya requires inorder to connect to a machine.

 Systems Settings > Network > USB LAN 100 > Details > TCP/IP > Configure IPv4 > Set to 'Using DHCP'

Once this is done you should be able to connect to the Red Petiya via its web service which becomes available 30 seconds after being powered on. Use either the QR code on the Petiya or the last six digits of the MAC address like so 'rp-XXXXXX.local' to connect to the device through your favorite browser using the web address. 

### Additional Troubleshooting  

If you still encounter issues with connecting/accessing this web portal, one suggestion is to disable your firewall temporarily while your working with the Red Petiya. On my machine, I can still connect with it, but its worth trying. Another suggestion is to ensure your machine sees the ethernet connection and device. Go into Terminal and use the following command: arp -a

This will show all the entries in the Address Resolution Protocol(ARP) Cache. It should show both the IP and web address for the Red Petiya in the listing if your machine sees the connection. If you do not see the Red Petiya in the table, its very likely the case that there is a problem with either your ethernet cable or the Red Petiya itself. Remember that the OS requires 30 seconds after being powered on to start the web service, so be patient as arp -a will show no device present until about 30 seconds. If other issues arise, consider powering on and off the device, and at worst, power on and off your machine and reenable the network settings identtified earlier to attempt to address any network problems on your end.

## Software Development on the Red Petiya

The first step to running code on the Red Petiya is to enable remote development through the web portal. Go to 'rp-XXXXXX.local' through the web browser, and upon connection, select the application