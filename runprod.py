from app import app

import os

port = int(os.environ.get('PORT', 39918))
app.run(host='0.0.0.0', port=port, debug=False)