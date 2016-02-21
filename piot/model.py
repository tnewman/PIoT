""" PIoT Model
"""

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PagedResult:
    """ Paged Query Results
    """

    page_number = int()
    """ The Current Page Number """

    page_size = int()
    """ The Size of Each Page """

    total_pages = int()
    """ The Total Number of Pages """

    elements = []
    """ Elements for the Current Page """

class SensorReading(Base):
    """ Sensor Reading
    """

    __tablename__ = 'sensorreading'
    
    id = Column(Integer, primary_key=True)
    """ Sensor Reading Unique Identifier """

    name = Column(String)
    """ Sensor Name """

    sensor_type = Column(String)
    """ Sensor Type """

    timestamp = Column(DateTime)
    """ Timestamp from When the Sensor Was Read """

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': sensor_type
    }


class AnalogSensorReading(SensorReading):
    """ Analog Sensor Reading
    """

    __tablename__ = 'analogsensorreading'

    id = Column(Integer, ForeignKey('sensorreading.id'), primary_key=True)
    """ Analog Sensor Reading Unique Identifier """

    value = Column(Numeric(precision=6, scale=2))
    """ Sensor Reading Value """

    unit = Column(String)
    """ Sensor Reading Unit """

    __mapper_args__ = {
        'polymorphic_identity': 'analogsensorreading',
    }


class DigitalSensorReading(SensorReading):
    """ Digital Sensor Reading
    """

    __tablename__ = 'digitalsensorreading'

    id = Column(Integer, ForeignKey('sensorreading.id'), primary_key=True)
    """ Digital Sensor Reading Unique Identifier """

    value = Column(Boolean)
    """ Sensor Reading Value """

    __mapper_args__ = {
        'polymorphic_identity': 'digitalsensorreading',
    }


class NotificationEvent(Base):
    """ Notification Event Log

        Notifications are sent when a sensor reading is abnormal, and those
        notification logs are stored here.
    """

    __tablename__ = 'notificationevent'

    id = Column(Integer, primary_key=True)
    """ Notification Log Unique Identifier """

    sensor_id = Column(Integer, ForeignKey('sensorreading.id'))
    """ Associated Sensor Unique Identifier """

    timestamp = Column(DateTime)
    """ Time Notification was Sent """
