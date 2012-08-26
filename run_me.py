import tornado.ioloop
import tornado.web
import tornado.websocket as websocket
import tornado.template as template
import json

browser_sockets = []
phone_sockets	= []
pictures_array	= []

def push_to_browsers(message):
	for socket_obj in browser_sockets:
		socket_obj.write_message(message)

class phoneWebSocket(websocket.WebSocketHandler):
    def open(self):
    	phone_sockets.append(self)

    def on_message(self, message):
    	##pictures_array.append(message)
    	push_to_browsers(message)
	
	def on_close(self):
		if self in phone_sockets: phone_sockets.remove(self)
	

class browserWebSocket(websocket.WebSocketHandler):
    def open(self):
    	browser_sockets.append(self)

    def on_message(self, message):
    	##pictures_array.append(message)
	
	def on_close(self):
		if self in browser_sockets: browser_sockets.remove(self)	
	
	
	
	
class phoneHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("phone.htm")

class browserHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("browser.htm")

application = tornado.web.Application([
    (r"/phone_socket", 		phoneWebSocket),
    (r"/browser_socket", 	browserWebSocket),
    (r"/phone", 			phoneHandler),
    (r"/browser", 			browserHandler),
])

if __name__ == "__main__":
    application.listen(8889)
    application.debug = True
    tornado.ioloop.IOLoop.instance().start()
    

