# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the License for the specific language governing permissions and
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

import webapp2
import cgi

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
def valid_month(month):
    if month:
        if month.title() in months: return month.title()
        
    return None

def valid_day(day):
    if not day.isdigit(): return None
    if (int(day)<1) or (int(day)>31): return None
    return int(day)

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if (year >= 1900) and (year <= 2020): return year
        return None

def escape_html(s):
    return cgi.escape(s, quote=True)

form="""
    <form method="post">
        What is your birthday?
        <br>
        <label> Month
            <input type="text" name="month" value="%(month)s">
        </label>
        <label> Day
            <input type="text" name="day" value="%(day)s">
        </label>
        <label> Year
            <input type="text" name="year" value="%(year)s">
        </label>
        <div style="color: red">%(error)s</div>
        <br><br>
        <input type="submit">
    </form>
"""



class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "day": escape_html(day),
                                        "year": escape_html(year),
                                        "month": escape_html(month)})

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

    def post(self):
        #self.response.out.write(self.request)
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        print user_day
        print day
        print user_month
        print month
        print user_year
        print year

        if not (month and day and year):
            self.write_form("that doesnt look valid", user_month,
                                                      user_day,
                                                      user_year)
        else: 
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks!")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)
], debug=True)
