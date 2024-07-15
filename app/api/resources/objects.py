import inspect
import sys

import inflection

from resources import db


class BaseTable:
    table_type = None
    db_table_name = None
    id_column = None

    @classmethod
    def init(cls):
        cls.table_type = inflection.underscore(cls.__name__)
        cls.db_table_name = f"{cls.table_type}s"
        cls.id_column = f"{cls.table_type}_id"

    @classmethod
    def create_instance(cls, values, db_config=None):
        new_id = db.insert_row(cls.db_table_name, None, values, db_config)
        if new_id:
            return cls.get_instance(new_id, db_config)
        return None

    @classmethod
    def get_instance(cls, id, db_config=None):
        return cls(
            db.read_one(
                query=f"SELECT * FROM {cls.db_table_name} WHERE {cls.id_column}={id}",
                db_config=db_config,
            )
        )

    @classmethod
    def get_instance_where(cls, where_clause, db_config=None):
        query = f"SELECT * FROM {cls.db_table_name} WHERE {where_clause}"
        return cls(
            db.read_one(
                query=query,
                db_config=db_config,
            )
        )

    @classmethod
    def list_instances(cls, limit: int = None, db_config=None):
        limit_clause = f"LIMIT {limit}" if limit else ""
        return [
            cls(row)
            for row in db.read(
                query=f"SELECT * FROM {cls.db_table_name} {limit_clause}",
                db_config=db_config,
            )
        ]

    @classmethod
    def update_instance(cls, id, values, db_config=None):
        db.update_row(cls.db_table_name, cls.id_column, id, values, db_config)

    @classmethod
    def get_single_value(cls, value, instance_id, db_config=None):
        return db.get_single_value(
            query=f"SELECT * FROM {cls.db_table_name} WHERE {cls.id_column}={instance_id}",
            value=value,
            db_config=db_config,
        )

    def _set_attributes(self, db_row):
        for key, value in db_row.items():
            setattr(self, key, value)

    def __init__(self, db_row={}):
        return self._set_attributes(db_row) if db_row else None

    def get_dict(self, include_id=False):
        attributes = self.__dict__
        if not include_id:
            attributes.pop(self.id_column, None)
        if "created_at" in attributes:
            # Convert datetime object to string
            attributes["created_at"] = attributes["created_at"].isoformat()
        return attributes

    def get_id(self):
        return getattr(self, self.id_column)

    def get_json(self):
        import json

        return json.dumps(self.get_dict(True))

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.get_dict(True)) + ")"

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.get_dict(True)) + ")"

    def __eq__(self, other):
        if isinstance(other, BaseTable):
            return self.get_dict(True) == other.get_dict(True)
        return False


class User(BaseTable):
    user_id = str()
    username = None
    password = None
    user_email = None
    is_email_verified = bool()
    created_at = None


_tables_initialized = False


def _intialize_tables():
    global _tables_initialized
    if _tables_initialized:
        return
    tables = []
    for _, member in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        member.init()
        tables.append(member)
    _tables_initialized = True


_intialize_tables()
