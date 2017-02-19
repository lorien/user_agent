from grab.spider import Spider, Task
from grab import Grab
from six.moves.urllib.parse import quote_plus
from pymongo import MongoClient
from pprint import pprint
from weblib.error import DataNotFound

db = MongoClient()['user_agent']


class ArenaSpider(Spider):
    def task_generator(self):
        for dev in db.dev_ua.find():
            html = db.html.find_one({'_id': dev['name']})
            if html:
                grab = Grab(html['html'].encode('utf-8'))
                try:
                    self.task_device(grab, Task(url='http://example.com',
                                                dev=dev))
                except DataNotFound as ex:
                    print(ex)
            else:
                continue
                url = ('http://www.gsmarena.com/results.php3'
                       '?sQuickSearch=yes&sName=%s' % quote_plus(dev['_id']))
                yield Task('search', url=url, dev=dev)

    def task_search(self, grab, task):
        print('Searching for %s' % task.dev['name'])
        if grab.doc('//h1[@class="specs-phone-name-title"]').exists():
            self.task_device(grab, task)
        else:
            for elem in grab.doc('//div[@class="makers"]/ul/li/a/strong/span'):
                name = elem.text(smart=True)
                if name.lower() == task.dev['name'].lower():
                    url = grab.make_url_absolute(
                        elem.select('../../@href').text())
                    yield Task('device', url=url, dev=task.dev)

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

    def parse_display_size(self, grab):
        data = grab.doc('//td[a[text()="Size"]]'
                        '/following-sibling::td').text()
        return float(data.split('inches')[0].strip())

    def task_device(self, grab, task):
        name = grab.doc('//h1[@class="specs-phone-name-title"]').text()
        if name.lower() == task.dev['name'].lower():
            db.html.save({
                '_id': task.dev['name'],
                'html': grab.doc.unicode_body(),
            })
            device = {
                '_id': task.dev['name'].lower(),
                'name': task.dev['name'],
                'resolution': self.parse_resulution(grab),
                'released': self.parse_released(grab),
                'cpu': self.parse_cpu(grab),
                'os': self.parse_os(grab),
                'display_size': self.parse_display_size(grab),
            }
            db.device.save(device)
            pprint(device)


def main(**kwargs):
    bot = ArenaSpider(thread_number=1)
    try:
        bot.run()
    finally:
        bot.render_stats(timing=False)
