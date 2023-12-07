from sqlalchemy.dialects.mysql import JSON

from common.models import (
    CreatedUpdatedAtMixin,
    CreatedAtMixin
)
from db import db

    

class Subscription(CreatedUpdatedAtMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(72), nullable=False)
    abi = db.Column(JSON(none_as_null=False))
    chain_id = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.Text())
    from_block = db.Column(db.Integer, nullable=False)
    to_block = db.Column(db.Integer)
    last_synced_block = db.Column(db.Integer, default=0)
    block_difference = db.Column(db.Integer, default=100)
    is_active = db.Column(db.Boolean, default=True)
    cache_options = db.Column(JSON(none_as_null=False))

    def get_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "chain_id": self.chain_id,
            "topic": self.topic,
            "from_block": self.from_block,
            "to_block": self.to_block,
            "last_synced_block": self.last_synced_block,
            "block_difference": self.block_difference,
            "is_active": self.is_active,
        }