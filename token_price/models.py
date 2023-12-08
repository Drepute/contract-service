from common.models import CreatedUpdatedAtMixin
from db import db
import enum


class TaskStatus(enum.IntEnum):
    DONE = 1
    PROCESSING = 2
    FAILED = 3

class TokenPriceSubscription(CreatedUpdatedAtMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(72), nullable=False)
    decimals = db.Column(db.Integer, nullable=False)
    market = db.Column(db.String(16), nullable=False)
    time_interval = db.Column(db.Integer, nullable=False)
    start_timestamp = db.Column(db.BigInteger, nullable=False)
    last_synced_timestamp = db.Column(db.BigInteger, nullable=False)
    exchange = db.Column(db.String(32), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    state = db.Column(db.Enum(TaskStatus), default=TaskStatus.DONE)

    def get_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "decimals": self.decimals,
            "time_interval": self.time_interval,
            "start_timestamp": self.start_timestamp,
            "last_synced_timestamp": self.last_synced_timestamp,
            "exchange": self.exchange,
            "state": self.state
        }