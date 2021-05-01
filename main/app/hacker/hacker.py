from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = 'localhost'
serverPort = 8080

def cipher_decrypt(ciphertext, key):

    decrypted = ""

    for c in ciphertext:

        if c.isupper(): 
            c_index = ord(c) - ord('A')
            c_og_pos = (c_index - key) % 26 + ord('A')
            c_og = chr(c_og_pos)
            decrypted += c_og

        elif c.islower(): 
            c_index = ord(c) - ord('a') 
            c_og_pos = (c_index - key) % 26 + ord('a')
            c_og = chr(c_og_pos)
            decrypted += c_og
        elif c.isdigit():
            c_og = (int(c) - key) % 10
            decrypted += str(c_og)
        else:
            decrypted += c

    return decrypted

class Server(BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        print(json.loads(post_data))
        json_object = json.loads(post_data)
        decrypted_strings= self.process_json(json.loads(post_data))
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(decrypted_strings).encode('utf-8'))
    
    def process_json(self,json_object):
        
        strart,end = json_object['key_range'].values()
        text = json_object['text']

        encrypted_strings = []
        for i in range(strart,end+1):
            encrypted_strings.append(cipher_decrypt(text,i))

        return encrypted_strings




server_address = ('',serverPort)
httpd = HTTPServer(server_address,Server)
httpd.serve_forever()