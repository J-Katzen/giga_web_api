from giga_web import giga_web

if __name__ == '__main__':
    # Heroku support: bind to PORT if defined, otherwise default to 5000.
    port = 5001

    giga_web.run(host='0.0.0.0', port=port)
