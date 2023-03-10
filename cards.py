
"""Card model and controller"""
from flask import Flask, send_from_directory, request, abort, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone
from database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        if existing_user_username := User.query.filter_by(
            username=username.data
        ).first():
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class Card(db.Model): # pylint: disable=too-few-public-methods
    """SQLAlchemy card class"""
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=C0103
    text = db.Column(db.String(120))
    column = db.Column(db.String(120), default="To Do")
    color = db.Column(db.String(7), default='#dddddd')
    modified = db.Column(db.DateTime, default=datetime.utcnow)
    archived = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        """Return a string representation of a card"""
        return '<Card (%d): %s>' % (self.id, self.text)

    def json(self):
        """Return a JSON representation of a card"""
        return {
            'id': self.id,
            'text': self.text,
            'column': self.column,
            'color': self.color,
            'modified': self.modified.replace(tzinfo=timezone.utc).isoformat(),
            'archived': self.archived,
        }

def all_cards():
    """Return JSON for all cards, sorted by the order_by attribute"""
    return [card.json() for card in Card.query.order_by(Card.sort_order.asc()).all()]

def create_card(text, **kwargs):
    """Create a new card"""
    # TODO: handle missing values
    db.session.add(Card(text=text, **kwargs))
    db.session.commit()

def delete_card(card_id):
    """Delete a card"""
    # TODO: handle missing values
    db.session.delete(Card.query.get(card_id))
    db.session.commit()

def order_cards(data):
    """Reposition a specified card"""

    # TODO: handle missing 'card' property
    card_id = data['card']
    before_id = data.get('before', 'all')

    cards = Card.query.order_by(Card.sort_order.asc()).all()

    card = next(card for card in cards if card.id == card_id)

    if before_id is None:
        # move to end
        cards.append(cards.pop(cards.index(card)))
    elif before_id == 'all':
        # move to start
        cards.insert(0, cards.pop(cards.index(card)))
    else:
        before_card = next(card for card in cards if card.id == before_id)
        moving_card = cards.pop(cards.index(card))
        new_index = cards.index(before_card)
        cards.insert(new_index, moving_card)

    for i, card in enumerate(cards):
        card.sort_order = i #len(cards) - i

    db.session.commit()

def update_card(card_id, json, columns):
    """Update an existing card"""
    card = Card.query.get(card_id)

    modified = False

    if 'text' in json:
        modified = True
        card.text = json['text']

    if 'color' in json:
        modified = True
        card.color = json['color']

    if 'column' in json:
        if json['column'] in columns:
            modified = True
            card.column = json['column']
        else:
            raise Exception("Invalid column name: %s" % json['column'])

    if 'archived' in json:
        modified = True
        card.archived = json['archived']

    if modified:
        card.modified = datetime.utcnow()

    db.session.commit()
