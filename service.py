#!/usr/bin/env python3
'''
Networking script.
'''

import http.server
import utils

__author__ = 'Ethan Jensen'
__version__ = '1.01'

class P2Server(http.server.BaseHTTPRequestHandler):
    '''
    Specialized subclass that listens at the HTTP socket,
    dispatching the requests to a handler.
    '''
    def do_GET(self):
        '''
        Overriding do_GET()
        '''
        self.log_message("path: %s", self.path)
        if utils.check_resource(self.path):
            self.log_message("TRUE ! TRUE")
        try:
            path = self.path
            if not utils.check_resource_start(path):
                self.log_message("resource: %s", path)
                self.send_error(404, 'Resource must begin with: /subnet')
            if not utils.check_resource(path):
                self.log_message("resource: %s", path)
                self.send_error(400, 'Resource is in invalid format')

            query = utils.grab_query(path).split('&')

            body = self.process_and_respond(query)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(body, 'UTF-8'))

        except Exception as exception:
            self.send_error(500, str(exception))


    def process_and_respond(self, query):
        '''
        Processes content for valid query.
        Parameters:
        query - the parameters provided to the query
        '''
        body = 'Hello! The subnet is: ' + utils.apply_mask(query[0], query[1])
        html = "<!DOCTYPE html><html>"
        html += "<head><title>"
        html += "Response from L13Server"
        html += "</title></head>"
        html += "<body><p><h1>"
        html += body
        html += "</h1></p></body>"
        html += "</html>"
        self.log_message("page built")
        return html

def start_server():
    PORT = 3280
    server = http.server.HTTPServer(('192.168.1.15', PORT), P2Server)
    print('Project 2 {}; Type <Ctrl-C> to stop server.'.format(PORT))
    server.serve_forever()

if __name__ == '__main__':
    start_server()
