

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


