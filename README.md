Light Control Server
====================

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

Now edit the *settings.json* file. Add an entry into the `pins` array for every GPIO pin you wish to let the server control.

    {
      "pins": [
        {
          "id": "1",
          "pin": 13,
          "value": 1,
          "initial": null
        }
        ...

Where:

- `id`: unique identifier
- `pin`: the GPIO pin to control
- `value`: the current pins state. `0` for on, `1` for off.
- `initial`: state to set the pin on server startup. `0` for on, `1` for off, `null` for no change.

REST API
--------

**outlets**

- `GET /outlets/` returns info about all server-managed GPIO pins and their current `value`s.
- `PUT /outlets/` updates info about multiple server-managed GPIO pins. Useful for batch operations. All fields except `id` are changeable.
- `GET /outlets/[id]` returns info about a single server-managed GPIO pin. `id` is that which is defined by the `id` field in *settings.json*.
- `PUT /outlets/[id]` updates info about a single server-managed GPIO pin. All fields except `id` are changeable.

Data will be formatted just like the pin definitions in *settings.json*.

**schedules**

- `GET /schedules/` returns a list of all server-managed cron schedules.
- `POST /schedules/` creates a new server-managed cron schedule.
- `GET /schedules/[name]` returns a single server-managed cron schedule.
- `PUT /schedules/[name]` updates a single server-managed cron schedule.
- `DELETE /schedules/[name]` deletes a single server-managed cron schedule.

Data will be formatted like the following:

    {
      "cron": "0 12 * * *", 
      "next": "2014-02-19 12:00:00", 
      "enabled": true, 
      "name": "Lamp on", 
      "outlets": [
        {
          "id": "0", 
          "value": 0
        }
      ]
    }

Running the Server
------------------

To start the HTTP server, run `server.py` from the command line.

    python server.py

**Installing as a Service**

You can make the Light Control Server behave like a Unix service by dropping the *service/lightcontrol.sh* in your */etc/init.d* directory.

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

**Provided**

This application comes with the following Light Control clients:

- A command line interface (*client.py*)
- A simple web client (*http://localhost:5000*)

Both of these are currently restricted to controlling four (4) pins. This is a legacy laziness that will be [cleaned up](https://bitbucket.org/zourtney/lightcontrol/issue/6/small-make-cli-and-web-client-handle) in due time.

**Mobile**

There is a full featured [Windows Phone client](http://www.windowsphone.com/en-us/store/app/lightcontrol/76eaf03e-8970-4957-bcca-d59486d2475f) available for free in the store.