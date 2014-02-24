Light Control Server 2.0
========================

This application provides a simple RESTful API for manipulating a Raspberry Pi's GPIO pins over HTTP. The two major features are:

 - Direct on/off GPIO pin manipulation
 - Scheduled GPIO pin manipulation (via cron)

Initial Setup
-------------

**Source**

First, get the source code from Bitbucket. The easiest way to do this is to do a `git clone` of the lightcontrol repo (don't worry, it's not that bad -- and [making it easier](https://bitbucket.org/zourtney/lightcontrol/issue/1/medium-make-easily-installable) is the list).

    git clone https://bitbucket.org/zourtney/lightcontrol.git
    cd lightcontrol
    git submodule update --init --recursive

Alternatively, you can get a zip file from the Downloads section on Bitbucket. However, you will need to manually install the [gpiocrust](https://github.com/zourtney/gpiocrust) dependency.

**3rd Party Dependencies**

Install the following dependencies using the [pip](https://pypi.python.org/pypi/pip/) package manager.

    pip install flask
    pip install requests
    pip install croniter
    pip install python-crontab==1.6

**NOTE:** you may need to run `pip install` under `sudo`.

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

To start the HTTP server, run `server.py` from the command line.

    python server.py

**Installing as a Service**

You can make the Light Control Server behave like a Unix service by dropping *service/lightcontrol.sh* into your */etc/init.d* directory. Currently, line 14 of the script defines `/home/pi/Development/lightcontrol` as Light Control Server's directory. Change this line if you installed the application elsewhere.

    sudo cp service/lightcontrol.sh /etc/init.d
    sudo chmod 755 /etc/init.d/lightcontrol.sh

Now you `start` and `stop` it at any time.

    sudo /etc/init.d/lightcontrol.sh start

**Running at Startup**

You'll probably want the server to run as soon as the Raspberry Pi boots up. To do this, register the service script.

    sudo update-rc.d /etc/init.d/lightcontrol.sh defaults

For more details, check out [this link](http://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html).

Clients
-------

**Webapp**

A full-featured webapp is available at the server root, [http://localhost:5000/](http://localhost:5000).

**Command line interface**

A command line interface is available by running *client.py*. In short, just define your switch name as an argument and *t* or *f* for turning the switch on or off (respectively).

    ./client.py -"Desk lamp" t

**Mobile**

There is a full-featured [Windows Phone client](http://www.windowsphone.com/en-us/store/app/lightcontrol/76eaf03e-8970-4957-bcca-d59486d2475f) available for free in the store. This client will be updated to be 2.0 compatible in the near future.