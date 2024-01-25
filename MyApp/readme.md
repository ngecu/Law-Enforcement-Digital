Go to Your terminal inside MyApp and create the database

(env) C:\Users\pc\Desktop\Law-Enforcement-Digital\MyApp>

from models import db

with app.app_context():
    db.create_all()

exit()

Then Go back and start the app:-

(env) C:\Users\pc\Desktop\Law-Enforcement-Digital> python -m MyApp.app

