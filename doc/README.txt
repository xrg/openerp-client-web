===============================================================================
OpenERP Web - the Web Client of OpenERP, the Enterprise Management Software
===============================================================================

    1. Introduction
    2. Linux Installation
    3. Run as service (Linux)
    4. Windows Installation
    5. Configure over HTTPS
    6. Web browser compatibilities
    7. Support

-------------------------------------------------------------------------------
1. INTRODUCTION
-------------------------------------------------------------------------------

OpenERP Web is the official web client of OpenERP developed by Tiny and Axelor.
It's built on TurboGears (http://www.turbogears.org).

Features:

    - High Performance
    - Light weight
    - Easy deployment
    - Clean & Ergonomic
    - Ajax enabled
    
OpenERP Web is known to work with all major web browsers available today, 
including Firefox, IE6, IE7, Safari3 and Opera9.

-------------------------------------------------------------------------------
2. LINUX INSTALLATION
-------------------------------------------------------------------------------

Here is the installation instructions for Debian based Linux distributions.
Tested on Debian Etch and Ubuntu Hardy. The procedure might work with other 
Linux or similar distributions. See the docs on how to install the specified 
Packages on your favourite distro.

Prerequisites:

    1. Python >= 2.4
    2. OpenERP Server >= 5.0.0
    3. TurboGears >= 1.0.7 < 1.1b1

OpenERP Server:

    To install OpenERP Server, please follow the instructions provided in 
    the official OpenERP Installation guide.

TurboGears:

    $ sudo apt-get install python-setuptools
    $ sudo easy_install "TurboGears==1.0.8"
    
or

    $ wget http://peak.telecommunity.com/dist/ez_setup.py
    $ sudo python ez_setup.py
    $ sudo easy_install "TurboGears==1.0.8"

OpenERP Web:

    $ sudo easy_install openerp-web
    
or 
    
    $ sudo easy_install http://openerp.com/download/stable/source/openerp-web-5.0.0.tar.gz

Configuration:

    Locate the `config/default.cfg` in the installed `EGG`, and make 
    appropriate changes, especially:

    [openerp]
    server = "localhost"
    port = 8070
    protocol = "socket"

    where:

    server is the OpenERP server host...
    port is the OpenERP server port...
    protocol is the protocol to be used (socket, http or https)

Now start the web server with `start-openerp-web` command:

    $ start-openerp-web

If you see message showing `cherrypy._cperror.NotReady: Port not free.` make
sure no other application is running on the specified port (8080 is default).

You can change port for by changing `server.socket_port` value in
`config/default.cfg`.

If everything is fine, open your favourite web browser and type 
http://localhost:8080, and your can see welcome page with login screen.

Don't forget to enable cookies !

Of course, OpenERP Server must be running at that time. You should create a
database from the DBAdmin interface by clicking on Manage button that you can
see besides the Database selection box. After creating a new database login
with the admin/admin or demo/demo to see OpenERP in action...

-------------------------------------------------------------------------------
3. Run as service (Linux):
-------------------------------------------------------------------------------

This has been tested on `ubuntu` only.

    $ sudo cp /path/to/openerp_web-5.0.0-py2.5.egg/scripts/openerp-web /etc/init.d
    $ sudo cp /path/to/openerp_web-5.0.0-py2.5.egg/config/default.cfg /etc/openerp-web.cfg

edit `/etc/init.d/openerp-web`:

    USER="terp"

and `/etc/openerp-web.cfg`:

    args="('server.log',)" ==> args="('/var/log/openerp-web.log',)"

Now run following command to start the OpenERP Web automatically on system startup.

    $ sudo update-rc.d openerp-web

Start the deamon:

    $ sudo /etc/init.d/openerp-web start

-------------------------------------------------------------------------------
4. WINDOWS INSTALLATION
-------------------------------------------------------------------------------

Prerequisites

    1. Python >= 2.4
    2. OpenERP Server >= 5.0.0
    3. TurboGears >= 1.0.7 < 1.1

Python:

    Download and Install Python 2.5 and make sure that the dirs 
    `C:\Python25;C:\Python25\Script` are in PATH environment.

OpenERP Server:

    To install OpenERP Server, please follow the instructions provided in 
    the official OpenERP Installation guide.

TurboGears:

    Install setuptools package from http://cheeseshop.python.org/packages/2.5/s/setuptools/setuptools-0.6c9.win32-py2.5.exe

    > easy_install "TurboGears==1.0.8"

OpenERP Web:

    > easy_install openerp-web
    
or

    > easy_install http://openerp.com/download/stable/source/openerp-web-5.0.0.tar.gz

Configuration:

    Locate the `config/default.cfg` in the installed `EGG`, and make 
    appropriate changes, especially:

    [openerp]
    server = "localhost"
    port = 8070
    protocol = "socket"

    where:

    server is the OpenERP server host...
    port is the OpenERP server port...
    protocol is the protocol to be used (socket, http or https)

Now start the the web server with `start-openerp-web` command:

    > start-openerp-web

If you see message showing `cherrypy._cperror.NotReady: Port not free.` make
sure no other application is running on the specified port (8080 is default).

You can change port by changing `server.socket_port` value in
`config/default.cfg`.

If everything is fine, open your favourite web browser and type 
http://localhost:8080, and your can see welcome page with login screen.

Don't forget to enable cookies !

Of course, OpenERP Server must be running at that time. You should create a
database from the DBAdmin interface by clicking on Manage button that you can
see besides the Database selection box. After creating a new database login
with the admin/admin or demo/demo to see the OpenERP in action...

-------------------------------------------------------------------------------
5. Configure HTTPS (Linux)
-------------------------------------------------------------------------------

The following text describes how to configure OpenERP Web for production 
environment over HTTPS with Apache2.

mod_proxy + mod_ssl (Apache2)

    See Apache manual for more information.

Apache configuration:

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

    </VirtualHost>

OpenERP Web configuration:

    base_url_filter.on = True
    base_url_filter.use_x_forwarded_host = False
    base_url_filter.base_url = "https://www.example.com"

Block the OpenERP Web server port (firewall):

On Linux do this:

    $ iptables -A INPUT -i lo -j ACCEPT
    $ iptables -A INPUT -p tcp --dport 8080 -j REJECT

    IMP: Don't block the localhost/121.0.0.1 (the first rule)

Notes:

    This method only works if you want your OpenERP Web application at the 
    root of your server (https://www.example.com). OpenERP Web currently can't 
    be deployed under a subdirectory, e.g. http://www.example.com/openerp.

    To overcome with the issue you can go with `subdomain`, like:

        https://openerp.example.com

    See: http://openerp.org/wiki/index.php/InstallationManual/WebClientHTTPS

-------------------------------------------------------------------------------
6. WEB BROWSER COMPATIBILITIES
-------------------------------------------------------------------------------

`OpenERP Web` is known to work best with `Mozilla` based web browsers.

Here is the list of supported browsers.

    1. Firefox >= 1.5
    2. Internet Explorer >= 6.0
    3. Google Chrome >= 1.0
    4. Safari >= 3.0
    5. Opera >= 9.0

-------------------------------------------------------------------------------
7. SUPPORT
-------------------------------------------------------------------------------

    1. http://openerp.com
    2. http://axelor.com

-------------------------------------------------------------------------------
Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. All Rights Reserved.
