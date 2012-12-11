=========================
Routing, bridging and LXC
=========================

We are using Linux COntainers as a means of creating distinct and seperate servers running cheaply on a server.

The 'plain vanilla' means is referenced here :http://frozone.readthedocs.org/en/latest/install-os.html

We have approximately 6 virtual servers in the 'eco-system' of frozone. 

This gives us a host machine, with half a dozen containers but they all sit as transparently visible IPs on the same network as the host.  This is the default  solution for putting in LXC containers.

This is fine for say having a server in the physical office, and usig that to develop on.  It all looks fine, when looking at the REST API on 10.0.0.10 from your laptop on 10.0.0.20.

We intend production machines to be on publically routable IPs, so they will act as if they are in the same network.

However, there is a clear example where we have one server, with one
public IP address, and on that we want to host 6 servers, but they need to 
be on a virtual LAN *inside* the host server.


This will be a virtual NAT'd LAN inside a sinlge IP'd server.




2. on the host set up bridging so that I have the real eth0 replaced
   by br0, configured in /etc/network/interfaces::


	# The loopback network interface
	auto lo
	iface lo inet loopback

	# The primary network interface
	auto eth0
	iface eth0 inet manual #let bridge cope with this


	auto br0
	iface br0 inet static
	    address 10.0.0.100
	    network 10.0.0.0
	    netmask 255.255.255.0
	    gateway 10.0.0.1
	    bridge_ports eth0   
	    bridge_stp off      #no need for spanning any trees.
	    bridge_fd 0         #speed
	    bridge_maxwait 0    #speed
  


3. set up a container, and in it set up its networking, tell it to use
   br0 as ethernet device via lxc.conf ::

    lxc.network.type=veth
    lxc.network.link=br0

3.a. Set up networking on the VM container to be using ::

	auto eth0
	iface eth0 inet static
	    address 10.0.0.104
	    network 10.0.0.0
	    netmask 255.255.255.0
	    gateway 10.0.0.1


4. This works::



	pbrian@hpcube:~$ brctl show
	bridge name     bridge id           STP     enabledinterfaces
	br0             8000.3cd92b0c2332   no      eth0
						    vethMSgJ2C     
						    veth5zepFK
						    vethGf3cpg
						    vethLuS6QF
						    vethQCFKhR
						    vethYFiXKj
						    vethYe2Qah
						    vethYxbXON
						    vethmebbUH
						    vethrGpf3e
						    vethrtk6UN


The containers can see and be seen from anywhere on my internal office
network 10.0.0.0/24 (and externally if I open up the linksys etc).

But this is because the VM ison the same IP network as the host and
the external gateway.  So although the bridge is doing all the Level 2
packet shifting, nothing ever fails at level 3.


Start from the beginning
========================

We now will create a virtual switch (bridge) that connects all the containers- essentially plugging the containers ethernet wires into the hub.(?)

This switch is then given a virtual NIC card (a tap), and an IP on the VLAN assigned to it.

Then we create a NAT router on the host, so the NIC that is now attached to the switch *and* the real NIC on the host, are connected by a NAT router in the kernel.

We can then see any host on any port from within the LAN, and can route externally over SNAT to say bbc.co.uk, and can either set up any host interanlly to have DMZ / port access, or more likely set nginx on the host to reverse proxy for external viewing.

This *may* be a suitable set up for production, bouncing off one webserver / loadbalancer to various backend servers.  


  

1. Linux and bridging.

ref: http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge#Bridging_and_Firewalling

A bridge device is a virtual switch - a layer 2 device that moves
Ethernet packets not IP Packets. It forward broadcasts packets to all
ports on the Ethernet and only sends traffic to (virtual) ports that
have specific MAC addresses on them.

Program is brctl and is included in bridge-utils.


So we have a switch that will move Ethernet frames around for us.
Lets plug into that a ethernet adaptor from a PC.


Tap device
----------

http://en.wikibooks.org/wiki/QEMU/Networking#TAP_interfaces
http://people.gnome.org/~markmc/qemu-networking.html
http://blog.bofh.it/debian/id_379

Setting up the Switch 
---------------------

Create the virtual switch device (Layer 2 bridge)
 sudo brctl addbr br1

Create a tun device (virtual NIC) 
 sudo ip tuntap add dev tap0 mode tap user root

Attach the tap device (NIC) to the switch (ie 'plug' the switch into the LAN)
 sudo brctl addif br1 tap0

