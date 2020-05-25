Linux Infrared Remote Control (LIRC)
====================================

The stb-automator library relies on `LIRC <http://lirc.org>`_ to receive and
emit IR signals.

Installation
------------
Typically your system package manager will be able to
install LIRC quite easily e.g. `sudo apt install lirc` for Ubuntu.

If not, you may have to `compile and install it <https://www.lirc.org/html/install.html>`_
that way, but I would avoid that if possible.

Configuration
-------------
The two things you'll have to figure out on your own is the
`lirc_options.conf` file and the remote configuration file as these are
dependent on the hardware you use for your setup. LIRC configuration is
typically in `/etc/lirc/`.

For `lirc_options.conf`, the main change you'll want to make is to
change the driver from `devinput` to `default`. Devinput works fine for
receiving IR, but it will not allow you to emit IR. This driver is
dependent on your hardware, but LIRC just works with most devices on
this driver nowadays.

For the remote configuration file, if you're using a common remote
control, you may be able to find it in the LIRC remote control database.
Otherwise, you'll have to create it yourself. This can be done with
`LIRC's IR record utility <https://www.lirc.org/html/irrecord.html>`_.
However, I've had much better luck using a `RedRat3-II <http://lircredrat3.sourceforge.net/>`_ and
`RedRat's IR Signal Database <https://www.redrat.co.uk/software/ir-signal-database-utility/>`_
for creating the remote configuration file. RedRat3-II is now discontinued,
although its `driver's are still available <https://www.redrat.co.uk/support/firmware-drivers/#panel-58-2-0-0>`_,
but you could look into the RedRatX or see if you can find a RedRat3-II used.
Place this generated remote configuration file in `/etc/lirc/lircd.conf.d/`.

If you're using an Iguanaworks IR Transciever, you may find the discussion
here useful:
* https://github.com/iguanaworks/iguanair/issues/39

See the [LIRC configuration guide](https://www.lirc.org/html/configuration-guide.html) for more information.

Platform Support
----------------

While there are ports to macOS and Windows for LIRC, I've found Linux by
far the easiest to work with.

The macOS port is here: https://github.com/andyvand/LIRC
The macports version of it is here: https://www.macports.org/ports.php?by=library&substr=lirc

On Windows, there is a winLIRC program: http://winlirc.sourceforge.net/

On Linux, your system package manager will likely have it already.

Check If LIRC Is Recieving and Interpretting Your Remote Commands
-----------------------------------------------------------------

One way to check if LIRC is recieving your commands is using the `irw`
utilty from LIRC. If you run `irw /var/run/lirc/lircd`, assumming that
is where your lircd daemon is, and then start pressing buttons on the
remote, you should see codes and key names printed out into your
terminal window.