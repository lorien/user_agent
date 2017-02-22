from pprint import pprint
from itertools import islice
import time
import re

from grab.spider import Spider, Task
from grab import Grab
from six.moves.urllib.parse import quote_plus
from pymongo import MongoClient
from weblib.error import DataNotFound
import time

db = MongoClient()['user_agent']


class InvalidUserAgent(Exception):
    pass


class ArenaSpider(Spider):
    re_android_ver = re.compile(r'v\d+\.\d+(?:\.\d+)?')

    def parse_dev_id(self, ua):
        if 'Linux; Android' in ua:
            if 'Build/' not in ua:
                raise InvalidUserAgent
            else:
                try:
                    dev_id = (ua.split('Linux; Android')[1]
                                .split(')')[0].split(';')[1]).strip()
                except IndexError:
                    raise InvalidUserAgent
                else:
                    model_id = dev_id.split(' Build/')[0].strip()
                    return model_id, dev_id
        else:
            raise InvalidUserAgent

    def iterate_dev_id(self):
        for line in open('var/ua_linux_android.txt'):
            count, ua = line.strip().split(' ', 1)
            if int(count) > 10:
                try:
                    model_id, dev_id = self.parse_dev_id(ua)
                except InvalidUserAgent as ex:
                    self.stat.inc('invalid-ua')
                else:
                    print('UA: %s' % ua)
                    print('MODEL: %s' % model_id)
                    print('DEV: %s' % dev_id)
                    yield model_id, dev_id

    def task_generator(self):
        for model_id, dev_id in islice(self.iterate_dev_id(), 1000000):
            if db.not_found.find_one({'_id': model_id.lower()}):
                self.stat.inc('skip-not-found')
                continue
            if db.dev.find_one({'_id': model_id.lower()}):
                self.stat.inc('skip-exists')
                continue
            url = ('http://www.gsmarena.com/results.php3'
                   '?sQuickSearch=yes&sName=%s' % quote_plus(model_id))
            yield Task('search', url=url, model_id=model_id,
                       dev_id=dev_id)
            time.sleep(0.1)

    def task_search(self, grab, task):
        print('Searching for %s' % task.dev_id)
        if grab.doc('//h1[@class="specs-phone-name-title"]').exists():
            self.task_device(grab, task)
        else:
            db.not_found.save({'_id': task.model_id.lower()})
            self.stat.inc('search-no-device-redirect')

    def parse_resulution(self, grab):
        data = grab.doc('//td[a[text()="Resolution"]]'
                        '/following-sibling::td').text()
        if 'pixels' in data:
            return [int(x.strip()) for x in data.split('pixels')[0].split('x')]
        else:
            return None

    def parse_released(self, grab):
        status = grab.doc('//td[a[text()="Status"]]'
                          '/following-sibling::td').text()
        announced = grab.doc('//td[a[text()="Announced"]]'
                             '/following-sibling::td').text()
        for data in (status, announced):
            if 'Released' in data:
                return int(data.split('Released')[1].strip().split(',')[0])
        return None

    def parse_cpu(self, grab):
        data = grab.doc('//td[a[text()="CPU"]]'
                        '/following-sibling::td').text()
        return data

    def parse_os(self, grab):
        data = grab.doc('//td[a[text()="OS"]]'
                        '/following-sibling::td').text()
        return data

    def parse_android_versions(self, grab):
        os = self.parse_os(grab).lower()
        if 'android' in os and self.re_android_ver.search(os):
            try:
                min_ver = self.re_android_ver.search(os).group(0)
                if 'upgradable' in os:
                    part = os.split('upgradable')[1]
                    max_ver = self.re_android_ver.search(part).group(0)
                else:
                    max_ver = min_ver
            except Exception:
                import pdb; pdb.set_trace()
            return min_ver, max_ver
        else:
            return None

    def parse_display_size(self, grab):
        data = grab.doc('//td[a[text()="Size"]]'
                        '/following-sibling::td').text()
        return float(data.split('inches')[0].strip())

    def parse_name(self, grab):
        return grab.doc('//h1').text()

    def task_device(self, grab, task):
        self.stat.inc('device-found')
        name = grab.doc('//h1[@class="specs-phone-name-title"]').text()
        device = {
            '_id': task.model_id.lower(),
            'model_id': task.model_id,
            'name': self.parse_name(grab),
            'resolution': self.parse_resulution(grab),
            'released': self.parse_released(grab),
            'cpu': self.parse_cpu(grab),
            'os': self.parse_os(grab),
            'android_versions': self.parse_android_versions(grab),
            'display_size': self.parse_display_size(grab),
        }
        db.dev.find_one_and_update(
            {'_id': task.model_id.lower()},
            {'$set': device,
            '$addToSet': {'dev_ids': task.dev_id}},
            upsert=True,
        )
        pprint(device)
        if not grab.doc.from_cache:
            time.sleep(0.5)


def main(**kwargs):
    bot = ArenaSpider(thread_number=1)
    bot.setup_cache('mongo', database='user_agent_cache')
    try:
        bot.run()
    finally:
        bot.render_stats(timing=False)
