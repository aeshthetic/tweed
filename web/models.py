import datetime
import functools
from app import db

db.Column = functools.partial(db.Column, nullable=False)

