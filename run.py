#!flask/bin/python
import os
from app import application

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.debug = True
    application.run(host='0.0.0.0', port=port)
