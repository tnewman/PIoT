from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensorReading(Base):
    __tablename__ = 'sensorreading'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Numeric(precision=6, scale=2))
    unit = Column(String)
    sensor_type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'sensorreading',
        'polymorphic_on': sensor_type
    }

    def __repr__(self):
        return 'SensorReading(name=\'%s\', value=\'%s\', unit=\'%s\')' \
            % (self.name, self.value, self.unit)


class AnalogSensorReading(SensorReading):
    __tablename__ = 'analogsensorreading'

    id = Column(Integer, ForeignKey('sensorreading.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'analogsensorreading',
    }


class DigitalSensorReading(SensorReading):
    __tablename__ = 'digitalsensorreading'

    id = Column(Integer, ForeignKey('sensorreading.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'digitalsensorreading',
    }