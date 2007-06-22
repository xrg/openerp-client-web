===============================================================================
eTiny! - A Web Client for TinyERP
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
2. LINUX INSTALLATION (Unices)
-------------------------------------------------------------------------------

Here is the installation instructions for Debain based Linux distributions.
Tested on `Debian Sarge` and `Ubuntu 6.06`.

The procedure might work with other Linux or similar distributions. See the 
docs on how to install the specified `Packages` on your favourite distro.

Prerequisites:

	1. Python 2.4
	2. Tiny ERP Server 4.1.1
	3. TurboGears 1.0.1
	4. matplotlib 0.90
	5. Python Imaging Library

Tiny ERP Server 4.1.1:

	To install Tiny ERP Server, please follow the instructions provided in the
	official Tiny ERP Installation guide.

	http://tinyerp.org/wiki/index.php/InstallationManual/HomePage
	
TurboGears 1.0.1:

	Please don't use `tgsetup.py` as it always installs latest version of the
	TurboGears.

	See `http://docs.turbogears.org/1.0/InstallOldVersions` for more details.

	To install TurboGears 1.0.1, follow the instructions provided here:

	> sudo apt-get install python2.4-setuptools	
	> sudo easy_install-2.4 -f http://www.turbogears.org/download/index.html \
	--script-dir /usr/local/bin TurboGears==1.0.1

	We have noticed that the `setuptools` fails to install some dependencies.
	Those are, `DecoratorTools` and `SQLObject`.
	
	To install them, do this:

	> sudo apt-get install DecoratorTools==1.4
	> sudo apt-get install SQLObject==0.8.4	

Matplotlib 0.90:

	To install matplotlib 0.90, please see INSTALL instructions for more
	details.

	Here are the instructions to compile it on Debain or Ubuntu...
	
	> sudo apt-get install build-essential
	> sudo apt-get install python2.4-dev
	> sudo apt-get install python2.4-numeric
	> sudo apt-get install python2.4-numeric-ext
	> sudo apt-get install libfreetype6-dev
	> sudo apt-get install libpng12-dev
	
	Tiny ERP GTK client requires GTK and CAIRO support, so do this:
	
	> sudo apt-get install python2.4-gtk2 python-gtk2-dev
	> sudo apt-get install python2.4-cairo python-cairo-dev

	This will install all the required packages to build the matplotlib 0.90.

	> cd /path/to/matplotlib-0.90
	> python2.4 setup.py build
	
	This will build the matplotlib, now to install the library do this:
	
	> sudo python2.4 setup.py install

Python Imaging Library (PIL):

	If you have installed TinyERP server on the same machine you already have
	installed Python Imaging Library (PIL). If not do this:
	
	> sudo apt-get install python2.4-imaging

eTiny! 0.0.1:
	
	Download the latest eTiny! from the Tiny ERP download area. Extract the
	sources and open `config/app.cfg`, make appropriate changes, especially:
	
		tiny.server = "localhost"
		tiny.port = 8070
		tiny.protocol = "socket"
		
	where:

	`tiny.server` is the Tiny ERP server host...
	`tiny.port` is the Tiny ERP server port...
	`tiny.protocol` is the protocol to be used (socket, http or https)

	There is yet another configuration file available at the top-level directory
	named `dev.cfg`, which defines some development specific configurations.

	Please see TurboGears documentation for more information on development and
	production environment configurations.
	
	As this is the first beta of the eTiny!, development configuration is 
	provided by default.
	
	If everything is installed properly, start the embedded HTTP server running 
	the `start-tinyerp.py` script from the command line. If everything is done 
	well you might see some thing similar to:

	> cd /path/to/etiny-0.0.1
	> python2.4 ./start-tinyerp.py

	2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG: Server parameters:
	2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG:   server.environment: development
	2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG:   server.log_to_screen: True
	2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG:   server.log_file:
	2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG:   server.log_tracebacks: True
	2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG:   server.log_request_headers: True
	2007-06-11 20:10:34,270 cherrypy.msg INFO CONFIG:   server.protocol_version: HTTP/1.0
	2007-06-11 20:10:34,270 cherrypy.msg INFO CONFIG:   server.socket_host:
	2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG:   server.socket_port: 8080
	2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG:   server.socket_file:
	2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG:   server.reverse_dns: False
	2007-06-11 20:10:34,272 cherrypy.msg INFO CONFIG:   server.socket_queue_size: 5
	2007-06-11 20:10:34,272 cherrypy.msg INFO CONFIG:   server.thread_pool: 10
	2007-06-11 20:10:34,543 cherrypy.msg INFO HTTP: Serving HTTP on http://localhost:8080/
	
	Now open your favourite web browser and type `http://localhost:8080`, and
	your can see welcome page with login screen.

	Of course, Tiny ERP Server must be running at that time. You should create
	a database from the DBAdmin interface by clicking on `Manage` button that
	you can see besides the Database selection box. After creating a new database
	login with the `admin/admin or demo/demo` to see the eTiny! in action...
	
