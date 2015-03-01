import datetime
from pytz import timezone
import pytz


class TestModel(object):
    def __init__(self, data):
        self.title = data.get('title')
        self.type = data.get('type')
        self.modified = datetime.datetime.now(timezone('US/Eastern'))