from webserver import create_app

if __name__ == '__main__':
    app = create_app()

    app.run(
        '0.0.0.0',
        port = 3210,
        debug = True
    )