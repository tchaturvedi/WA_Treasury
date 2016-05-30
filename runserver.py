from app import App

if __name__ == '__main__':
    App.debug = True
    App().app.run(debug=True)