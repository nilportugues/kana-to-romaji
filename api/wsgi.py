from app import app


if __name__ == "__main__":
   app.config['DEBUG'] = False
   app.run(host='127.0.0.1', port=5000)

