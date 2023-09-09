import http.client
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            conn = http.client.HTTPSConnection("time.com")
            conn.request("GET", "/")
            res = conn.getresponse()

            if res.status == 200:
                html_content = res.read().decode('utf-8')
                stories = []

                story_pattern = re.compile(r'<a href="(.*?)">.*?<h3 class="latest-stories__item-headline">(.*?)</h3>', re.DOTALL)
                matches = re.findall(story_pattern, html_content)

                for link, title in matches:
                    stories.append({
                        "title": title.strip(),
                        "link": "https://time.com" + link
                    })

                html_output = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Breaking Stories from Time.com</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                        }
                        header {
                            background-color: #333;
                            color: #fff;
                            text-align: center;
                            padding: 20px 0;
                        }
                        h1 {
                            font-size: 24px;
                        }
                        .container {
                            max-width: 800px;
                            margin: 20px auto;
                            background-color: rgba(255, 255, 255, 0.8); 
                            box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
                            border-radius: 4px;
                        }
                        ul {
                            list-style-type: none;
                            padding: 0;
                            margin: 0;
                        }
                        li {
                            border-bottom: 1px solid #ddd;
                            padding: 15px;
                        }
                        a {
                            color: #FF0000;
                            text-decoration: none;
                        }
                        a:hover {
                            text-decoration: underline;
                        }
                    </style>
                </head>
                <body>
                    <header>
                        <h1>Breaking Stories from Time.com</h1>
                    </header>
                    <div class="container">
                        <ul>
                """

                for story in stories:
                    html_output += f'<li><a href="{story["link"]}" target="_blank">{story["title"]}</a></li>'

                html_output += """
                        </ul>
                    </div>
                </body>
                </html>
                """

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(html_output.encode('utf-8'))
            else:
                self.send_response(res.status)
                self.end_headers()
                self.wfile.write(b'Error')

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), MyHandler)
    print('Starting server on port 8080...')
    server.serve_forever()
