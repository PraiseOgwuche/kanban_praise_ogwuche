#/usr/bin/env python

"""A simple Kanban board application using Flask and SQLLite"""

from flask import Flask, send_from_directory, request, abort, redirect, url_for, render_template
from flask.json import jsonify
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from database import db
import cards

login_manager = LoginManager()

def setup_app(kanban_db):
    """Create a new instance of the flask app"""
    kanban_app = Flask(__name__)
    #bcrypt = Bcrypt(kanban_app)
    kanban_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
    kanban_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    kanban_app.config['SECRET_KEY'] = 'secret'
    kanban_app.config['kanban.columns'] = ['To Do', 'Doing', 'Done']
    kanban_db.init_app(kanban_app)
    kanban_app.app_context().push()
 
    login_manager.login_view = 'login'
    login_manager.init_app(kanban_app)
    kanban_db.create_all()
    return kanban_app
bcrypt = Bcrypt(setup_app(kanban_db=db))
app = setup_app(db) # pylint: disable=invalid-name

@login_manager.user_loader
def load_user(user_id):
    return cards.User.query.get(int(user_id))

@app.route('/')
def index():
    """Serve the main index page"""
    return send_from_directory('templates', 'index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = cards.LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    if user := cards.User.query.filter_by(
        username=form.username.data
    ).first():
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return send_from_directory('templates','login.html')


# @app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     return send_from_directory('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = cards.RegisterForm()

    if not form.validate_on_submit():
        return render_template('register.html', form=form)

    hashed_password = bcrypt.generate_password_hash(form.password.data)
    new_user = cards.User(username=form.username.data, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/templates/<path:path>')
def templates_file(path):
    """Serve files from the templates directory"""
    return send_from_directory('templates', path)

@app.route('/cards')
def get_cards():
    """Get an order list of cards"""
    return jsonify(cards.all_cards())

@app.route('/columns')
def get_columns():
    """Get all valid columns"""
    return jsonify(app.config.get('kanban.columns'))

@app.route('/card', methods=['POST'])
def create_card():
    """Create a new card"""

    # TODO: validation
    cards.create_card(
        text=request.form.get('text'),
        column=request.form.get('column', app.config.get('kanban.columns')[0]),
        color=request.form.get('color', None),
    )

    # TODO: handle errors
    return 'Success'

@app.route('/card/reorder', methods=["POST"])
def order_cards():
    """Reorder cards by moving a single card

    The JSON payload should have a 'card' and 'before' attributes where card is
    the card ID to move and before is the card id it should be moved in front
    of. For example:

      {
        "card": 3,
        "before": 5,
      }

    "before" may also be "all" or null to move the card to the beginning or end
    of the list.
    """

    if not request.is_json:
        abort(400)
    cards.order_cards(request.get_json())
    return 'Success'


@app.route('/card/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    """Update an existing card, the JSON payload may be partial"""
    if not request.is_json:
        abort(400)

    # TODO: handle errors
    cards.update_card(card_id, request.get_json(), app.config.get('kanban.columns'))

    return 'Success'

@app.route('/card/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    """Delete a card by ID"""

    # TODO: handle errors
    cards.delete_card(card_id)
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)
