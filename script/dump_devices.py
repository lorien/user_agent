from grab.stat import Stat
import json

from .arena import db


def build_dev_ids(uas):
    res = set()
    for ua in uas:
        try:
            dev = ua.split('(')[1].split(')')[0]
            dev = dev.split(';')[-1].strip()
        except IndexError:
            pass
        else:
            if len(dev) >= 8:
                res.add(dev)
    return list(res)


def dump_devices(devices, file_token):
    res = []
    for dev, dev_ua in devices:
        ids = build_dev_ids(dev_ua['uas'])
        if ids:
            res.append({
                'name': dev['name'], 
                'released': dev['released'], 
                'cpu': dev['cpu'], 
                'resolution': dev['resolution'], 
                'ids': ids,
            })
    with open('user_agent/data/%s_dev_ext.json' % file_token, 'w') as out:
        json.dump(res, out, indent=2)
    with open('user_agent/data/%s_dev_id.json' % file_token, 'w') as out:
        ids = []
        for dev in res:
            ids.extend(dev['ids'])
        json.dump(ids, out, indent=2)


def main(**kwargs):
    stat = Stat()
    tablets = []
    smartphones = []
    for dev in db.device.find():
        if not dev['released']:
            stat.inc('released-none')
        else:
            stat.inc('released-ok')
            if dev['released'] >= 2014:
                stat.inc('released>=2014')
                dev_ua = db.dev_ua.find_one({'_id': dev['_id']})
                if dev_ua:
                    stat.inc('uas')
                    if dev['display_size'] >= 7:
                        tablets.append((dev, dev_ua))
                        stat.inc('tablet')
                    else:
                        smartphones.append((dev, dev_ua))
                        stat.inc('smartphone')
    dump_devices(smartphones, 'smartphone')
    dump_devices(tablets, 'tablet')
    print(stat.counters)
