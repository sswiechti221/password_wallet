from . import create_app
from .config import DEBUG

if __name__ == "__main__":
    create_app().run(debug=DEBUG)
    