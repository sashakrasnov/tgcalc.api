# -*- coding: utf-8 -*-
from flask import request
from sqlalchemy.sql import text
from functions import *
from consts import *
from tgcalc import app, engine
from hashlib import md5

# Информация о Телеграм-пользователе
# <token> -- цифровая подпись Tg-бота
# <uid>   -- id Tg-пользователя
@app.route('/user', methods=['GET'])
def get_user():
    token = request.args.get('token', type=str)
    uid   = request.args.get('uid',   type=int)

    if token == TG_TOKEN:
        if uid:
            try:
                con = engine.connect()
                u = load_user(uid, con)

                return error_resp(ERR_OK, u) if u else error_resp(ERR_DB)

            except:
                return error_resp(ERR_CONNECT)

            finally:
                con.close()
        else:
            return error_resp(ERR_USER_ID)
    else:
        return error_resp(ERR_TOKEN)

# Регистрация Телеграм-пользователей
# <token>   -- цифровая подпись Tg-бота
# <uid>     -- id Tg-юзера
# <uname>   -- имя Tg-юзера (username)
# <fname>   -- полное имя Tg-юзера, если есть (необязательный параметр)
# <lang_id> -- Идентификатор языка интерфейса (необязательный параметр)
# <src>     -- Источник посещения (необязательный параметр)
@app.route('/user/register', methods=['GET'])
def user_register():
    token = request.args.get('token',      type=str)
    uid   = request.args.get('uid',        type=int)
    uname = request.args.get('uname',  '', type=str)
    fname = request.args.get('fname',  '', type=str)
    lang  = request.args.get('lang_id', 0, type=int)
    src   = request.args.get('src',    '', type=str)

    if token == TG_TOKEN:
        if uid:
            try:
                con = engine.connect()

                try:
                    con.execute(text('INSERT INTO `tg_users` (`id`, `uname`, `fname`, `langs`, `lang_id`, `city_def`, `src`) VALUES (:id, :un, :fn, 0, :l, 1, :s)'), id=uid, un=uname, fn=fname, l=lang, s=src)

                    u = load_user(uid, con)

                    return error_resp(ERR_OK, u) if u else error_resp(ERR_DB)

                except:
                    return error_resp(ERR_DB)

            except:
                return error_resp(ERR_CONNECT)

            finally:
                con.close()

        else:
            return error_resp(ERR_USER_ID)
    else:
        return error_resp(ERR_TOKEN)

# Обновление Телеграм-пользователей. Если во время обновления были ошибки, то возвращается просто ошибка.
# Если ошибок не было, то возвращается обновленная информация о пользователе
# <token> -- цифровая подпись Tg-бота
# <uid>   -- id Tg-юзера
# <lang_id> -- язык интерфейса Tg-бота (Необязательный параметр)
# <langs>   -- битовая маска языков, на которых юзер готов участвовать  (Необязательный параметр)
# <uname>   -- имя Tg-юзера (username) (Необязательный параметр)
# <fname>   -- полное имя Tg-юзера (Необязательный параметр)
# <src>     -- Источник посещения (необязательный параметр)
# <city_def> -- город "по-умолчанию"
@app.route('/user/update', methods=['GET'])
def user_update():
    fields = {'lang_id':int, 'langs':int, 'fname':str, 'uname':str, 'src':str, 'city_def':int}

    token = request.args.get('token', type=str)
    uid   = request.args.get('uid',   type=int)

    if token == TG_TOKEN:
        if uid:
            try:
                con = engine.connect()

                for f in fields:
                    r = request.args.get(f, type=fields[f])
                    if r is not None:
                        trans = con.begin()
                        try:
                            con.execute(text("UPDATE `tg_users` SET `" + f + "` = :f WHERE `id` = :i"), f=r, i=uid)
                            trans.commit()
                        except:
                            trans.rollback()
                            return error_resp(ERR_DB)

                # если не было exceptions во время обновление прошло успешно, возвращает инфо о пользователе
                u = load_user(uid, con)

                return error_resp(ERR_OK, u) if u else error_resp(ERR_DB)

            except:
                return error_resp(ERR_CONNECT)

            finally:
                con.close()

        else:
            return error_resp(ERR_USER_ID)
    else:
        return error_resp(ERR_TOKEN)

