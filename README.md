# TekMonks-Project-Assessment

## Problem Statement:

To use any programming language to create an application that extracts the latest 6 stories from Time.com's homepage. To do this, you will need to process the HTML of the homepage using a basic approach. This means that you should not use any internal or external libraries or packages to process the text. The application should return the title, publication date, and link to each story. You can call this application as a custom API. The Source URL is https://time.com .

## Approach/Methodology:

1. Importing Required Modules:
   - The code begins by importing necessary Python modules:
   - http.client: Used for making HTTP requests to a website (in this case, Time.com).
   - json: Used for handling JSON data.
   - re: Used for regular expressions to parse HTML content.
   - http.server: Provides classes for implementing an HTTP server.
   - BaseHTTPRequestHandler: A base class for creating custom HTTP request handlers.
```python
import http.client
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
```     

2. Defining a Custom Request Handler Class MyHandler:
   - This custom request handler class inherits from BaseHTTPRequestHandler and is used to define how the HTTP server responds to incoming requests.
```python
class MyHandler(BaseHTTPRequestHandler):
```

3. Handling HTTP GET Requests (do_GET method):
   - This method is called whenever an HTTP GET request is made to the server.
```python
def do_GET(self):
```

4. Making an HTTPS Request to Time.com:
   - An HTTPS connection is established to the "time.com" website, and a GET request is sent to retrieve the homepage.
```python
conn = http.client.HTTPSConnection("time.com")
conn.request("GET", "/")
res = conn.getresponse()
```

5. Checking the Response Status:
   - The code checks if the response status from Time.com is 200 (OK), indicating a successful request.
```python
if res.status == 200:
```
     
6. Extracting Story Data from HTML Content:
   - The HTML content of the Time.com homepage is fetched and parsed using regular expressions to extract story titles and links.
   - The extracted data is stored in the stories list as dictionaries.
```python
html_content = res.read().decode('utf-8')
stories = []

story_pattern = re.compile(r'<a href="(.*?)">.*?<h3 class="latest-stories__item-headline">(.*?)</h3>', re.DOTALL)
matches = re.findall(story_pattern, html_content)

for link, title in matches:
    stories.append({
        "title": title.strip(),
        "link": "https://time.com" + link
    })
```
  
7. Saving JSON Data to a File:
   - The extracted story data is saved as JSON to a file named "Recent.json" with proper indentation and encoding.
```python
with open('Recent.json', 'w', encoding='utf-8') as json_file:
    json.dump(stories, json_file, indent=6, ensure_ascii=False)
```
  
8. Creating an HTML Page with Styling:
   - An HTML template is defined with CSS styling to create a visually appealing webpage.
```python
html_output = """
<!DOCTYPE html>
<html>
<head>
    <!-- ... HTML and CSS styling ... -->
</head>
<body>
    <!-- ... HTML content ... -->
</body>
</html>
"""
```
  
9. Adding Story Data to the HTML Page:
    - The extracted story data is added to the HTML page within an unordered list [ul] as list items [li] with hyperlinks to the story links.
```python
for story in stories:
    html_output += f'<li><a href="{story["link"]}" target="_blank">{story["title"]}</a></li>'
```  
10. Sending the HTML Response:
    - The HTTP response status is set to 200 (OK), and the HTML content is sent as the response to the client's browser.
    - CORS headers are included to allow cross-origin requests.
```python
self.send_response(200)
self.send_header('Content-type', 'text/html')
self.send_header('Access-Control-Allow-Origin', '*')
self.end_headers()
self.wfile.write(html_output.encode('utf-8'))
```
   
11. Handling Errors:
    - If any exceptions occur during the process (e.g., network issues or parsing errors), the server responds with a 500 (Internal Server Error) status and an error message in JSON format.
```python
except Exception as e:
    self.send_response(500)
    self.end_headers()
    self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
```
   
12. Main Section and Server Initialization:
    - The code block for starting the HTTP server is wrapped in if __name__ == '__main__': to ensure that it runs only when the script is executed directly (not when imported as a module).
    - An HTTP server is created to listen on localhost at port 8080 using the custom request handler class MyHandler. The server is then started and runs indefinitely, waiting for incoming HTTP requests.
```python
if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), MyHandler)
    print('Starting server on port 8080...')
    server.serve_forever()
```

   
This Project combines web scraping, JSON data processing, and HTTP server handling/API call to create a webpage that displays the latest stories from Time.com in a visually appealing format. We can access this webpage by navigating to http://127.0.0.1:8080/ in our web browsers. 

## Output:

JSON FILE

![image](https://github.com/Jayashreerao15/TekMonks-Problem-Assessment/assets/74660507/3298ea8d-50cf-4315-b9a9-aedc30b0c7aa)


WEBPAGE

![image](https://github.com/Jayashreerao15/TekMonks-Problem-Assessment/assets/74660507/8c873ce9-6e7e-40b8-ac4b-33d68eb71cc8)

JSON FILE CREATION + WEBPAGE 

![image](https://github.com/Jayashreerao15/TekMonks-Problem-Assessment/assets/74660507/b440f307-0f93-4f6d-890c-85eb51db1190)




