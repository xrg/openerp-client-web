===============================================================================
eTiny! - The official Web Client for Tiny ERP
===============================================================================

    1. Introduction
    2. Linux Installation
    3. Windows Installation
    4. Web browser compatibilities
    5. Support

-------------------------------------------------------------------------------
1. INTRODUCTION
-------------------------------------------------------------------------------

This is a TurboGears (http://www.turbogears.org) project. It can be
started by running the start-tinyerp.py script.

TODO: introduction

-------------------------------------------------------------------------------
2. LINUX INSTALLATION
-------------------------------------------------------------------------------

Here is the installation instructions for Debain based Linux distributions.
Tested on Debian Etch and Ubuntu Fiesty. The procedure might work with other 
Linux or similar distributions. See the docs on how to install the specified 
Packages on your favourite distro.

Prerequisites:

   1. Python >= 2.4
   2. Tiny ERP Server 4.2.x
   3. TurboGears >= 1.0.3.2
   4. matplotlib >= 0.87
   5. Python Imaging Library (PIL) 

Tiny ERP Server:

    To install Tiny ERP Server, please follow the instructions provided in 
    the official Tiny ERP Installation guide.

TurboGears:

    > wget http://peak.telecommunity.com/dist/ez_setup.py
    > python2.4 ez_setup.py
    > easy_install-2.4 TurgoGears==1.0.3.2

Matplotlib 0.87:

    > apt-get install python-matplotlib

Python Imaging Library (PIL):

    > apt-get install python-imaging

eTiny! (latest):

    > easy_install-2.4 eTiny

Configuration:

    Locate the `config/app.cfg` in the installed `eTiny! egg`, and make 
    appropriate changes, especially:

    tiny.server = "localhost"
    tiny.port = 8070
    tiny.protocol = "socket"

    where:

    tiny.server is the Tiny ERP server host...
    tiny.port is the Tiny ERP server port...
    tiny.protocol is the protocol to be used (socket, http or https)

If everything is installed properly, start the eTiny! HTTP server running 
the `start-tinyerp.py` script from the command line. 

If everything is done well you might see some thing similar to:

> start-tinyerp.py

2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG: Server parameters:
2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG: server.environment: development
2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG: server.log_to_screen: True
2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG: server.log_file:
2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG: server.log_tracebacks: True
2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG: server.log_request_headers: True
2007-06-11 20:10:34,270 cherrypy.msg INFO CONFIG: server.protocol_version: HTTP/1.0
2007-06-11 20:10:34,270 cherrypy.msg INFO CONFIG: server.socket_host:
2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG: server.socket_port: 8080
2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG: server.socket_file:
2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG: server.reverse_dns: False
2007-06-11 20:10:34,272 cherrypy.msg INFO CONFIG: server.socket_queue_size: 5
2007-06-11 20:10:34,272 cherrypy.msg INFO CONFIG: server.thread_pool: 10
2007-06-11 20:10:34,543 cherrypy.msg INFO HTTP: Serving HTTP on http://localhost:8080/

Now open your favourite web browser and type http://localhost:8080, and your
can see welcome page with login screen.

Don't forget to enable cookies !

Of course, Tiny ERP Server must be running at that time. You should create a
database from the DBAdmin interface by clicking on Manage button that you can
see besides the Database selection box. After creating a new database login
with the admin/admin or demo/demo to see the eTiny! in action...

-------------------------------------------------------------------------------
3. WINDOWS INSTALLATION
-------------------------------------------------------------------------------

Prerequisites

   1. Python >= 2.4
   2. Tiny ERP Server 4.2.x
   3. TurboGears >= 1.0.3.2
   4. matplotlib >= 0.87
   5. Python Imaging Library (PIL)

Python:

    Download and Install Python 2.4 and make sure that the dirs 
    `C:\Python24;C:\Python24\Script` are in PATH environment.

Tiny ERP Server:

    To install Tiny ERP Server, please follow the instructions provided in 
    the official Tiny ERP Installation guide.

TurboGears:

    Install setuptools package from http://cheeseshop.python.org/packages/2.4/s/setuptools/setuptools-0.6c6.win32-py2.4.exe

    > easy_install TurboGears==1.0.3.2

Matplotlib:

    Download and install matplotlib 0.91 from: http://downloads.sourceforge.net/matplotlib/matplotlib-0.91.0.win32-py2.4.exe

Python Imaging Library (PIL):

    If you have installed TinyERP server on the same machine you already have
    installed Python Imaging Library (PIL). If not do install it from: http://effbot.org/downloads/PIL-1.1.6.win32-py2.4.exe

eTiny!:

    > easy_install-2.4 eTiny

Configuration:

    Locate the `config/app.cfg` in the installed `eTiny! egg`, and make 
    appropriate changes, especially:

    tiny.server = "localhost"
    tiny.port = 8070
    tiny.protocol = "socket"

    where:

    tiny.server is the Tiny ERP server host...
    tiny.port is the Tiny ERP server port...
    tiny.protocol is the protocol to be used (socket, http or https)

If everything is installed properly, start the eTiny! HTTP server running 
the `start-tinyerp.py` script from the command line. 

If everything is done well you might see some thing similar to:

> start-tinyerp.py

2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG: Server parameters:
2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG: server.environment: development
2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG: server.log_to_screen: True
2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG: server.log_file:
2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG: server.log_tracebacks: True
2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG: server.log_request_headers: True
2007-06-11 20:10:34,270 cherrypy.msg INFO CONFIG: server.protocol_version: HTTP/1.0
2007-06-11 20:10:34,270 cherrypy.msg INFO CONFIG: server.socket_host:
2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG: server.socket_port: 8080
2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG: server.socket_file:
2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG: server.reverse_dns: False
2007-06-11 20:10:34,272 cherrypy.msg INFO CONFIG: server.socket_queue_size: 5
2007-06-11 20:10:34,272 cherrypy.msg INFO CONFIG: server.thread_pool: 10
2007-06-11 20:10:34,543 cherrypy.msg INFO HTTP: Serving HTTP on http://localhost:8080/

Now open your favourite web browser and type http://localhost:8080, and your can see welcome 
page with login screen.

Don't forget to enable cookies !

Of course, Tiny ERP Server must be running at that time. You should create a
database from the DBAdmin interface by clicking on Manage button that you can
see besides the Database selection box. After creating a new database login
with the admin/admin or demo/demo to see the eTiny! in action...

-------------------------------------------------------------------------------
4. WEB BROWSER COMPATIBILITIES
-------------------------------------------------------------------------------

eTiny! is known to work best with `Mozilla` based web browsers.

Here is the list of supported browsers.

    1. Firefox 1.5 or greater
    2. Internet Explorer 6.0/7.0
    3. Opera 9.0
    4. Safari 3.0
	
-------------------------------------------------------------------------------
5. SUPPORT
-------------------------------------------------------------------------------

 TODO: support info

-------------------------------------------------------------------------------
Copyright (c) 2007 Tiny ERP India Pvt. Ltd.