-------------------------------------------------------------------------------
3. WINDOWS INSTALLATION
-------------------------------------------------------------------------------

Prerequisites:

	1. Python 2.4
	2. Tiny ERP Server 4.1.1
	3. TurboGears 1.0.1
	4. matplotlib 0.90

Tiny ERP Server 4.1.1:

	To install Tiny ERP Server, please follow the instructions provided in the
	official Tiny ERP Installation guide.

	http://tinyerp.org/wiki/index.php/InstallationManual/HomePage
	
TurboGears 1.0.1:

	Please don't use `tgsetup.py` as it always installs latest version of the
	TurboGears.
	
	See `http://docs.turbogears.org/1.0/InstallOldVersions` for more details.
	
	To install TurboGears 1.0.1, follow the instructions provided here:
	
	Download and install `setuptools` package for Python2.4 from:

	http://cheeseshop.python.org/packages/2.4/s/setuptools/setuptools-0.6c6.win32-py2.4.exe	
	
	> set PATH=C:\Python24;C:\Python24\Scripts;%PATH%
	> easy_install -f http://www.turbogears.org/download/index.html TurboGears==1.0.1

Matplotlib 0.90:

	Download and install matplotlib 0.90 from:
		
		http://downloads.sourceforge.net/matplotlib/matplotlib-0.90.0.win32-py2.4.exe
		
Python Imaging Library (PIL):

	If you have installed TinyERP server on the same machine you already have
	installed Python Imaging Library (PIL). If not do this:
	
	http://effbot.org/downloads/PIL-1.1.6.win32-py2.4.exe

eTiny! 0.0.1:
	
	Download the latest eTiny! from the Tiny ERP download area. Extract the
	sources and open `config/app.cfg`, make appropriate changes, especially:
	
		tiny.server = "localhost"
		tiny.port = 8070
		tiny.protocol = "socket"
		
	where:
		
	`tiny.server` is the Tiny ERP server host...
	`tiny.port` is the Tiny ERP server port...
	`tiny.protocol` is the protocol to be used (socket, http or https)
	
	There is yet another configuration file available at the top-level directory
	named `dev.cfg`, which defines some development specific configurations.

	Please see TurboGears documentation for more information on development and
	production environment configurations.
	
	As this is the first beta of the eTiny!, development configuration is 
	provided by default.
	
	If everything is installed properly, start the embedded HTTP server running 
	the `start-tinyerp.py` script from the command line. If everything is done 
	well you might see some thing similar to:
		
	> cd \path\to\etiny-0.0.1
	> python start-tinyerp.py

	2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG: Server parameters:
	2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG:   server.environment: development
	2007-06-11 20:10:34,268 cherrypy.msg INFO CONFIG:   server.log_to_screen: True
	2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG:   server.log_file:
	2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG:   server.log_tracebacks: True
	2007-06-11 20:10:34,269 cherrypy.msg INFO CONFIG:   server.log_request_headers: True
	2007-06-11 20:10:34,270 cherrypy.msg INFO CONFIG:   server.protocol_version: HTTP/1.0
	2007-06-11 20:10:34,270 cherrypy.msg INFO CONFIG:   server.socket_host:
	2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG:   server.socket_port: 8080
	2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG:   server.socket_file:
	2007-06-11 20:10:34,271 cherrypy.msg INFO CONFIG:   server.reverse_dns: False
	2007-06-11 20:10:34,272 cherrypy.msg INFO CONFIG:   server.socket_queue_size: 5
	2007-06-11 20:10:34,272 cherrypy.msg INFO CONFIG:   server.thread_pool: 10
	2007-06-11 20:10:34,543 cherrypy.msg INFO HTTP: Serving HTTP on http://localhost:8080/
	
	Now open your favourite web browser and type `http://localhost:8080`, and
	your can see welcome page with login screen.

	Of course, Tiny ERP Server must be running at that time. You should create
	a database from the DBAdmin interface by clicking on `Manage` button that
	you can see besides the Database selection box. After creating a new database
	login with the `admin/admin or demo/demo` to see the eTiny! in action...
	
-------------------------------------------------------------------------------
4. WEB BROWSER COMPATIBILITIES
-------------------------------------------------------------------------------

eTiny! is known to work best with `Mozilla` based web browsers.

Here is the list of supported browsers.

	1. Firefox 1.5 or greater
	2. Internet Explorer 6.0
	3. Opera 9.0
	
Due to a bug in TurboGears, `Safari` browser is not supported currently. MAC
users should use `Mozilla Camino` or `Internet Explorer for MAC`.
	
-------------------------------------------------------------------------------
5. SUPPORT
-------------------------------------------------------------------------------

 TODO: support info

-------------------------------------------------------------------------------
Copyright (c) 2007 TinyERP India Pvt. Ltd.
