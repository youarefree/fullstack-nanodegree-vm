from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Restaurant, Base, MenuItem
import cgi


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        try:
            if self.path.endswith("/delete"):
                restaurantPathId = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantPathId).one()
                print restaurantQuery.name
                if restaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += '<html><body>'
                    output += '<h1>'
                    output += restaurantQuery.name + ' ' + str(restaurantQuery.id)
                    output += '</h1>'
                    output += '''<form method='POST' enctype='multipart/form-data' 
                    action='/restaurants/%s/delete'><h2>Are you sure you want to delete restaurant:</h2><input type="submit" value="Submit"> </form>
                    ''' % restaurantQuery.id
                    output += '</body></html>'
                    print output
                    self.wfile.write(output)

            if self.path.endswith("/edit"):
                restaurantPathId = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantPathId).one()
                print restaurantQuery.name
                if restaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += '<html><body>'
                    output += '<h1>'
                    output += restaurantQuery.name + ' ' + str(restaurantQuery.id)
                    output += '</h1>'
                    output += '''<form method='POST' enctype='multipart/form-data' 
                    action='/restaurants/%s/edit'><h2>New RestaurantName:</h2><input name="newRestaurantName" 
                    type="text" ><input type="submit" value="Submit"> </form>
                    ''' % restaurantQuery.id 
                    output += '</body></html>'
                    print output
                    self.wfile.write(output)

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<a href="restaurants/new">New restaurant</a>'''
                for restaurant in restaurants:
                    output += '''</br>%s''' % restaurant.name
                    output += '''</br><a href="/restaurants/%s/edit">Edit</a>''' % str(restaurant.id)
                    output += '''</br><a href="/restaurants/%s/delete">Delete</a></br>''' % str(restaurant.id)
                    
                
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h2> lyurtov e lud </h2>"
                output += "<h1> blabla </h1>"
                output += '''
                <form method='POST' enctype='multipart/form-data' 
                action='/restaurants/new'><h2>Restaurant name:</h2><input name="restaurantName" 
                type="text" ><input type="submit" value="Submit"> </form>
                '''
                output += '''
                <input type="submit" value="Go to my link location" 
                onclick="window.location=/restaurants>'''
                output += "</body></html>"
                self.wfile.write(output)

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            print self.path
            print 2
            engine = create_engine('sqlite:///restaurantmenu.db')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            session = DBSession()
            if self.path.endswith("/restaurants/new"):
            
                #if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('restaurantName')
                    print(restaurantName[0])
                restaurant1 = Restaurant(name=restaurantName[0])
                session.add(restaurant1)
                session.commit()
                print(restaurant1)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                restaurantPathId = self.path.split('/')[2]
                print 4
                print restaurantPathId
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantPathId).one()
                print restaurantQuery
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('newRestaurantName')
                    print(restaurantName[0])
                restaurantQuery.name = restaurantName[0]
                session.add(restaurantQuery)
                session.commit()
                print(restaurantQuery)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/delete"):
                restaurantPathId = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantPathId).one()
                session.delete(restaurantQuery)
                session.commit()
                print(restaurantQuery)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()    
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()