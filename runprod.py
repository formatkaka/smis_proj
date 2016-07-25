from app import app

import logging
from logging.handlers import SMTPHandler

import os

from app import 

ADMINS = ["siddhantloya2008@gmail.com"]

port = int(os.environ.get('PORT', 54658))
app.run(host='0.0.0.0', port=port, debug=False)

##### MAIL HANDLER #####

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)

mail_handler = SMTPHandler(mailhost=('smtp.sendgrid.com',465),
							fromaddr='college.connect28@gmail.com',
							toaddrs=ADMINS,
							subject='logging'
							credentials=('collegeconnect','collegeconnect1234'),
							)
mail_handler.setLevel(logging.INFO)
mail_handler.setFormatter("%(asctime)s %(levelname)-5s %(message)s")

logger.addHandler(mail_handler)

mail_handler.info("sdsgf")