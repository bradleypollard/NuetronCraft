Instructions for NeutronCraft - By Bradley Pollard (2012)
---------------------------------------------------------

-----
About
-----

NeutronCraft is a StarCraft inspired game, written in Pygame 1.9.1 for Python 3.1 and tested thoroughly on
the Raspberry Pi in Pygame 1.9.2pre for Python 3.2. By default, the Raspbian "Wheezy" distro (15/07/2012)
comes with only Pygame for Python 2.7 installed, thus to run NeutronCraft you will need to compile 
Pygame 1.9.2pre on the device. NOTE: Do not run NeutronCraft inside X.
 
-------------------------------
Installation of Pygame 1.9.2pre
-------------------------------

Thank you to croston on the Raspberry Pi forums, and the author of the "RPi Debian Python3" page on the RPi
wiki for their help with getting Pygame installed for Python 3.2.

(croston - http://www.raspberrypi.org/phpBB3/viewtopic.php?f=32&t=13032)
(RPi Wiki - http://elinux.org/RPi_Debian_Python3)

------------
Instructions - indented lines are commands to be written in Terminal.
------------

=Step 1=
Install the development version of Python 3.2 with the following line in terminal:

	sudo apt-get install python3-dev python3-numpy

=Step 2=
Get the Pygame source code and change to the new Pygame directory with the following lines:

	sudo apt-get install mercurial
	hg clone https://bitbucket.org/pygame/pygame
	cd pygame

=Step 3=
Install the following dependencies needed to build Pygame

	sudo apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
	sudo apt-get install libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev

*VERY IMPORTANT NOTE: When running the above "apt-get installs" you may experience 404 errors. If
		      you get ANY 404 errors, be sure to run the following lines after the installations
		      have finished:*

	sudo apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev --fix-missing
	sudo apt-get install libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev --fix-missing
		     
		      *This will fix the errors. If you do not run these lines, building Pygame will fail.*

=Step 4=
Now we build and install Pygame (takes about 15 minutes):

	python3 setup.py build
	sudo python3 setup.py install
	
Once this is complete and successful, you can run the game!

-----------------
Starting the Game
-----------------

When running NeutronCraft, DO NOT RUN THE GAME INSIDE X. Always start it from the command line. 

To start the game, change to the directory you have it stored in and enter the command

	python3 NeutronCraft.py

The game will launch full screen onto the Main Menu. To learn how to play, be sure to have your sound turned
on, and click "Help" on the menu. A tutorial will start walking you through the basics. 

Good luck, and have fun - thanks for trying Neutron Craft! -Bradley Pollard, 18.
