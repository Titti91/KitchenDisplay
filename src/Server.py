#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from Scraper import Scraper
from Display import Display #einkommentieren befor das auf den pi geschoben wird
from Recipe import Recipe

myScraper = Scraper()
myDisplay = Display()   #einkommentieren befor das auf den pi geschoben wird


class Server(BaseHTTPRequestHandler):
    myRecipe = Recipe()

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        if self.path == "/new/recipe": #/
            jsonData = json.loads(post_data.decode('utf-8').replace("\\", ""))


            global myRecipe  # einkommentieren bevor das auf den pi geschoben wird
            myRecipe = myScraper.scrapeWeb(jsonData["url"])
            self.initializeDisplay()

        if self.path == "/recipe/page":
            jsonData = json.loads(post_data.decode('utf-8').replace("\\", ""))
            print(jsonData["direction"])
            if (jsonData["direction"] == "++"): #check if page should be increased
                if len(myDisplay.descriptionPages.pages) > (myDisplay.currentDescriptionPage + 1):
                    myDisplay.currentDescriptionPage += 1
                    self.updatePage()
            if (jsonData["direction"] == "--"): #check if page should be decreased
                if (myDisplay.currentDescriptionPage - 1) >= 0:
                    myDisplay.currentDescriptionPage -= 1
                    self.updatePage()

        if self.path == "/ingredient/page":
            jsonData = json.loads(post_data.decode('utf-8').replace("\\", ""))
            print(jsonData["direction"])
            if (jsonData["direction"] == "++"):  # check if page should be increased
                if len(myDisplay.ingredientPages.pages) > (myDisplay.currentIngredientPage + 1):
                    myDisplay.currentIngredientPage += 1
                    self.updatePage()
            if (jsonData["direction"] == "--"):  # check if page should be decreased
                if (myDisplay.currentIngredientPage - 1) >= 0:
                    myDisplay.currentIngredientPage -= 1
                    self.updatePage()

        if self.path == "/screensaver":
            myDisplay.drawScreensaver()

        #print(jsonData["url"])

    def updatePage(self):
        # myDisplay.updateDisplay(myRecipe, myDisplay.currentIngredientPage, myDisplay.currentDescriptionPage)
        myDisplay.updateDisplay()
    def initializeDisplay(self):
        #print(self.myRecipe.prettyPrint())
        myDisplay.initDisplay(myRecipe)

def run(server_class=HTTPServer, handler_class=Server, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()