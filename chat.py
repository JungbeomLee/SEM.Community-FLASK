from app import create_app, socket_io

app = create_app(debug=True)

if __name__ == '__main__':
    socket_io.run(app)