===============================================================================
eTiny! - A Web Client for TinyERP
===============================================================================

	1. Introduction
	2. Installation
	3. Support

-------------------------------------------------------------------------------
1. INTRODUCTION
-------------------------------------------------------------------------------

This is a TurboGears (http://www.turbogears.org) project. It can be
started by running the start-tinyerp.py script.

TODO: brief intro

-------------------------------------------------------------------------------
2. INSTALLATION
-------------------------------------------------------------------------------

Prerequisites:
	
	1. Tiny ERP Server (Latest trunk)
	2. TurboGears 1.0.1
	3. matplotlib 0.90
	
Linux Installation (and other similar OSes):

	To install Tiny ERP Server, please follow the instructions provided in the
	official Tiny ERP Installation guide.
	
	To install TurboGears 1.0.1, follow the instructions provided in the 
	official TurboGears installation guilde.
		
	To install matplotlib 0.90, please see INSTALL instructions.
	
	Download the latest eTiny! from the Tiny ERP download area. Extract the
	sources and open `config/app.cfg`, make approperiate changes, especially:
	
		tiny.server = "localhost"
		tiny.port = 8070
		tiny.protocol = "socket"
		
	where:
		
	`tiny.server` is the Tiny ERP server on the specified server.
	`tiny.port` is the port on which Tiny ERP server is running.
	`tiny.protocol` is the protocol to be used (socket, http or https)
	
	there is yet another configuration file available at the top-level directory
	named `dev.cfg`, which defines some development specific configurations.
	
	Please see TurboGears documentation for more information on development and
	production environment configurations.
	
	As this is the first beta of the eTiny!, development configuration is 
	provided by default.
	
	If everything is installed properly, start the eTiny! embeded server by
	running the `start-tinyerp.py` script from the command line, if everything
	is done well you might see some thing similar to:
	
	> cd /path/to/etiny
	> ./start-tinyerp.py
		
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
	a detabase from the DBAdmin interface by clicking on `Manage` button that
	you can see besides the Database selection box. After creating a new database
	login with the `admin/admin or demo/demo` to see the eTiny! in action...
	
MS Windows Installation:

	You should follow the same procedure described above except that you might
	found pre-built binary distributions of Tiny ERP server and MATPLOTLIB 0.90.
		
-------------------------------------------------------------------------------
3. SUPPORT
-------------------------------------------------------------------------------

 TODO: support info

-------------------------------------------------------------------------------
Copyright (c) 2007 TinyERP India Pvt. Ltd.