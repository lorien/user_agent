import os.path
import json


PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(PACKAGE_DIR, 'data/smartphone_dev_id.json')) as f:
    SMARTPHONE_DEV_IDS = json.load(open(f))
with open(os.path.join(PACKAGE_DIR, 'data/tablet_dev_id.json')) as f:
    TABLET_DEV_IDS = json.load(open())
