from app import app

import os

port = int(os.environ.get('PORT', 9080))
app.run(host='127.0.0.1', port=9080, debug=False)