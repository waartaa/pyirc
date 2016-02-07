
# ircb

A versatile IRC bouncer.


## Setup

If you want to set up `ircb` for development purpose. Follow the given steps

- Install Python3 and Python3 development packages for your distro, if not already there. In Fedora, it'd be:  
``sudo dnf install -y python3 python3-devel python3-pip python-virtualenvwrapper``

- Create a Python3 virtualenv:  
``mkvirtualenv ircb --no-site-packages -p /usr/bin/python3``

- Activate the virtualenv `ircb`:  
``workon ircb``

- Install dependencies:  
``pip3 install -r requirements.txt``

- Copy and extend ``ircb/config/default_settings.py``, as needed, to a custom location. say, ``/etc/ircb/settings.py``.
- [OPTIONAL] ``export IRCB_SETTINGS=<path to your custom settings file>``

- Install the project as a development dep ``python3 setup.py develop``

## Setting up data
- Creating a user:
  ```
  ircb users create USERNAME EMAIL [PASSWORD]
  ```

- Creating a network for a user:
  ```
  ircb networks create USER NETWORK_NAME HOST PORT NICK
  ```
  You'll get an access token as an output of the above. Use this as
  **server password** when configuring your IRC client to connect to ``ircb``.

## Running the app

### Quickstart
```
ircb run server
```

### Advanced

- Run stores as a different process: ``ircb run stores``
- Run bouncer: ``irc run server``

## Connecting for IRC client

Now, you should be able to connect to ``ircb`` from your IRC client at:
- host/port: ``localhost/9000``
- server password: ``<your network access token>``
