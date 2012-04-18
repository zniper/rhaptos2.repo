

install - OS level
==================



* Ubunutu 11.10

setup local 

1. Install ubunutu
   (kickstart file would be good here.)
   partition layout:
   / 30GB
   /swap 10GB (2*RAM Max + a bit)
   /home 30GB
   /var  (remainder)

2. install sshd
   ::
      sudo apt-get install openssh-server

   Versions?? 

   I think I made wrong choice not getting ubuntu server - will revamp.

3. install base pkgs

::
    sudo apt-get install lxc debootstrap bridge-utils
    sudo apt-get install emacs
    # because you know you have to have emacs because editing with pico is a joke...



4. kill network manager

   basically I want /etc/network/interfaces to be it.
::

   sudo sh -c "echo exit > /etc/default/NetworkManager"
   sudo sh -c "echo exit > /etc/default/NetworkManagerDispatcher"

   kill avahi
   sudo update-rc.d avahi-demon remove

   aaaarrgghghghghghg

   change resolv.conf to needed settings, and stop any other service stomping on it
   sudo chattr +i /etc/resolv.conf



5. seeting up networking statically

   seems the linux curse strikes - debian has /etc/networking/interfaces, but u=buntu has /etc/network/interfaces


bridge network:

::
    #replace this into file /etc/network/interfaces on a Ubunutu 11.10 (not debian afaik thats /etc/networking)
    # The loopback network interface
    auto lo
    iface lo inet loopback

    # The primary network interface
    auto eth0
    iface eth0 inet manual


    auto br0
    iface br0 inet static
	address 10.0.0.103
	network 10.0.0.0
	netmask 255.255.255.0
	gateway 10.0.0.1
	bridge_ports eth0
	bridge_stp off
	bridge_fd 0
	bridge_maxwait 0

    now restart networking ::

      sudo /etc/init.d/networking restart

    We should then have a successful bridged adaptor - br0 is wrapping eth0 as it were.


6. control groups

   it seems that this script, run on boot,will mount cgroups sensibly'
::

    init/cgroup-lite.conf

    pbrian@hpcube:/etc$ mount
    /dev/sda1 on / type ext4 (rw,errors=remount-ro)
    proc on /proc type proc (rw,noexec,nosuid,nodev)
    sysfs on /sys type sysfs (rw,noexec,nosuid,nodev)
    fusectl on /sys/fs/fuse/connections type fusectl (rw)
    none on /sys/kernel/debug type debugfs (rw)
    none on /sys/kernel/security type securityfs (rw)
    udev on /dev type devtmpfs (rw,mode=0755)
    devpts on /dev/pts type devpts (rw,noexec,nosuid,gid=5,mode=0620)
    tmpfs on /run type tmpfs (rw,noexec,nosuid,size=10%,mode=0755)
    none on /run/lock type tmpfs (rw,noexec,nosuid,nodev,size=5242880)
    none on /run/shm type tmpfs (rw,nosuid,nodev)
    cgroup on /sys/fs/cgroup type tmpfs (rw,relatime,mode=755)
    cgroup on /sys/fs/cgroup/cpuset type cgroup (rw,relatime,cpuset)
    cgroup on /sys/fs/cgroup/cpu type cgroup (rw,relatime,cpu)
    cgroup on /sys/fs/cgroup/cpuacct type cgroup (rw,relatime,cpuacct)
    cgroup on /sys/fs/cgroup/memory type cgroup (rw,relatime,memory)
    cgroup on /sys/fs/cgroup/devices type cgroup (rw,relatime,devices)
    cgroup on /sys/fs/cgroup/freezer type cgroup (rw,relatime,freezer)
    cgroup on /sys/fs/cgroup/net_cls type cgroup (rw,relatime,net_cls)
    cgroup on /sys/fs/cgroup/blkio type cgroup (rw,relatime,blkio)
    cgroup on /sys/fs/cgroup/perf_event type cgroup (rw,relatime,perf_event)


I am now deeply suspicious of the stuff on internet - there is a lot of out of date how tos.
I have reverted to reading the man pages... this is slower than planned

7. create a container

man lxc-create 


pbrian@hpcube:/etc/lxc$ cat /etc/lxc/lxc.conf
lxc.network.type=veth
lxc.network.link=br0
lxc.network.flags=up



sudo lxc-create -t ubuntu -f /etc/lxc/lxc.conf -n cnx01

...

Setting up lxcguest (0.7.5-0ubuntu8) ...
'ubuntu' template installed
'cnx01' created


Now, 

/var/lib/lxc/cnx01/rootfs  is where the rootfs lives.

pbrian@hpcube:/etc/lxc$ ls -l  /var/lib/lxc/cnx01/rootfs/etc/network/interfaces 
-rw-r--r-- 1 root root 63 2012-04-17 19:56 /var/lib/lxc/cnx01/rootfs/etc/network/interfaces

change the networking config and resolv.conf (or check they are ok)

lxc-start -n cnx01 -d



lxc-console --name cnx01

-> ctl-a q for quitting

config for the containier
less /var/lib/lxc/cnx01/config

root passwd problem - cheat and splunk shadow?
read the lxc-create script

Refer to the examples in /usr/lib/lxc/templates

biblio

http://lxc.teegra.net/#_setup_of_the_controlling_host
https://help.ubuntu.com/community/KVM/Networking
http://wiki.debian.org/NetworkConfiguration#The_resolv.conf_configuration_file
http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge#Bridging_and_Firewalling
 