GIve that NIC an address on the LAN
 sudo ifconfig br1 10.1.1.1 netmask 255.255.255.0 broadcast 10.1.1.255

Now I should be able to see my bridge on the host::

 pbrian@hpcube:~$ brctl show
 bridge name    bridge id            STP enabled    interfaces
 br0        8000.3cd92b0c2332        no             eth0
 br1        8000.5e8ae4af4b7d        no             tap0

Change the instructions for LXC to use the above bridge for new LXC::

 pbrian@hpcube:~$ cat /etc/lxc/taplxc.conf
 lxc.network.type=veth
 lxc.network.link=br1
 lxc.network.flags=up

create container
 sudo lxc-create -t ubuntu -f /etc/lxc/vlanlxc.conf -n cnx6


update using fab file::

    fab -H fillet.cnx.rice.edu -f fab_lxc.py preboot:vhostname=cnx1,vhostip=10.1.1.6
    # be careful here need to sort out ssh keys across fillet 


Change the interface defintions ::

 pbrian@hpcube:~$ cat /var/lib/lxc/cnx6/rootfs/etc/network/interfaces
 #from frozone tmpl 
 auto lo
 iface lo inet loopback

 auto eth0
 iface eth0 inet static
     address 10.1.1.6
     network 10.1.1.0
     netmask 255.255.255.0
     gateway 10.1.1.1
     broadcast 10.1.1.255
     dns-nameservers 128.42.178.32 128.42.209.32
     dns-search cnx.rice.edu
     

So veth type created *should* link to br1 ::

 pbrian@hpcube:~$ brctl show
 bridge name    bridge id            STP enabled    interfaces
 br0        8000.3cd92b0c2332        no             eth0
 br1        8000.5e8ae4af4b7d        no             tap0
						    vethh4V8pY


Yayme!!


login to container ::

    root@cnx6:~# ping 10.1.1.1
    PING 10.1.1.1 (10.1.1.1) 56(84) bytes of data.
    64 bytes from 10.1.1.1: icmp_req=1 ttl=64 time=1.90 ms
    64 bytes from 10.1.1.1: icmp_req=2 ttl=64 time=0.056 ms
    64 bytes from 10.1.1.1: icmp_req=3 ttl=64 time=0.051 ms

yayme * 2 



Now, we have a switch on the 10.1.1.1 ip (br1), and it needs to talk to
the real host NIC card.  We need to set up a NAT ::

   $ sudo iptables-restore < /etc/iptables.rules

   pbrian@fillet:~$ cat /etc/iptables.rules
   *nat
   :PREROUTING ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]

   -A PREROUTING -d 128.42.169.25/32 -i eth0 -p tcp -m tcp --dport 22210 -j DNAT --to-destination 10.1.1.6:22

   #from world to .6
   #-A PREROUTING -d 128.42.169.25 -i eth0 -j DNAT --to-destination 10.1.1.6


   -A POSTROUTING -s 10.1.1.0/24 -o eth0 -j SNAT --to-source 128.42.169.25
   COMMIT

   #snat - all traffic from 10.1.1.0 will go out to internet looking like comes from 128.

Testing it
----------

ping from container to anywhere::
   
    ubuntu@cnx2:~$ ping www.google.com
    ...
    64 bytes from dfw06s16-in-f19.1e100.net (74.125.227.115):...


can I see the webserver running on a container, from the host::

    pbrian@fillet:~$ wget 10.1.1.7


Using the VLAN with firefox
===========================

Two approaches

1. tunnel X from a server inside the 10.1.1.0/24 network, so run xfce4 on a container and just display locally.  This is a good one, configuration a bit fiddly - so I shall leave it for later.

2. create  SOCKS5 proxy, so that firefox tunnels all its requests through the ssh tunnel and out in 10.1.1.0/24 network. This is by far the simplest approach, and works fine for now, also allowing test systems to run locally.


login to a server on the 10.1.1.0 network::

  $ ssh ubuntu@fillet -p 22217
    
    I have setup a port forwarding on fillet to go through to port 22 on 10.1.1.7 already.  
    So this should log us into that remote machine
  $ exit

  $ ssh -D 8081 -N ubuntu@fillet -p 22217

  Also set ::


    network.proxy.socks_remote_dns = true

  so all DNS is run from remote end too.

.. figure:: socksProxy.jpg
   :scale: 33 %

.. figure:: dnsviafillet.png
   :scale: 33 %

   

Acknowledgements
----------------

A big tip o' the hat to macker.  Thanks.
