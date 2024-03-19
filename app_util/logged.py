from flask import Flask, request, render_template, redirect, flash, session, jsonify
from functools import wraps
from models import db, connect_db, User


def logged_in(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if not session.get('username'):
            flash("Please log in to see the content", "danger")
            return redirect('/')
        user_id = get_user_id(session['username'])
        return func(*args, user_id=user_id, **kwargs)
    return decorator


def get_user_id(username):
    user = User.query.filter(User.username == username).first()
    return user.id