# Обновление состояний дата-город. Для каждой комбинации дата/город может быть только одна запись
# В независимости от того, успешно добавилось или нет, возвращает список дата/город относительно <now>
# <token> -- цифровая подпись Tg-бота
# <uid>   -- id Tg-юзера
# <now>   -- дата "сегодня" в формате ГГГГ-ММ-ДД. Для разных часовых поясов она может быть своя
# <dt>    -- относительная дата к <now>. 0: сегодня, 1: завтра, 2: послезавтра, и т.д.
# <city>  -- id города, где проводится мероприятие
@app.route('/user/state', methods=['GET'])
def user_state():
    token = request.args.get('token', type=str)
    uid   = request.args.get('uid',   type=int)
    now   = request.args.get('now',   type=str)
    dt    = request.args.get('dt', 0, type=int)
    city  = request.args.get('city',  type=int)

    if token == TG_TOKEN:
        # заданы и дата и город
        if uid and now:
            try:
                con = engine.connect()

                if dt is not None and city is not None:
                    trans = con.begin()

                    try:
                        con.execute(text("DELETE FROM `states` WHERE `tg_id` = :i AND `dt` = DATE_ADD(:ymd, INTERVAL :d DAY)"), i=uid, ymd=now, d=dt)
                        con.execute(text("INSERT INTO `states` (`tg_id`, `dt`, `city_id`) VALUES (:i, DATE_ADD(:ymd, INTERVAL :d DAY), :c)"), i=uid, ymd=now, d=dt, c=city)
                        con.execute(text("UPDATE `tg_users` SET `city_def` = :c WHERE `id` = :i"), c=city, i=uid)
                        trans.commit()

                    except:
                        trans.rollback()
                        return error_resp(ERR_DB)

                # возвращаем список состояний в любом случае
                try:
                    res = con.execute(text("SELECT *, UNIX_TIMESTAMP(`dt`) AS `utime`, DATEDIFF(`dt`, :ymd) AS `diff` FROM `states` WHERE `tg_id` = :i AND `city_id` > 0 HAVING `diff` >= 0 AND `diff` <= 3 ORDER BY `dt` ASC LIMIT 25"), ymd=now, i=uid)

                    resp = []

                    for r in res:
                        resp.append({'d': r['dt'].strftime(DT_FORMAT), # дата по формату
                                     'dt': r['diff'],                  # дата относительно <now>
                                     'utime': r['utime'],              # unixtime даты
                                     'city_id': r['city_id']})         # id города проведения мероприятия

                    return error_resp(ERR_OK, resp)

                except:
                    return error_resp(ERR_DB)

            except:
                return error_resp(ERR_CONNECT)

            finally:
                con.close()

        else:
            return error_resp(ERR_USER_ID)
    else:
        return error_resp(ERR_TOKEN)

# Список событий, который возможен для данного пользователя с учетом его местоположения на определенную дату
# в определенном городе, при условии, что мероприятия удовлетворяют языкам и вообще доступны
# <token> -- цифровая подпись Tg-бота
# <uid>   -- id Tg-юзера
# <now>   -- дата "сегодня" в формате ГГГГ-ММ-ДД. Для разных часовых поясов она может быть своя
# <pg>    -- номер страницы. Не обязательный параметр. По-умолчанию "0" для первой страницы
# <lim>   -- количество записей на страницу. Не обязательный параметр. По-умолчанию "5"
@app.route('/user/events', methods=['GET'])
def user_events():
    token = request.args.get('token',  type=str)
    uid   = request.args.get('uid',    type=int)
    now   = request.args.get('now',    type=str)
    pg    = request.args.get('pg',  0, type=int)
    lim   = request.args.get('lim', 5, type=int)

    if token == TG_TOKEN:
        if uid and now:
            try:
                con = engine.connect()

                try:
                    res = con.execute("SELECT `e`.*, UNIX_TIMESTAMP(`e`.`dt`) AS `utime`, `u`.`city_def`, `s`.`dt` AS `state_dt`, `s`.`city_id` AS `state_city_id` FROM `tg_users` AS `u`, `events` AS `e` LEFT JOIN `states` AS `s` ON `s`.`dt`=DATE(`e`.`dt`) WHERE `u`.`id`=" + str(uid) + " AND (`e`.`lang_id` & `u`.`langs`=`e`.`lang_id` OR `u`.`langs`=0) AND `e`.`status`>=0 AND `e`.`count_paid`<`e`.`count_max` AND DATE(`e`.`dt`) BETWEEN '" + now + "' AND DATE_ADD('" + now + "', INTERVAL " + str(DT_EVENTS_INTERVAL) + " DAY) AND IF(`s`.`city_id` IS NOT NULL, `s`.`city_id`, `u`.`city_def`)=`e`.`city_id` ORDER BY `e`.`dt` ASC LIMIT " + str(lim) + " OFFSET " + str(pg*lim))

                    resp = []

                    for r in res:
                        resp.append({'eid': r['id'],                    # id мероприятия
                                     'title': r['title'],               # название мероприятия
                                     'descr': r['descr'],               # краткое описание мероприятия
                                     'long_descr': r['long_descr'],     # длинное описание мероприятия
                                     'org_id': r['org_id'],             # id организатора
                                     'utime': r['utime'],               # unixtime мероприятия
                                     'dt': str(r['dt']),                # datetime мероприятия
                                     'd': r['dt'].strftime(DT_FORMAT),  # дата мероприятия по формату
                                     't': r['dt'].strftime('%H:%M'),    # время мероприятия
                                     'lang_id': r['lang_id'],           # id языка мероприятия
                                     'status': r['status'],             # статус мероприятия
                                     'city_id': r['city_id'],           # id города мероприятия
                                     'addr': r['addr'],                 # адрес проведения
                                     'map': r['map'],                   # ссылка на карту
                                     'price': r['price'],               # стоимость
                                     'count_min': r['count_min'],       # минимальное количество участников
                                     'count_max': r['count_max'],       # максимальное количество участников
                                     'count_free': r['count_free'],     # количество бесплатных билетов
                                     'count_paid': r['count_paid'],     # количество оплаченных билетов
                                     'report': r['link'],               # ссылка на отчет о мероприятии
                                     'images': event_images(r),         # изображения
                                     'city_def': r['city_def'],         # id города "по-умолчанию"
                                     # дата и город из таблицы состояний. если None, то запись в таблице отсутствует,
                                     # и таким образом мероприятие подобрано по городу "по-умолчанию"
                                     'state_d': r['state_dt'].strftime(DT_FORMAT) if r['state_dt'] else None, 'state_city_id': r['state_city_id'] if r['state_city_id'] else None})

                    return error_resp(ERR_OK, resp)

                except:
                    return error_resp(ERR_DB)

            except:
                return error_resp(ERR_CONNECT)

            finally:
                con.close()

        else:
            return error_resp(ERR_USER_ID)
    else:
        return error_resp(ERR_TOKEN)

