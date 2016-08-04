import datetime


class Cache:

    cache = {}

    @staticmethod
    def delete(item):
        del Cache.cache[item]

    @staticmethod
    def read():
        return Cache.cache

    @staticmethod
    def write(item):

        print("write")

        try:

            temp = Cache.cache[item.device_id]

            print(item.post_time >= temp['post_time'].strftime("%Y-%m-%d %H:%M:%S"))
            print(item.post_time)
            print(temp['post_time'].strftime("%Y-%m-%d %H:%M:%S"))

            if item.post_time >= temp['post_time'].strftime("%Y-%m-%d %H:%M:%S"):
                Cache.cache[item.device_id] = {
                    "post_time":datetime.datetime.strptime(item.post_time, "%Y-%m-%d %H:%M:%S"),
                    "receive_time":datetime.datetime.strptime(item.receive_time, "%Y-%m-%d %H:%M:%S"),
                    "device_id":item.device_id,
                    "device_type":item.device_type,
                    "lat":item.lat,
                    "lng":item.lng
                }
        except KeyError:

            Cache.cache[item.device_id] = {
                "post_time": datetime.datetime.strptime(item.post_time, "%Y-%m-%d %H:%M:%S"),
                "receive_time": datetime.datetime.strptime(item.receive_time, "%Y-%m-%d %H:%M:%S"),
                "device_id": item.device_id,
                "device_type": item.device_type,
                "lat": item.lat,
                "lng": item.lng
            }

