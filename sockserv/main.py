from flask import Flask, request, jsonify
import threading
import SUCC.sockserv as ss
import sys
sys.path.append('..')
from ip import get_ip, FLASK_PORT

addr = get_ip()
print("addr: ", addr)
port = FLASK_PORT

app = Flask(__name__)

@app.route('/getlist', methods=['GET'])
def get_applet_list():
    return jsonify(results=ss.getlist(request.args.get('login')))


@app.route('/sendDataToApplet', methods=['POST'])
def sendToApplet():
    l, p, c, d = request.form['login'], request.form['pass'], request.form['appletid'], request.form['description']
    print ("l = {}, p = {},\n c = {}, d = {}".format(l,p,c,d))
    ss.send_data(c, l, p, d)
    return 'SUCCESS'


if __name__ == '__main__':
    sockser = ss.Initializer()
    t = threading.Thread(target=sockser.run)
    t.start()
    app.run(addr, port=port)