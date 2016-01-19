#!/usr/bin/env python3
from piot import config
from piot.model import Base
from sqlalchemy import create_engine

sqlalchemyengine = create_engine(config.sql_alchemy_connection_string)

Base.metadata.create_all(bind=sqlalchemyengine)
