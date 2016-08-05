from flask import Flask
from flask import redirect
from flask import request

from model.position import Position
from dao.cache import Cache

import time
import json
import urllib.request

app = Flask(__name__)


@app.route('/')
def index():
    return redirect("static/index.html")


@app.route("/api/position/submit")
def position_submit():

    position = Position()

    position.lng = float(request.args.get("lng"))
    position.lat = float(request.args.get("lat"))
    position.device_id = request.args.get("id")
    position.device_type = request.args.get("type")
    position.coords_type = request.args.get("coords_type")

    position.post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(request.args.get("time"))/1000))
    position.receive_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    Cache.write(position)
    position.save()

    res = {
        "status": 200,
        "message": "success",
        "content": {}
    }

    return json.dumps(res)


@app.route("/api/position/query_all")
def position_query_all():
    position = Position()
    res = position.query_all()

    content = []

    for p in res:
        print(p)
        content.append({
            "id": p[0],
            "lat": p[1],
            "lng": p[2],
            "postTime": int(time.mktime(p[3].timetuple())*1000),
            "receiveTime": int(time.mktime(p[4].timetuple())*1000),
            "deviceId": p[5],
            "deviceType": p[6],
            "coords_type": p[7]
        })

    return json.dumps({
        "status": 200,
        "message": "success",
        "content": content
    })


@app.route("/api/position/query_last")
def position_query_last():
    res = Cache.read()

    content = []
    del_list = []

    for i in res.items():

        p = i[1]

        if time.time() - int(time.mktime(p['post_time'].timetuple())) > 30:
            del_list.append(i[0])

        coords_type = p['coords_type']

        if  coords_type == 'gps' or coords_type == "wgs84":
            url = "http://api.map.baidu.com/geoconv/v1/?ak=v6h8X6k5VpdFHrYsWDZiyWmlGBzyd8zn&from=1&coords="+str(p['lng'])+","+str(p['lat'])
        elif coords_type == 'gcj02':
            url = "http://api.map.baidu.com/geoconv/v1/?ak=v6h8X6k5VpdFHrYsWDZiyWmlGBzyd8zn&from=3&coords="+str(p['lng'])+","+str(p['lat'])
        elif coords_type == 'bd09ll':
            url = "http://api.map.baidu.com/geoconv/v1/?ak=v6h8X6k5VpdFHrYsWDZiyWmlGBzyd8zn&from=5&coords="+str(p['lng'])+","+str(p['lat'])

        convert = urllib.request.urlopen(url).read().decode('utf-8')
        convert = json.loads(convert)

        content.append({
            "lat": convert['result'][0]['y'],
            "lng": convert['result'][0]['x'],
            "postTime": int(time.mktime(p['post_time'].timetuple()) * 1000),
            "receiveTime": int(time.mktime(p['receive_time'].timetuple()) * 1000),
            "deviceId": p['device_id'],
            "deviceType": p['device_type'],
            "coords_type": "bd09ll"
        })

    for item in del_list:
        Cache.delete(item)

    return json.dumps({
        "status": 200,
        "message": "success",
        "content": content
    })

if __name__ == '__main__':
    app.run(host="www.zhangkaiqiang.com",
            port=5005)
