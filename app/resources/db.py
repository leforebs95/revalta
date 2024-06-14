import logging
import time
import mariadb
import environment


def _generate_insert_query(
    table_name, key_name, key_value_map, ignore=False, skip_created_at=False
):
    query = f"INSERT INTO {table_name} "
    if ignore:
        query += "IGNORE "
    query += "("
    if "created_at" not in key_value_map and not skip_created_at:
        query += "created_at, "
    if key_name:
        query += f"{key_name}, "
    query += ", ".join(key_value_map.keys())
    query += ") VALUES ("
    if "created_at" not in key_value_map and not skip_created_at:
        query += "NOW(), "
    if key_name:
        query += "?, "
    query += ", ".join(["?" for _ in key_value_map])
    query += ")"
    return query


def _generate_update_query_where(table_name, key_value_map, where_clause):
    query = f"UPDATE {table_name} SET "
    query += ", ".join([f"{k} = ?" for k in key_value_map.keys()])
    if where_clause:
        query += f" WHERE {where_clause}"
    return query


def _generate_update_query(
    table_name, key_name, key_value_map, add_where_clause: bool = False
):
    where_clause = None
    if add_where_clause:
        where_clause = f"{key_name} = ?"
    return _generate_update_query_where(table_name, key_value_map, where_clause)


def _generate_bindings(key_name, key_value, key_value_map):
    vals = tuple()
    if key_name and key_name not in key_value_map.keys():
        vals += (key_value,)
    for val in key_value_map.values():
        vals += (val,)
    return vals


def build_insert_query_bindings(table_name, key_name, key_value_map, ignore=False):
    query = _generate_insert_query(table_name, key_name, key_value_map, ignore)
    bindings = _generate_bindings(None, None, key_value_map)
    return query, bindings


def build_update_query_bindings(table_name, key_name, key_val, key_value_map):
    query = _generate_update_query(table_name, key_name, key_value_map, True)
    bindings = _generate_bindings(None, None, key_value_map)
    bindings += (key_val,)
    return query, bindings


class DatabaseConnection:
    log_quieries = True
    query_set = set()

    def _create_connection(self):
        return mariadb.connect(
            host=self._config["host"],
            port=3306,
            user=self._config["user"],
            database=self._db_name,
            password=self._config["password"],
        )

    def __init__(self, db_name: str = None, db_config: dict = None):
        self._db_conn = None
        self._config = (
            db_config
            if db_config and isinstance(db_config, dict)
            else environment.get_config()["db"]
        )
        self._db_name = db_name or self._config["db-name"]
        self._connect_time = time.time()
        self._curr_cursor = None
        self._db_conn = self._create_connection()

    def __del__(self):
        if self._db_conn:
            self._db_conn.close()
            self._db_conn = None

    def rollback(self):
        try:
            self._db_conn.rollback()
        except mariadb.Error as e:
            logging.error(f"Error occurred during rollback: {e}")

    def get_current_cursor(self):
        if not self._curr_cursor:
            self._curr_cursor = self._db_conn.cursor()
        return self._curr_cursor

    def close_current_cursor(self):
        if self._curr_cursor:
            self._curr_cursor.close()
            self._curr_cursor = None

    def log_query(self, query, bindings=None):
        if DatabaseConnection.log_quieries:
            print(
                f'Executing {query} with {bindings} on {(self._db_name, self._config["host"])}'
            )
            DatabaseConnection.query_set.add(query)

    def log_db_status(self):
        logging.info(f"DB Connection: {self._db_conn}")
        logging.info(f"DB Connection Time: {self._connect_time}")
        logging.info(f"DB Cursor: {self._curr_cursor}")
        logging.info(f"DB Queries: {DatabaseConnection.query_set}")

    def execute_query(self, query, bindings=None):
        cursor = self.get_current_cursor()
        self.log_query(query, bindings)
        try:
            cursor.execute(query, bindings)
        except mariadb.Error as e:
            logging.error(f"Error occurred during query execution: {e}")
            self.rollback()

        return cursor

    def read(self, query):
        cursor = self.execute_query(query)
        col_names = [desc[0] for desc in cursor.description]
        try:
            rows = cursor.fetchall()
        except mariadb.Error as e:
            logging.warn(f"Error occurred during read: {e}")
            return None
        if not rows:
            logging.warn(f"No rows found for query: {query}")
            return list(dict())
        return [dict(zip(col_names, row)) for row in rows]

    def read_one(self, query):
        cursor = self.execute_query(query)
        col_names = [desc[0] for desc in cursor.description]
        try:
            row = cursor.fetchone()
        except mariadb.Error as e:
            logging.warn(f"Error occurred during read_one: {e}")
            return None
        if not row:
            logging.warn(f"No rows found for query: {query}")
            return dict()
        return dict(zip(col_names, row))

    def get_single_value(self, query, value):
        return self.read_one(query).get(value, None)

    def write(self, query, bindings, dry_run=False):

        if dry_run:
            logging.info(f"DRY RUN: {query}")
            return None

        self.execute_query(query, bindings)
        try:
            self._db_conn.commit()
            lid = self._curr_cursor.lastrowid
            return lid
        except mariadb.Error as e:
            if isinstance(e, mariadb.OperationError):
                logging.error(f"Error occurred during write, attempting rollback: {e}")
                self.rollback()

            raise e

    def write_insert(
        self,
        table_name,
        key_name,
        key_value_map,
        ignore=False,
        dry_run=False,
    ):
        query, bindings = build_insert_query_bindings(
            table_name, key_name, key_value_map, ignore
        )
        return self.write(query, bindings, dry_run)

    def write_update(
        self,
        table_name,
        key_name,
        key_val,
        key_value_map,
        dry_run=False,
    ):
        query, bindings = build_update_query_bindings(
            table_name, key_name, key_val, key_value_map
        )
        return self.write(query, bindings, dry_run)

    def close(self):
        if self._db_conn:
            self.close_current_cursor()
            self._db_conn.close()
            self._db_conn = None


def read(query, db_config=None):
    db_conn = DatabaseConnection(db_config=db_config)
    return db_conn.read(query)


def read_one(query, db_config=None):
    db_conn = DatabaseConnection(db_config=db_config)
    return db_conn.read_one(query)


def get_single_value(query, value, db_config=None):
    db_conn = DatabaseConnection(db_config=db_config)
    return db_conn.get_single_value(query, value=value)


def insert_row(
    table_name, key_name, key_value_map, ignore=False, dry_run=False, db_config=None
):
    db_conn = DatabaseConnection(db_config=db_config)
    return db_conn.write_insert(table_name, key_name, key_value_map, ignore, dry_run)


def update_row(
    table_name, key_name, key_val, key_value_map, dry_run=False, db_config=None
):
    db_conn = DatabaseConnection(db_config=db_config)
    return db_conn.write_update(table_name, key_name, key_val, key_value_map, dry_run)
