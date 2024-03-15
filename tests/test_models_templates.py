import pytest
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc


from models import db, User, Template

@pytest.fixture
def app_ctx():
    with app.app_context():
        yield

os.environ['DATABASE_URL'] = "postgresql:///shopping-test"        

with app.app_context():
    db.create_all()