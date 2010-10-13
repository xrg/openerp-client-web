===========================================================================
OpenERP Web - the Web Client of OpenERP, the Enterprise Management Software
===========================================================================

.. contents::

Introduction
------------

OpenERP Web is the official web client of OpenERP developed by Tiny and Axelor.

Features:

    - High Performance
    - Light weight
    - Easy deployment
    - Clean & Ergonomic
    - Ajax enabled

OpenERP Web is known to work with all major web browsers available today,
including Firefox, IE6, IE7, Safari3 and Opera9.

Linux Installation
------------------

Here is the installation instructions for Debian based Linux distributions.
Tested on Debian Etch and Ubuntu Hardy. The procedure might work with other
Linux or similar distributions. See the docs on how to install the specified
Packages on your favourite distro.

Prerequisites:

    #. Python >= 2.4
    #. CherryPy >= 3.1.2
    #. Mako >= 0.2.4
    #. Babel >= 0.9.4
    #. FormEncode >= 1.2.2
    #. simplejson >= 2.0.9
    #. pyparsing >= 1.5.0

Remember, this version requires CherryPy3 which is conflicting with
CherryPy2 (used by TurboGears), so you can't install both in system area.
To overcome with the issue, we added support for local library installation
for OpenERP Web. In that case, just download the source package and do the
following::

    $ cd /path/to/openerp-web/lib
    $ ./populate.sh
    $ cd ..

This will install all required dependencies in private lib directory, and you
don't need to install anything...

The rest will describe how to install the client in system area...

Python::

    $ sudo apt-get install python python-dev build-essential
    $ sudo apt-get install python-setuptools

OpenERP Web::

    $ sudo easy_install -U openerp-web

all other dependencies will be installed automatically by setuptools...

Configuration:

Locate the ``doc/openerp-web.cfg`` in the installed EGG, and make appropriate
changes, especially:

.. sourcecode:: ini

    [openobject]
    server = "localhost"
    port = 8070
    protocol = "socket"

where:

* server is the OpenERP server host
* port is the OpenERP server port
* protocol is the protocol to be used (socket, http or https)

Now start the web server with ``openerp-web`` command::

    $ openerp-web

If you see message showing ``IOError: Port 8080 not free on '0.0.0.0'`` make
sure no other application is running on the specified port (8080 is default).

You can change port by changing ``server.socket_port`` value in ``openerp-web.cfg``.

If everything is fine, open your favourite web browser and type
http://localhost:8080/, and your can see welcome page with login screen.

Please make sure cookies are enabled in your browser.

Of course, OpenERP Server must be running at that time. You should create a
database from the DBAdmin interface by clicking on Database button that you can
see on the login screen. After creating a new database login with the
admin/admin or demo/demo to see OpenERP in action...

Run as service (Linux):
-----------------------

This has been tested on Ubuntu only::

    $ sudo cp /path/to/openerp_web-6.0-py2.5.egg/openerp-web/scripts/init.d/openerp-web /etc/init.d/
    $ sudo cp /path/to/openerp_web-6.0-py2.5.egg/openerp-web/doc/openerp-web.cfg /etc/

edit ``/etc/init.d/openerp-web``:

.. sourcecode:: ini

    USER="openerp"

and ``/etc/openerp-web.cfg``:

.. sourcecode:: ini

    log.access_file = "/var/log/openerp-web/access.log"
    log.error_file = "/var/log/openerp-web/error.log"

Now run following command to start the OpenERP Web automatically on
system startup::

    $ sudo mkdir /var/log/openerp-web
    $ sudo chown -R openerp /var/log/openerp-web
    $ sudo update-rc.d openerp-web

Start the deamon::

    $ sudo /etc/init.d/openerp-web start

Windows Installation
--------------------

Prerequisites

    #. Python >= 2.4
    #. CherryPy >= 3.1.2
    #. Mako >= 0.2.4
    #. Babel >= 0.9.4
    #. FormEncode >= 1.2.2
    #. simplejson >= 2.0.9
    #. pyparsing >= 1.5.0

Python:

Download and Install Python 2.5 and make sure that the dirs
``C:\Python25;C:\Python25\Script`` are in PATH environment.

Setuptools (or distribute):

Follow the `distribute installation`_ instructions for more details. This will install
recent version of ``easy_install`` tools.

.. _distribute installation: http://pypi.python.org/pypi/distribute/0.6.14#distribute-setup-py

OpenERP Web::

    > easy_install -U openerp-web

Configuration:

Please see `Linux Installation`_ doc for configuration/startup...

.. note::
    
    Use ``python C:\Python25\Scripts\openerp-web`` command to startup openerp-web.

Configure HTTPS (Linux)
-----------------------

The following text describes how to configure OpenERP Web for production
environment over HTTPS with Apache2.

mod_proxy + mod_headers + mod_ssl (Apache2)

See Apache manual for more information.

Apache configuration::

    <VirtualHost *:443>

        SSLEngine on
        SSLCertificateFile /etc/apache2/ssl/apache.pem

        <Proxy *>
            Order deny,allow
            Allow from all
        </Proxy>

        ProxyRequests Off

        ProxyPass        /   http://127.0.0.1:8080
        ProxyPassReverse /   http://127.0.0.1:8080

        RequestHeader set "X-Forwarded-Proto" "https"

        # Fix IE problem (http error 408/409)
        SetEnv proxy-nokeepalive 1

    </VirtualHost>

OpenERP Web configuration::

    tools.proxy.on = True

Block the OpenERP Web server port (firewall):

On Linux do this::

    $ iptables -A INPUT -i lo -j ACCEPT
    $ iptables -A INPUT -p tcp --dport 8080 -j REJECT

.. warning:: Don't block the localhost/127.0.0.1 (the first rule)

.. note::
    This method only works if you want your OpenERP Web application at the
    root of your server (https://www.example.com). OpenERP Web currently can't
    be deployed under a subdirectory, e.g. http://www.example.com/openerp.

    To overcome with the issue you can go with ``subdomain``, like:

        https://openerp.example.com

    See: http://openerp.org/wiki/index.php/InstallationManual/WebClientHTTPS

OpenERP Web as a WSGI Application
---------------------------------

OpenERP Web's root CherryPy application is exposed via
``openerp.application`` along with a few configuration functions. It's
therefore possible to easily run OpenERP Web via any WSGI server you
want. For instance using ``wsgiref.simple_server``::

    from wsgiref.simple_server import make_server
    from cherrypy._cpconfig import as_dict
    import openobject

    server = make_server('localhost', 8080, openobject.application)
    openobject.configure(as_dict('openerp-web.cfg'))
    openobject.enable_static_paths() # serve static file via the wsgi server
    server.serve_forever()

.. warning:: OpenERP Web's default configuration file is setup to
    integrate with CherryPy's multithreaded single-process server. You
    might have to provide different configuration options for
    e.g. session storage depending on the WSGI server you'll be using.

.. note:: If you don't serve static resources through Python WSGI
    (using CherryPy's static service), ensure that you serve the main
    static ressources (``openobject/static``) but also the static
    resources of all the addons you're using
    (``addons/${addon}/static``)

Web Browser Compatibilities
---------------------------

*OpenERP Web* is known to work best with Mozilla based web browsers.

Here is the list of supported browsers.

    * Firefox >= 1.5
    * Internet Explorer >= 6.0
    * Google Chrome >= 1.0
    * Safari >= 3.0
    * Opera >= 9.0

Support
-------

* http://openerp.com
* http://axelor.com

----

Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. All Rights Reserved.
