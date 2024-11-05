from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import validates

from app import db

class LBG_EPC_SUBMISSION(db.model):
    __tablename__ = 'submission'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(50))
    email_address = Column(String(50))
    phone_number = Column(String(50))
    address = Column(String(50))
    region = Column(String(50))

    def __str__(self):
        return self.name

    @validates('region')
    def validate_region(self, key, value):
        assert value in ['England','Scotland','Wales','Northern Ireland']
        return value
