import sqlite3


class Sqlite3:
    """This class is sqlite3 wrapper...

    connect: db = Sqlite3(-dbname-)
    close: db.close()
    """

    def __init__(self, dbname):
        self.dbname = dbname
        self.db = sqlite3.connect(dbname)
        self.dbc = self.db.cursor()

    @staticmethod
    def _create_question(length):
        result = ""
        if length:
            for i in range(length - 1):
                result += "?, "
            result += "?"
        return result

    def tables(self):
        self.dbc.execute("select name from sqlite_master where type='table'")
        return [x[0] for x in self.dbc.fetchall()]

    def table(self, tablename):
        return Sqlite3Table(self, tablename)

    def __str__(self):
        return self.dbname


class Sqlite3Table:

    def __init__(self, db, tablename):
        self.db = db.db
        self.dbc = db.dbc
        self.tablename = tablename

    def execute(self, sql, values=None):
        if values:
            data = self.dbc.execute(sql, values)
        else:
            data = self.dbc.execute(sql)
        self.db.commit()

    def get(self, sql):
        return self.dbc.execute(sql).fetchall()

    def columns(self):
        return [x[0] for x in self.dbc.execute(
            "select * from {}".format(self.tablename)).description]

    def exists(self):
        return bool(self.get(
                "select count(*) from sqlite_master where type='table' and name='{}'".format(
                    self.tablename
                ))[0][0])

    def close(self):
        self.dbc.close()
        self.db.close()

    def create(self, *columns):
        self.execute("create table if not exists {0} ({1})".format(
            self.tablename,
            ",".join(columns)
            ))

    def insert(self, **data):
        self.execute("insert into {0}({1}) values({2})".format(
            self.tablename,
            ",".join(data),
            Sqlite3._create_question(len(data)),
            ), list(data.values()))

    def update(self, where, **sets):
        set_result = ""
        for key in sets:
            set_result += "{0}={1}, ".format(
                str(key),
                str(sets[key])
                if type(sets[key]) == int
                else "'"+str(sets[key])+"'",
                )
        self.execute(
                "update {0} set {1} where {2}".format(
                    self.tablename, set_result[:-2], where))

    def select_all(self, limit=-1):
        return self.get("select * from {}".format(self.tablename))

    def search(self, column, word):
        return self.get("select * from {0} where {1} like '%{2}%'".format(
            self.tablename,
            column,
            "%".join(word.split()),
            ))

    def delete_all(self):
        self.execute("delete from {}".format(self.tablename))

    def delete(self, where):
        self.execute("delete from {0} where {1}".format(self.tablename, where))

    def drop(self):
        self.execute("drop table {}".format(self.tablename))

    def __str__(self):
        return self.tablename
