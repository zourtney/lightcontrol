LightControl 2.0
================

This application provides a simple RESTful API for manipulating a Raspberry Pi's GPIO pins over HTTP. The two major features are:

 - Direct on/off GPIO pin manipulation
 - Scheduled GPIO pin manipulation (via cron)

**Multi-zone support is coming soon!**

Initial Setup
-------------

**Source**

First, get the source code from GitHub. The easiest way to do this is to do a `git clone` of the lightcontrol repo (don't worry, it's not that bad -- and [making it easier](https://github.com/zourtney/lightcontrol/issues/1) is on the list).

    git clone https://github.com/zourtney/lightcontrol.git
    cd lightcontrol
    git fetch && git checkout dev

Alternatively, you can get a zip file from the Downloads section on GitHub. However, you will need to manually install the [gpiocrust](https://github.com/zourtney/gpiocrust) dependency.

**3rd Party Dependencies**

LightControl has dependencies on a few 3rd party libraries. You can easily install them with the [pip](https://pypi.python.org/pypi/pip/) package manager. If you don't already have it, you can install pip via apt-get on Debian distributions.

    sudo apt-get install python-pip

Then install the dependencies:

    sudo pip install flask requests croniter python-crontab

**Troubleshooting**

If you encounter a dependency error along the lines of [`ValueError: invalid range specifier: 'root' ('root')`](https://gist.github.com/zourtney/9340796), attempt the [following steps](https://bugs.launchpad.net/python-crontab/+bug/1199761):

    sudo pip uninstall crontab
    sudo pip install python-crontab
    pip install python-crontab

Edit settings.json
------------------

Now edit the *settings.json* file. Add an entry into the `switches` array for every GPIO pin you wish to let the server control.

    {
      "switches": [
        {
          "name": "Desk lamp",
          "pin": 13,
          "value": 1,
          "initial": null
        }
        ...

Where:

- `name`: unique identifier
- `pin`: the GPIO pin to control
- `value`: the pin's current state. `0` for on, `1` for off.
- `initial`: state to set the pin on server startup. `0` for on, `1` for off, `null` for no change.

**NOTE 1:** the name may not contain an eqauls (`=`) sign.

**NOTE 2:** `0` is "on" and `1` is "off" because of that's how the 5v AC-controlling relays I've used work. If you're controlling DC, this will likely be "backwards." If this bothers you, complain in [Issues](https://github.com/zourtney/lightcontrol/issues).

REST API
--------

**switches**

- `GET /api/switches/` returns info about all server-managed GPIO pins and their current `value`s.
- `PUT /api/switches/` updates info about multiple server-managed GPIO pins. Useful for batch operations. All fields except `name` are changeable.
- `GET /api/switches/[name]` returns info about a single server-managed GPIO pin. `name` is that which is defined by the `name` field in *settings.json*.
- `PUT /api/switches/[name]` updates info about a single server-managed GPIO pin. All fields except `name` are changeable.

Data will be formatted just like the pin definitions in *settings.json*.

**schedules**

- `GET /api/schedules/` returns a list of all server-managed cron schedules.
- `POST /api/schedules/` creates a new server-managed cron schedule.
- `GET /api/schedules/[name]` returns a single server-managed cron schedule.
- `PUT /api/schedules/[name]` updates a single server-managed cron schedule.
- `DELETE /api/schedules/[name]` deletes a single server-managed cron schedule.

Data will be formatted like the following:

    {
      "cron": "0 12 * * *", 
      "next": "2014-02-19 12:00:00", 
      "enabled": true, 
      "name": "Lamp on", 
      "switches": [
        {
          "name": "Desk lamp", 
          "value": 0,
          ...
        },
        ...
      ]
    }

Running the Server
------------------

To start the HTTP server, run `lightcontrol.py` from the command line with the `start` argument. You will need to run as `sudo` to get access to the Raspberry Pi's GPIO pins.

    sudo ./lightcontrol.py start

**Installing as a Service**

You can make LightControl behave like a Unix service by dropping *init.d/lightcontrol.sh* into your */etc/init.d* directory. Currently, line 14 of the script defines `/home/pi/Development/lightcontrol` as LightControl's directory. Change this line if you installed the application elsewhere.

    sudo cp init.d/lightcontrol.sh /etc/init.d/
    sudo chmod 755 /etc/init.d/lightcontrol.sh

Now you `start` and `stop` it at any time.

    sudo /etc/init.d/lightcontrol.sh start

**Running at Startup**

You'll probably want the server to run as soon as the Raspberry Pi boots up. To do this, register the service script.

    sudo update-rc.d lightcontrol.sh defaults

For more details, check out [this link](http://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html).

Schedules
---------
TODO: explain schedules. Use screenshot from the bundled webapp.

Clients
-------

**Webapp**

A full-featured AngularJS webapp is available at the server root, [http://localhost:5000/](http://localhost:5000). You can toggle switches; you can create, edit, and delete schedules. Multi-zone support is coming soon.

**Command line interface**

A command line interface is available by running *lightcontrol.py* with the `-s` argument. Example:

    sudo ./lightcontrol.py -s "Desk lamp"=0

**Mobile**

There is a full-featured [Windows Phone client](http://www.windowsphone.com/en-us/store/app/lightcontrol/76eaf03e-8970-4957-bcca-d59486d2475f) available for free in the store. This client will be updated to be 2.0 compatible in the near future.