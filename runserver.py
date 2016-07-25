from app import app, db

# db.create_all()

import logging
from logging.handlers import SMTPHandler

ADMINS = ["siddhantloya2008@gmail.com"]

# logger = logging.getLogger("")
# logger.setLevel(logging.DEBUG)

# mail_handler = SMTPHandler(mailhost=('smtp.sendgrid.com',465),
# 							fromaddr='college.connect28@gmail.com',
# 							toaddrs=ADMINS,
# 							subject='logging',
# 							credentials=('collegeconnect','collegeconnect1234'),
# 							)
# mail_handler.setLevel(logging.INFO)
# mail_handler.setFormatter("%(asctime)s %(levelname)-5s %(message)s")

# app.logger.addHandler(mail_handler)

# app.logger.info("sdsgf")

app.run(debug=True)