import sys
from . import create_app

if __name__ == "__main__":
    debug: bool = False
    if sys.argv.count('--debug') > 0:
        debug = True
        
    app = create_app(debug=debug)
    app.run(use_reloader=False)