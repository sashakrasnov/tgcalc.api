# -*- coding: utf-8 -*-
import flask.json as json
from sqlalchemy.sql import text
from consts import *
from hashlib import md5

"""
Функции
"""

# Возврат ответа с кодом ошибки, в формате JSON. error: 0 -- нет ошибки
def error_resp(code, resp=None):
    if resp is not None:
        return json.jsonify({'error': code, 'response': resp}), 200
    else:
        return json.jsonify({'error': code}), 405

# Загрузка билета по id билета
def load_ticket(id, con):
    q = text("SELECT `e`.*, UNIX_TIMESTAMP(`e`.`dt`) AS `e_utime`, `t`.`id` AS `tid`, `t`.`tg_id`, `t`.`t_buy`, `t`.`t_refund`, `t`.`status` AS `t_status`, `t`.`t_code`, `t`.`ts`, UNIX_TIMESTAMP(`t`.`ts`) AS `t_utime` FROM `events` AS `e` , `tickets` AS `t` WHERE `t`.`event_id` = `e`.`id` AND `t`.`id` = :i")

    try:
        return format_ticket(con.execute(q, i=id).fetchone())

    except:
        return None

def format_ticket(r):
    if r:
        event = {'id': r['id'],                     # идентификатор мероприятия
                 'title': r['title'],               # название мероприятия
                 'descr': r['descr'],               # краткое описание мероприятия
                 'long_descr': r['long_descr'],     # длинное описание мероприятия
                 'org_id': r['org_id'],             # id организации
                 'lang_id': r['lang_id'],           # id языка мероприятия
                 'dt': str(r['dt']),                # datetime мероприятия
                 'd': r['dt'].strftime(DT_FORMAT),  # дата мероприятия
                 't': r['dt'].strftime('%H:%M'),    # время начала мероприятия
                 'utime': r['e_utime'],             # unixtime мероприятия
                 'status': r['status'],             # статус мероприятия. -1: отмена, 0: неподтв., 1: подтв.
                 'game_id': r['game_id'],           # тип игры. фактически не используется
                 'city_id': r['city_id'],           # id города проведения мероприятия
                 'addr': r['addr'],                 # адрес проведения мероприятия
                 'map': r['map'],                   # ссылка на карту адреса проведения мероприятия
                 'price': r['price'],               # стоимость билета
                 'count_min': r['count_min'],       # минимальное количество билетов
                 'count_max': r['count_max'],       # максимальное количество билетов
                 'count_free': r['count_free'],     # количество бесплатных мест
                 'count_paid': r['count_paid'],     # количество оплаченных билетов
                 'link': r['link'],                 # ссылка на фотоотчет
                 'images': event_images(r)}         # картинки к событию

        t_no = '{}-{}'.format(r['t_code'], r['tid'])
        ticket = {'id': r['tid'],                    # id билета
                  'tg': r['tg_id'],                  # id ТГ-пользователя
                  'buy': r['t_buy'],                 # транзакция покупки
                  'refund': r['t_refund'],           # транзакция возврата
                  'code': r['t_code'],               # код билета
                  'number': t_no,                    # полный номер билета <code>-<id>
                  'status': r['t_status'],           # статус билета. -1: возврат, 0: норм, 1: погашен
                  'utime': r['t_utime'],             # unixtime момента покупки билета
                  'dt': str(r['ts']),                # стандартный таймстемп даты и времени покупки билета
                  'd': r['ts'].strftime(DT_FORMAT),  # дата мероприятия
                  't': r['ts'].strftime('%H:%M'),    # время начала мероприятия
                  'image': URL_IMAGES + '/t/' + t_no + '.' + TYPE_IMG + '?key=' + md5('{}{}{}'.format(t_no, r['org_id'], SALT_KEY).encode('utf-8')).hexdigest()}

        return {'event': event, 'ticket': ticket}

    else:
        return {}

# Загрузка юзера по его id
def load_user(id, con, cache=None):
    if cache is not None:
        try:
            val = cache.get('tg:' + str(id)).decode()
        except:
            val = ''
    else:
        val = None

    try:
        r = con.execute(text("SELECT *, UNIX_TIMESTAMP(`ts`) AS `utime` FROM `tg_users` WHERE `id` = :i"), i=id).fetchone()

        resp = {'uid': r['id'],                # id Tg-юзера
                'uname': r['uname'],           # Tg-юзер
                'fname': r['fname'],           # полное имя пользователя
                'langs': r['langs'],           # языки мероприятий
                'lang_id': r['lang_id'],       # язык Tg-бота
                'city_def': r['city_def'],     # город "по-умолчанию"
                'ts': str(r['ts']),            # таймстемп регистрации
                'utime': r['utime'],           # unixtime регистрации
                'src': r['src'],               # источник посещения
                'd': r['ts'].strftime(DT_FORMAT),
                't': r['ts'].strftime('%H:%M')} if r else {}

    except:
        resp = None

    if resp:# is not None:
        resp['cache'] = val
    else:
        resp = {'cache': val} if val else None

    return resp

# построение списка изображений к событию по готовой выборке
def event_images(e, id='id'):
    imgs = list()

    for i in range(1, NUM_IMAGES + 1):
        img_ext = 'img_ext_' + str(i)
        if e[img_ext]:
            imgs.append(URL_IMAGES + '/e/' + str(e[id]) + '-' + str(i) + '.' + e[img_ext])

    return imgs