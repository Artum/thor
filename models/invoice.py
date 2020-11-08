from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func

from database import db

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = Column(String(256), primary_key=True)
    source_name = Column(String(256))
    source_address = Column(String(256))
    target_name = Column(String(256))
    target_address = Column(String(256))
    time_created = Column(DateTime(), server_default=func.now())
    time_updated = Column(DateTime(), onupdate=func.now())
    account_number = Column(String(512))
    amount = Column(Float(precision=2))
    time_invoice_begin = Column(DateTime())
    time_invoice_end = Column(DateTime())

    def __repr__(self):
       return f"<Invoice(id='{self.id}', source_name='{self.source_name}', source_address='{self.source_address}', target_name='{self.target_name}', target_address='{self.target_address}', time_created='{self.time_created}', time_updated='{self.time_updated}', account_number='{self.account_number}', amount='{self.amount}', time_invoice_begin='{self.time_invoice_begin}', time_invoice_end='{self.time_invoice_end}')>"
    
    def to_dict(self):
        return {
            "id": self.id, 
            "source_name": self.source_name,
            "source_address": self.source_address,
            "target_name": self.target_name,
            "target_address": self.target_address,
            "time_created": self.time_created,
            "time_updated": self.time_updated,
            "account_number": self.account_number,
            "amount": self.amount,
            "time_invoice_begin": self.time_invoice_begin,
            "time_invoice_end": self.time_invoice_end,
        }
