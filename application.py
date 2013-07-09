from giga_web import giga_web

application = giga_web

if __name__ == '__main__':
    port = 5001

    application.run(host='0.0.0.0', port=port, debug=True)
