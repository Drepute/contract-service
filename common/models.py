import enum
from datetime import datetime

from db import db


class CreatedAtMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class CreatedUpdatedAtMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
