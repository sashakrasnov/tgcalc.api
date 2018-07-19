# -*- coding: utf-8 -*-
from flask import Flask
from sqlalchemy import create_engine
from redis import StrictRedis

engine = create_engine('mysql+mysqldb://<mysql_user>:<mysql_pass>@12playerdb.mysql.database.azure.com:3306/mundial?charset=utf8mb4', pool_pre_ping=True)

cache = StrictRedis(host='12playerdb.redis.cache.windows.net', port=6380, password='<redis_pass>', ssl=True)

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

from routes1 import *