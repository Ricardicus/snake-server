""" THIS IS THE BACKEND """

import time
import BaseHTTPServer 
import os

HOST_NAME = "" 
PORT_NUMBER = 80

SCORES = []
max_scores = 10

def comp(a,b):
  return b["score"] - a["score"]

def remove_mini():
  mini = 99999999
  for i in SCORES:
    if(i["score"] <= mini):
      mini = i["score"]

  for i in range(len(SCORES)):
    if (SCORES[i]["score"] == mini):
      SCORES.pop(i)
      return

def register(name, score):
  new = {}
  new["name"] = name
  new["score"] = score

  if (len(SCORES) >= max_scores): 
    remove_mini()

  SCORES.append(new)
  SCORES.sort(comp)

def cgi(s, url):

  if "?" not in url:
    s.send_response(200)
    s.send_header("Content-type", "text/html")  
    s.end_headers()
    s.wfile.write("? not in url!")
    return

  action = url.split("action=")[1].split("&")[0]

  if(action == "get_highscore"):
    s.send_response(200)
    s.send_header("Content-type", "text/html")  
    s.end_headers()

    s.wfile.write("<thead><tr><th></th><th><p>Name</p></th><th><p>Score</p></th></tr></thead>")
    s.wfile.write("<tbody>")
    if(len(SCORES) < 1):
      s.wfile.write("<td>No</td><td>results</td><td>yet ...</td>")
      return
    for i in range(len(SCORES)):
      s.wfile.write("<tr><td>" + str(i+1) + ":</td><td>" + SCORES[i]["name"] + "</td><td>" + str(SCORES[i]["score"]) + "</td></tr>")
    s.wfile.write("</tbody>")
  elif(action == "post_score"):
    register(url.split("name=")[1].split("&")[0], int(url.split("score=")[1].split("&")[0]))
    s.send_response(200)
    s.send_header("Content-type", "text/html")  
    s.end_headers()
    s.wfile.write("Good!")



class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
  def do_GET(s):
    # If someone went to "http://something.somewhere.net/foo/bar/",
    # then s.path equals "/foo/bar/".
    if(s.path == "/"):
      s.send_response(200)
      s.send_header("Content-type", "text/html")  
      s.end_headers()
      f = open("index.html", "r")
      s.wfile.write(f.read())
      f.close()       
    elif(os.path.isfile(s.path[1:])):
      s.send_response(200)
      if(s.path.endswith(".js")): 
        s.send_header("Content-type", "text/javascript")
      elif(s.path.endswith(".css")):
        s.send_header("Content-type", "text/css")  
      elif(s.path.endswith(".gif")):
        s.send_header("Content-type", "image/gif")
        s.send_header("Content-description", "File Transfer");
        s.send_header("Content-transfer-encoding", "binary")
      s.end_headers()
      f = open(s.path[1:], "r")
      s.wfile.write(f.read())
      f.close() 
    elif ".cgi" in s.path:
      cgi(s, s.path[1:])
    else:
      print s.path[1:]
      s.wfile.write("<html><head><title>Get page</title></head>")
      s.wfile.write("<body><p>This is a test.</p>")
      s.wfile.write("<p>You accessed path: %s, from your ip: %s</p>" % (s.path , ".".join(s.address_string().split(".")[::-1][2:])))
      s.wfile.write("</body></html>") 

if __name__ == '__main__':
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)