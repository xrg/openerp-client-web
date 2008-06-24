===============================================================================
eTiny - Web Client of OpenERP, the Enterprise Management Software
===============================================================================

    1. Introduction
    2. Linux Installation
    3. eTiny as service (Linux)
    4. Windows Installation
    5. eTiny + HTTPS
    6. Web browser compatibilities
    7. Support

-------------------------------------------------------------------------------
1. INTRODUCTION
-------------------------------------------------------------------------------

eTiny is the official web client of OpenERP developed by Tiny and Axelor.
It's built on TurboGears (http://www.turbogears.org).

Features:

    - High Performance
    - Light weight
    - Easy deployment
    - Clean & Ergonomic
    - Ajax enabled
    
eTiny is known to work with all major web browsers available today, including
Firefox, IE6, IE7, Safari3 and Opera9.

-------------------------------------------------------------------------------
2. LINUX INSTALLATION
-------------------------------------------------------------------------------

Here is the installation instructions for Debian based Linux distributions.
Tested on Debian Etch and Ubuntu Feisty/Gutsy. The procedure might work with 
other Linux or similar distributions. See the docs on how to install the 
specified Packages on your favourite distro.

Prerequisites:

   1. Python >= 2.4
   2. OpenERP Server >= 4.2.1
   3. TurboGears >= 1.0.3.2
   4. matplotlib >= 0.87
   5. Python Imaging Library (PIL) 

OpenERP Server:

    To install OpenERP Server, please follow the instructions provided in 
    the official OpenERP Installation guide.

TurboGears:

    $ wget http://www.turbogears.org/download/tgsetup.py
    $ python2.4 tgsetup.py
    
or

    $ wget http://peak.telecommunity.com/dist/ez_setup.py
    $ python2.4 ez_setup.py
    $ easy_install-2.4 TurboGears==1.0.3.2

Matplotlib 0.87:

    $ apt-get install python-matplotlib

Python Imaging Library (PIL):

    $ apt-get install python-imaging

eTiny 1.0:

    $ easy_install-2.4 eTiny
    
or 
    
    $ easy_install-2.4 http://openerp.com/download/stable/source/eTiny-1.0.tar.gz

Configuration:

    Locate the `config/default.cfg` in the installed `eTiny EGG`, and make 
    appropriate changes, especially:

    [tinyerp]
    server = "localhost"
    port = 8070
    protocol = "socket"

    where:

    server is the OpenERP server host...
    port is the OpenERP server port...
    protocol is the protocol to be used (socket, http or https)

Now start the eTiny server with `start-tinyerp` command, like:

    $ start-tinyerp

If you see message showing `cherrypy._cperror.NotReady: Port not free.` make
sure no other application is running on the specified port (8080 is default).

You can change port for `eTiny` by changing `server.socket_port` value in
`config/default.cfg`.

If everything is fine, open your favourite web browser and type 
http://localhost:8080, and your can see welcome page with login screen.

Don't forget to enable cookies !

Of course, OpenERP Server must be running at that time. You should create a
database from the DBAdmin interface by clicking on Manage button that you can
see besides the Database selection box. After creating a new database login
with the admin/admin or demo/demo to see the eTiny in action...


-------------------------------------------------------------------------------
3. Run eTiny as service (Linux):
-------------------------------------------------------------------------------

This has been tested on `ubuntu gutsy` only.

    $ cp /path/to/eTiny-1.0-py2.4.egg/scripts/etiny-server /etc/init.d
    $ cp /path/to/eTiny-1.0-py2.4.egg/config/default.cfg /etc/etiny-server.cfg

edit `/etc/init.d/etiny-server`:

    USER="terp"

and `/etc/etiny-server.cfg`:

    args="('server.log',)" ==> args="('/var/log/etiny-server.log',)"

Now run following command to start eTiny automatically on system startup.

    $ sudo update-rc.d etiny-server

Start eTiny deamon:

    $ sudo /etc/init.d/etiny-server start

