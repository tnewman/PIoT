import piot.service
import pytest
from piot.model import Base
from sqlalchemy import create_engine

sqlalchemyengine = create_engine('sqlite:///:memory:')

@pytest.fixture()
def sqlalchemy():
    # SQLAlchemy recommends a single engine is used across an application
    piot.service.engine = sqlalchemyengine

    Base.metadata.drop_all(bind=sqlalchemyengine)
    Base.metadata.create_all(bind=sqlalchemyengine)
