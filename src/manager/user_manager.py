from ..models import User, db
import flask_login, flask

class UserManager:
    def __init__(self, app: flask.Flask) -> None:
        login_manager = flask_login.LoginManager()
        login_manager.init_app(app)

        @login_manager.user_loader
        def user_loader(user_id):
            return User.query.filter_by(id=user_id).first()

        @login_manager.request_loader
        def request_loader(request):
            username = request.form.get("username")
            user = User.query.filter_by(username=username).first()
            return user

        @login_manager.unauthorized_handler
        def unauthorized_handler():
            return "Unauthorized", 401
        
        # app.before_request
        
        @app.before_request
        def create_tables():
            db.create_all()
        pass