-------------------------------------------------------------------------------
4. WINDOWS INSTALLATION
-------------------------------------------------------------------------------

Prerequisites

    1. Python >= 2.4
    2. OpenERP Server 4.2.x
    3. TurboGears >= 1.0.3.2
    4. matplotlib >= 0.87
    5. Python Imaging Library (PIL)

Python:

    Download and Install Python 2.4 and make sure that the dirs 
    `C:\Python24;C:\Python24\Script` are in PATH environment.

OpenERP Server:

    To install OpenERP Server, please follow the instructions provided in 
    the official OpenERP Installation guide.

TurboGears:

    Install setuptools package from http://cheeseshop.python.org/packages/2.4/s/setuptools/setuptools-0.6c7.win32-py2.4.exe

    > easy_install TurboGears==1.0.3.2

Matplotlib:

    Download and install matplotlib 0.91 from: http://downloads.sourceforge.net/matplotlib/matplotlib-0.91.0.win32-py2.4.exe

Python Imaging Library (PIL):

    If you have installed TinyERP server on the same machine you already have
    installed Python Imaging Library (PIL). If not do install it from: http://effbot.org/downloads/PIL-1.1.6.win32-py2.4.exe

eTiny:

    > easy_install-2.4 eTiny
    
or

    > easy_install-2.4 http://openerp.com/download/stable/source/eTiny-1.0.tar.gz

Configuration:

    Locate the `config/default.cfg` in the installed `eTiny egg`, and make 
    appropriate changes, especially:

    [tinyerp]
    server = "localhost"
    port = 8070
    protocol = "socket"

    where:

    server is the OpenERP server host...
    port is the OpenERP server port...
    protocol is the protocol to be used (socket, http or https)

Now start the eTiny server with `start-tinyerp` command, like:

    > start-tinyerp

If you see message showing `cherrypy._cperror.NotReady: Port not free.` make
sure no other application is running on the specified port (8080 is default).

You can change port for `eTiny` by changing `server.socket_port` value in
`config/default.cfg`.

If everything is fine, open your favourite web browser and type 
http://localhost:8080, and your can see welcome page with login screen.

Don't forget to enable cookies !

Of course, OpenERP Server must be running at that time. You should create a
database from the DBAdmin interface by clicking on Manage button that you can
see besides the Database selection box. After creating a new database login
with the admin/admin or demo/demo to see the eTiny in action...

-------------------------------------------------------------------------------
5. eTiny + HTTPS (Linux)
-------------------------------------------------------------------------------

The following text describes how to configure eTiny for production environment
over HTTPS with Apache2.

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

eTiny configuration:

    base_url_filter.on = True
    base_url_filter.use_x_forwarded_host = False
    base_url_filter.base_url = "https://www.example.com"

Block the eTiny server port (firewall):

On Linux do this:

    $ iptables -A INPUT -i lo -j ACCEPT
    $ iptables -A INPUT -p tcp --dport 8080 -j REJECT

    IMP: Don't block the localhost/121.0.0.1 (the first rule)

Notes:

    This method only works if you want your eTiny application at the root of 
    your server (https://www.example.com). eTiny currently can't be deployed 
    under a subdirectory, e.g. http://www.example.com/tinyerp.

    To overcome with the issue you can go with `subdomain`, like:

        https://openerp.example.com

    See: http://openerp.org/wiki/index.php/InstallationManual/WebClientHTTPS

-------------------------------------------------------------------------------
6. WEB BROWSER COMPATIBILITIES
-------------------------------------------------------------------------------

`eTiny` is known to work best with `Mozilla` based web browsers.

Here is the list of supported browsers.

    1. Firefox 1.5 or greater
    2. Internet Explorer 6.0/7.0
    3. Opera 9.0
    4. Safari 3.0

-------------------------------------------------------------------------------
7. SUPPORT
-------------------------------------------------------------------------------

    1. http://openerp.com
    2. http://axelor.com

-------------------------------------------------------------------------------
Copyright (C) 2007-TODAY TIny ERP Pvt. Ltd. All Rights Reserved.
