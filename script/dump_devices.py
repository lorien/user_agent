from grab.stat import Stat
import json

from .arena import db


def dump_devices(devices, file_token):
    res = []
    for dev in devices:
        res.append({
            'name': dev['name'], 
            'dev_ids': dev['dev_ids'],
            'released': dev['released'], 
            'cpu': dev['cpu'], 
            'resolution': dev['resolution'], 
            'dev_ids': dev['dev_ids'],
        })
    with open('user_agent/data/%s_dev_ext.json' % file_token, 'w') as out:
        json.dump(res, out, indent=2)
    with open('user_agent/data/%s_dev_id.json' % file_token, 'w') as out:
        ids = []
        for dev in res:
            ids.extend(dev['dev_ids'])
        ids = sorted(ids)
        json.dump(ids, out, indent=2)


def parse_major_ver(val):
    return int(val.lstrip('v').split('.')[0])


def main(**kwargs):
    stat = Stat()
    tablets = []
    smartphones = []
    for dev in db.dev.find():
        if not dev['released']:
            stat.inc('released-none')
        else:
            stat.inc('released-ok')
            if dev['released'] >= 2014:
                stat.inc('released>=2014')
                if (dev['android_versions']
                    and parse_major_ver(dev['android_versions'][0]) >= 4):
                    if dev['display_size'] >= 7:
                        tablets.append(dev)
                        stat.inc('tablet')
                    else:
                        smartphones.append(dev)
                        stat.inc('smartphone')
                else:
                    stat.inc('skip-android-old')
            else:
                stat.inc('released<2014')
    dump_devices(smartphones, 'smartphone')
    dump_devices(tablets, 'tablet')
    print(stat.counters)
