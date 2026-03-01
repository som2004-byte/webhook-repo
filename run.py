from app import create_app

app = create_app()

if __name__ == '__main__':
    # use_reloader=False avoids WinError 10038 on Windows when using ngrok
    app.run(debug=True, use_reloader=False)
