from models import *
from datetime import datetime

@event.listens_for(ValuesFloat.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        ValuesFloat(offer_id=1, field_id=1, value=35),
        ValuesFloat(offer_id=1, field_id=3, value=2.5),
        ValuesFloat(offer_id=2, field_id=1, value=15),
        ValuesFloat(offer_id=3, field_id=1, value=25),
        ValuesFloat(offer_id=4, field_id=1, value=25),
        ValuesFloat(offer_id=5, field_id=1, value=1),
        ValuesFloat(offer_id=6, field_id=1, value=20),
    ])
    session.commit()

