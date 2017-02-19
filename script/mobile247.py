from grab.spider import Spider, Task

from .arena import db


class MobileSpider(Spider):
    def task_generator(self):
        yield Task('home', url='http://www.mobile247.eu/online-tools'
                               '/user-agent-strings')

    def task_home(self, grab, task):
        for elem in grab.doc('//table[@id="uas_index"]/tr[2]/td[4]/a'):
            dev = elem.text()
            print(dev)
            dev = {
                '_id': dev.lower(),
                'name': dev,
            }
            db.dev_ua.save(dev)
            yield Task('dev', url=elem.attr('href'), dev=dev)

    def task_dev(self, grab, task):
        uas = []
        for elem in grab.doc('//td[@class="uas_useragent"]'):
            ua = elem.text()
            print(ua)
            uas.append(ua)
        db.dev_ua.update(
            {'_id': task.dev['_id']},
            {'$set': {'uas': uas}},
        )


def main(**kwargs):
    bot = MobileSpider(thread_number=1)
    try:
        bot.run()
    finally:
        bot.render_stats(timing=False)
