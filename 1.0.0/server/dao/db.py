import pymysql
import dao.config as config


class DataBase:

    def __init__(self):

        self.con = pymysql.connect(host=config.host,
                                   port=config.port,
                                   user=config.user,
                                   db=config.database,
                                   passwd=config.passwd,
                                   charset=config.charset)

        self.cur = self.con.cursor()

    def save(self,sql):
        res = self.cur.execute(sql)
        self.con.commit()

    def query(self,sql):
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res

    def close(self):
        self.cur.close()
        self.con.close()