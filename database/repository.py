from database.connection import get_connection


class Repository:

    def __init__(self):

        self.connection = get_connection()

        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):

        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)

    def executemany(self, query, params):

        self.cursor.executemany(query, params)

    def fetchone(self):

        return self.cursor.fetchone()

    def fetchall(self):

        return self.cursor.fetchall()

    def commit(self):

        self.connection.commit()

    def rollback(self):

        self.connection.rollback()

    def close(self):

        self.cursor.close()

        self.connection.close()

    def get_existing_call_ids(self, table_name):

        query = f"""
        SELECT [Call ID]
        FROM [{table_name}]
        """

        self.execute(query)

        rows = self.fetchall()

        return set(row[0] for row in rows)