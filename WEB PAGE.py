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

                # Using regular expressions to extract story titles and links
                story_pattern = re.compile(r'<a href="(.*?)">.*?<h3 class="latest-stories__item-headline">(.*?)</h3>', re.DOTALL)
                matches = re.findall(story_pattern, html_content)

                for link, title in matches:
                    stories.append({
                        "title": title.strip(),
                        "link": "https://time.com" + link
                    })

                # Convert the list of stories to HTML with clickable links
                html_output = """
                    <html>
                    <head>
                        <title>Latest News from Time.com</title>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                margin: 20px;
                            }
                            h1 {
                                color: #333;
                                text-align: center;
                            }
                            ul {
                                list-style-type: none;
                                padding: 0;
                            }
                            li {
                                margin-bottom: 10px;
                            }
                            a {
                                color: #0073e6;
                                text-decoration: none;
                            }
                            a:hover {
                                text-decoration: underline;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Latest News from Time.com</h1>
                        <ul>
                """
                for story in stories:
                    html_output += f'<li><a href="{story["link"]}" target="_blank">{story["title"]}</a></li>'
                html_output += """
                        </ul>
                    </body>
                    </html>
                """

                # Send HTML response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                # Add CORS headers to allow cross-origin requests
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
