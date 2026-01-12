import os
from flask_admin import Admin
from models import db, User, People, Planet, Favorite
from flask_admin.contrib.sqla import ModelView


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class UserView(ModelView):
        column_list = ('id', 'email', 'is_active')

    class PeopleView(ModelView):
        column_list = ('id', 'name', 'gender')

    class PlanetView(ModelView):
        column_list = ('id', 'name', 'climate')

    class FavoriteView(ModelView):
        column_list = ('id', 'user_email', 'planet_id', 'people_id')

    admin.add_view(UserView(User, db.session))
    admin.add_view(PeopleView(People, db.session))
    admin.add_view(PlanetView(Planet, db.session))
    admin.add_view(FavoriteView(Favorite, db.session))