# Список билетов заданного пользователя
# <token> -- цифровая подпись Tg-бота
# <uid>   -- id Tg-юзера
# <now>   -- дата "сегодня" в формате ГГГГ-ММ-ДД. Для разных часовых поясов она может быть своя
# <lim>   -- общее количество записей, которое будем возвращать. По-умолчанию "25"
@app.route('/user/tickets', methods=['GET'])
def user_tickets():
    token = request.args.get('token',   type=str)
    uid   = request.args.get('uid',     type=int)
    lim   = request.args.get('lim', 25, type=int)
    now   = request.args.get('now',     type=str)

    if token == TG_TOKEN:
        if uid and now:
            try:
                con = engine.connect()

                try:
                    res = con.execute(text("SELECT `e`.*, UNIX_TIMESTAMP(`e`.`dt`) AS `e_utime`, `t`.`id` AS `tid`, `t`.`tg_id`, `t`.`t_buy`, `t`.`t_refund`, `t`.`status` AS `t_status`, `t`.`t_code`, `t`.`ts`, UNIX_TIMESTAMP(`t`.`ts`) AS `t_utime` FROM `events` AS `e` , `tickets` AS `t` WHERE `t`.`event_id` = `e`.`id` AND `t`.`tg_id` = :i AND DATE(`e`.`dt`) BETWEEN DATE_SUB(:ymd, INTERVAL 1 DAY) AND DATE_ADD(:ymd, INTERVAL :t DAY) ORDER BY `e`.`dt` ASC, `t`.`status` DESC LIMIT :l"), i=uid, ymd=now, t=DT_TICKETS_INTERVAL, l=lim)

                    resp = []

                    for r in res:
                        resp.append(format_ticket(r))

                    return error_resp(ERR_OK, resp)

                except:
                    return error_resp(ERR_DB)

            except:
                return error_resp(ERR_CONNECT)

            finally:
                con.close()

        else:
            return error_resp(ERR_USER_ID)
    else:
        return error_resp(ERR_TOKEN)

# Информация по конкретному мероприятию
# <token> -- цифровая подпись Tg-бота
# <eid>   -- id мероприятия
@app.route('/event', methods=['GET'])
def get_event():
    token = request.args.get('token', type=str)
    eid   = request.args.get('eid',   type=int)

    if token == TG_TOKEN:
        if eid is not None:
            try:
                con = engine.connect()

                try:
                    r = con.execute(text("SELECT *, UNIX_TIMESTAMP(`dt`) AS `utime` FROM `events` WHERE `id` = :i"), i=eid).fetchone()

                    resp = {'eid': r['id'],                   # id мероприятия
                            'title': r['title'],              # название мероприятия
                            'descr': r['descr'],              # краткое описание мероприятия
                            'long_descr': r['long_descr'],    # длинное описание мероприятия
                            'org_id': r['org_id'],            # id организатора
                            'dt': str(r['dt']),               # datetime мероприятия
                            'utime': r['utime'],              # unixtime мероприятия
                            'd': r['dt'].strftime(DT_FORMAT), # дата мероприятия по формату
                            't': r['dt'].strftime('%H:%M'),   # время мероприятия
                            'lang_id': r['lang_id'],          # id языка мероприятия
                            'status': r['status'],            # статус мероприятия. -1: отм., 0: не подтв., 1: подтв.
                            'city_id': r['city_id'],          # id города мероприятия
                            'addr': r['addr'],                # адрес мероприятия
                            'map': r['map'],                  # сслыка на карту места проведения
                            'price': r['price'],              # стоимость мероприятия
                            'count_min': r['count_min'],      # минимальное количество билетов
                            'count_max': r['count_max'],      # максимальное количество билетов
                            'count_free': r['count_free'],    # количество бесплатных билетов
                            'count_paid': r['count_paid'],    # количество оплаченыых билетов
                            'images': event_images(r),        # изображения к событию
                            'report': r['link']} if r else {} # ссылка на репортаж о мероприятий

                    return error_resp(ERR_OK, resp)

                except:
                    return error_resp(ERR_DB)

            except:
                return error_resp(ERR_CONNECT)

            finally:
                con.close()

        else:
            return error_resp(ERR_USER_ID)
    else:
        return error_resp(ERR_TOKEN)

