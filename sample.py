# Author: Chris Oliver
# Email: excid3@gmail.com
# Website: http://excid3.betaserver.org

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class MyData(db.Model):
    """ Database """
    author = db.UserProperty()                    # Username

    # Actual Data
    name = db.StringProperty()                    # Name string
    number = db.StringProperty()                  # Number string
    color = db.StringProperty()                   # Color string

    date = db.DateTimeProperty(auto_now_add=True) # Used for sorting

class MainPage(webapp.RequestHandler):
    """ Handles / """
    def get(self):
        self.response.out.write('<html><body>')

        # Write the submission form and the footer of the page
        self.response.out.write("""
              <form action="/post" method="post">
                <div>Name: <input type="text" name="Name"></div>
                <div>Favorite Number: <input type="text" name="Number" size="8"></div>
                <div>Favorite Color:     
                  <select name="Color">
                       <option value="Red">Red</option>
                       <option value="Blue">Blue</option>
                       <option value="Yellow">Yellow</option>
                     </select>
                </div>
                <div><input type="submit" value="Submit"></div>
              </form>
              <form action="/results" method="get">
                <input type="submit" value="View Results">
              </form>
            </body>
          </html>""")

class Post(webapp.RequestHandler):
    """ Handles /post """
    def post(self):
        """ Save the data and clear forms """
        data = MyData()

        data.name = self.request.get('Name')
        data.put()

        data.number = self.request.get('Number')
        data.put()
    
        data.color = self.request.get('Color')
        data.put()
    
        #TODO: Clear forms
        self.redirect('/')
        
class Results(webapp.RequestHandler):
    """ Handles /results """
    def get(self):
        """ Writes database entries to a table """
        self.response.out.write("""<html><body>
                                     <table border="1">
                                       <tr>
                                         <th>Name</th>
                                         <th>Number</th>
                                         <th>Color</th>
                                       </tr>""")

        data = db.GqlQuery('SELECT * FROM MyData ORDER BY date DESC')

        for item in data: # For each entry in the database, add a table entry
          self.response.out.write('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (item.name, item.number, item.color))

        self.response.out.write('<html><body>')
        
# Initialize application
application = webapp.WSGIApplication([('/', MainPage), 
                                      ('/post', Post),
                                      ('/results', Results)],
                                      debug=True)

def main():
    """ Runs the application """
    run_wsgi_app(application)

if __name__ == "__main__":
    """ Entry point """
    main()
