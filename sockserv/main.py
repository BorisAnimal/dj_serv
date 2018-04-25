from flask import Flask, request, jsonify
import threading
import SUCC.sockserv as ss

app = Flask(__name__)

addr = '10.240.22.236'

@app.route('/getlist', methods=['GET'])
def getl():
    return jsonify(results=ss.getlist(request.args.get('login')))


@app.route('/sendDataToApplet', methods=['POST'])
def shd1():
    l, p, c = request.form['login'], request.form['pass'], request.form['appletid']
    print ("l = {}, p = {}, c ={}".format(l,p,c))
    ss.send_data(c, l, p)
    return 'Rekt'


if __name__ == '__main__':
    sockser = ss.Initializer()
    t = threading.Thread(target=sockser.run)
    t.start()
    app.run(addr)