# Информация о конкретном билете
# <token> -- цифровая подпись Tg-бота
# <tid>   -- id билета
@app.route('/ticket', methods=['GET'])
def get_ticket():
    token = request.args.get('token', type=str)
    tid   = request.args.get('tid',   type=int)

    if token == TG_TOKEN:
        if tid is not None:
            try:
                con = engine.connect()
                t = load_ticket(tid, con)

                if t is not None:
                    return error_resp(ERR_OK, t)
                else:
                    return error_resp(ERR_DB)

            except:

                return error_resp(ERR_CONNECT)

            finally:
                con.close()

        else:
            return error_resp(ERR_USER_ID)
    else:
        return error_resp(ERR_TOKEN)

# Добавление билета. В случае успеха возращается инфо о билете
# <token> -- цифровая подпись Tg-бота
# <uid>   -- id Tg-юзера
# <eid>   -- id мероприятия
# <trans> -- транзакция "покупки"
@app.route('/ticket/add', methods=['GET'])
def add_ticket():
    token = request.args.get('token', type=str)
    uid   = request.args.get('uid',   type=int)
    eid   = request.args.get('eid',   type=int)
    tr    = request.args.get('trans', type=str)

    if token == TG_TOKEN:
        if uid is not None and eid is not None and tr is not None:
            try:
                con = engine.connect()
                trans = con.begin()

                try:
                    tid = con.execute(text("INSERT INTO `tickets` (`event_id`, `tg_id`, `t_buy`, `t_code`, `status`) VALUES (:e, :i, :t, CONCAT(LPAD(ROUND(RAND()*1000000), 5, '0'), '-', LPAD(ROUND(RAND()*100000), 5, '0')), 0)"), e=eid, i=uid, t=tr).lastrowid

                    con.execute(text("UPDATE `events` SET `count_paid`=`count_paid`+1 WHERE `id` = :i"), i=eid)

                    trans.commit()

                    t = load_ticket(tid, con)

                    if t is not None:
                        return error_resp(ERR_OK, t)
                    else:
                        return error_resp(ERR_DB)

                except:
                    trans.rollback()
                    return error_resp(ERR_DB)

            except:
                return error_resp(ERR_CONNECT)

            finally:
                con.close()

        else:
            return error_resp(ERR_USER_ID)

    else:
        return error_resp(ERR_TOKEN)

# Возврат билета. В случае успеха возращается инфо о билете
# <token> -- цифровая подпись Tg-бота
# <tid>   -- id билета
# <trans> -- транзакция "рефанда"
@app.route('/ticket/refund', methods=['GET'])
def refund_ticket():
    token = request.args.get('token', type=str)
    tid   = request.args.get('tid',   type=int)
    tr    = request.args.get('trans', type=str)

    if token == TG_TOKEN:
        if tid is not None and tr is not None:
            try:
                con = engine.connect()
                trans = con.begin()

                try:
                    con.execute(text("UPDATE `events` AS `e`, `tickets` AS `t` SET `e`.`count_paid` = `e`.`count_paid` - 1, `t`.`t_refund` = :t, `t`.`status` = -1 WHERE `e`.`id` = `t`.`event_id` AND `t`.`status` = 0 AND `t`.`id` = :i"), t=tr, i=tid)

                    trans.commit()

                    t = load_ticket(tid, con)

                    if t is not None:
                        return error_resp(ERR_OK, t)
                    else:
                        return error_resp(ERR_DB)

                except:
                    trans.rollback()
                    return error_resp(ERR_DB)

            except:
                return error_resp(ERR_CONNECT)

            finally:
                con.close()

        else:
            return error_resp(ERR_USER_ID)

    else:
        return error_resp(ERR_TOKEN)
