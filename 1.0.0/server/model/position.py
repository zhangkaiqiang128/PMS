from dao.db import DataBase


class Position:

    def __init__(self):
        self.id = 0
        self.lat = 34.000122
        self.lng = 108.444756
        self.post_time = "2016-08-02 05:04:32"
        self.receive_time = "2016-08-02 05:04:32"
        self.device_id = "41584322"
        self.device_type = "mobile"
        self.coords_type = ""

    def save(self):

        sql = 'INSERT INTO position (lat,lng,post_time,receive_time,device_id,device_type,coords_type) VALUES (%f, %f, "%s", "%s", "%s", "%s","%s")' \
              % \
              (self.lat, self.lng, self.post_time, self.receive_time, self.device_id, self.device_type,self.coords_type)

        db = DataBase()
        db.save(sql)
        db.close()

    @staticmethod
    def query_all():

        db = DataBase()
        res = db.query("select * from position")

        db.close()

        return res