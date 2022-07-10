from flask_frozen import Freezer
from run import app

freezer = Freezer(app)

# this code is pretty much all from https://pythonhosted.org/Frozen-Flask/
# with line 2 edited
if __name__ == '__main__':
    freezer.freeze()
