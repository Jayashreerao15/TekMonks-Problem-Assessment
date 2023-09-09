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

                with open('Recent.json', 'w', encoding='utf-8') as json_file:
                    json.dump(stories, json_file, indent=6, ensure_ascii=False)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                json_output = json.dumps(stories, indent=6, ensure_ascii=False)
                self.wfile.write(json_output.encode('utf-8'))
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
