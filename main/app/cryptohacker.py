from flask import Flask,request,redirect,url_for
import subprocess
import requests
import threading
import time

app = Flask(__name__)
config={
    "max_key_value" : 10000,
    "key_per_container" :  1000 ,
    "containers_count" : 10
}
process_txt =''
@app.route('/',methods = ['GET','POST'])
def home_page():
    if request.method =='POST':
        process_txt = request.form['crypto_text']
        subprocess.check_output(["docker build -t hacker_container ."], shell=True)
        threads = []
        for i in range(config['containers_count']):
            time.sleep(1)
            thread = threading.Thread(target= lambda : subprocess.check_output([f'docker run -p 808{i}:8080 -d  --name=hacker{i} hacker_container '], shell=True))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        return redirect( url_for('start',text = process_txt))
       
    else:
        header = '<html><head><title> Hacker </title></head><body>'
        body= '''<form method = "POST">
        <input type ="text" name="crypto_text">
        <input type ="submit" value ="submit">
        </form>
        '''
        footer = '</body></html>'
        return header + body+footer

@app.route('/start/<text>')
def start(text):
        threads = []
        lock = threading.Lock()
        results = []
        for i in range(config['containers_count']):
            thread = threading.Thread(target= send_info,args=(i,lock,results,text))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        return str(results)

def send_info(i,lock,results,text):
    key_range = {'start':i * config['key_per_container'],'end': (i+1) * config['key_per_container']}

    data = {'key_range' : key_range,'text': text}
    URL = f'http://localhost:808{i}'
    req = requests.post(url = URL, json= data)
    time.sleep(1)
    subprocess.check_output([f'docker rm -f hacker{i}'], shell=True)

    lock.acquire()
    print(req.json())
    results.append(req.json())
    lock.release()

if __name__ == '__main__':
    app.run(debug=True,host='',port=9090)