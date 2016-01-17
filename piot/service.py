from contextlib import contextmanager
from piot import config
from piot.model import NotificationEvent, SensorReading
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.sql_alchemy_connection_string)


@contextmanager
def transaction_scope():
    """ Wraps SQLAlchemy operations. Commits a session if there are no errors,
        rolls back a session on exception and closes a session in either case.
    """
    session_class = sessionmaker(bind=engine, expire_on_commit=False)
    session = session_class()
    
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class BaseSQLAlchemyService:
    """ Base Class providing CRUD (Create, Read, Update and Delete) operations
        to all services that rely on SQLAlchemy.
    """

    def __init__(self, model):
        """ Constructor
        :param model: Model Class used by child service.
        :type model: piot.model.Base
        """
        self._model = model
    
    def all(self):
        """ Retrieve all records.
        :return: All records.
        :rtype model: piot.model.Base
        """
        with transaction_scope() as session:
            records = session.query(self._model).with_polymorphic('*').all()

        return records
    
    def get(self, key):
        """ Retrieves a specific record.
        :param key: Primary Key of record to retrieve.
        :return: Record specified by the id.
        """
        with transaction_scope() as session:
            record = session.query(self._model).with_polymorphic('*') \
                .filter_by(id=key).first()

        return record

    def create(self, object):
        with transaction_scope() as session:
            session.add(object)

    def update(self, object):
        with transaction_scope() as session:
            session.merge(object)
    
    def delete(self, object):
        with transaction_scope() as session:
            session.delete(object)


class NotificationEventService(BaseSQLAlchemyService):
    def __init__(self):
        super().__init__(NotificationEvent)

    def get_newest_notification(self):
        with transaction_scope() as session:
            record = session.query(self._model).order_by(
                    desc(self._model.timestamp)).first()

        return record


class SensorReadingService(BaseSQLAlchemyService):
    def __init__(self):
        super().__init__(SensorReading)
