from gevent import monkey; monkey.patch_all();
from giga_web import giga_web, socketio
application = giga_web

if __name__ == '__main__':
    port = 5001
    application.run(host='0.0.0.0', port=port, debug=True)

