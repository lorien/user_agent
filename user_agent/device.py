import os.path
import json


PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))
SMARTPHONE_DEV_IDS = json.load(open(os.path.join(
    PACKAGE_DIR, 'data/smartphone_dev_id.json')))
TABLET_DEV_IDS = json.load(open(os.path.join(
    PACKAGE_DIR, 'data/tablet_dev_id.json')))
