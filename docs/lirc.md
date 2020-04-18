# LIRC

This file is to house information related to working with LIRC.
It's purpose is to help you get up and running with it since I didn't
find it the easiest to work with when I started, and I had wished there
was more up to date information on it.

## Platform Support

While there are ports to macOS and Windows, I would still advise you use 
this with Linux if you can. In my experience, I found them much more difficult 
to get working and use. 

The macOS port is here: https://github.com/andyvand/LIRC
The macports version of it is here: https://www.macports.org/ports.php?by=library&substr=lirc

On Windows, there is a winLIRC program: http://winlirc.sourceforge.net/

On Linux, your system package manager will likely have it already.

## Check If LIRC Is Recieving and Interpretting Your Remote Commands

One way to check if LIRC is recieving your commands is using the `irw` 
utilty from LIRC. IF you run `irw /var/run/lirc/lircd`, assumming that
is where your lircd daemon is, and then start pressing buttons on the
remote, you should see codes and key names printed out into your 
terminal window.