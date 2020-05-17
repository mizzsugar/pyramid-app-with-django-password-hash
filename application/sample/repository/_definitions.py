from typing import Final

import sqlalchemy.ext.declarative
import sqlalchemy


_Base: Final = sqlalchemy.ext.declarative.declarative_base()


class Migration(_Base):
    __tablename__ = 'migrations'

    version = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    applied_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=False), nullable=False)


class User(_Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    email = sqlalchemy.Column(sqlalchemy.Text, nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.text('CURRENT_TIMESTAMP'),
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.text('now()'),
    )
