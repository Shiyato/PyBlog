from initialization import login_manager
from db_models import db


@login_manager.user_loader
def load_user(user_id):
    return db.query.get(int(user_id))