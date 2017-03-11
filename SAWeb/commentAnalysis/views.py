from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
import codecs
import MySQLdb


def getdata_commentlength_and_setiscore():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gghacker', port=3306)
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    sections_start = [0] * 100
    section_comt_cnt = [0] * 100
    section_seti_avg = [0] * 100
    unit = 567  # length of one section
    sections_start[1] = unit
    for d in range(2, 100):
        sections_start[d] = sections_start[d-1] + unit

    sql = "select LENGTH(textcon), seti_score from comtab_small; "
    # sql = "select LENGTH(textcon), seti_score from comtab where STRCMP(timems, '1420141743') >= 0;"

    count = cur.execute(sql)
    datas = cur.fetchallDict()

    for x in datas:
        # print x['LENGTH(textcon)'], x['seti_score']
        for d in range(100):
            if x['LENGTH(textcon)'] >= sections_start[d] and x['LENGTH(textcon)'] < sections_start[d] + unit:
                section_comt_cnt[d] = section_comt_cnt[d] + 1
                section_seti_avg[d] = section_seti_avg[d] + x['LENGTH(textcon)']
                break

    for d in range(100):
        section_seti_avg[d] = (section_seti_avg[d] / section_comt_cnt[d]) if section_seti_avg[d] else 0


    data = {}
    data['name'] = 'comment length and setiscore'
    data['unit'] = unit
    data['section_start'] = sections_start
    data['section_comt_cnt'] = section_comt_cnt
    data['section_seti_avg'] = section_seti_avg

    cur.close()
    conn.close()

    return data


def getdata_all_user_seti_distribution():

    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gghacker', port=3306)
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    section_start = [0] * 5
    section_avg_by_comment = [0] * 5
    section_avg_by_user = [0] * 5
    reader_seti_all = 0
    unit = 0.2  # length of one section
    section_start[1] = unit
    for d in range(2, 5):
        section_start[d] = section_start[d - 1] + unit


    # compute avg by comment seti_score
    sql = "select timems, seti_score from comtab_small where STRCMP(timems, '1420141743') >= 0;"  # data since 2015-01-01
    # sql = "select timems, seti_score from comtab where STRCMP(timems, '1420141743') >= 0;"

    count = cur.execute(sql)  # number of items Mysql returned
    datas = cur.fetchallDict()  # x in datas is dict which contains {"textcon": 'xxx', "ranking": 'x', ...}
    for x in datas:
        # print x['timems'], x['seti_score']
        for d in range(5):
            if x['seti_score'] >= section_start[d] and x['seti_score'] < section_start[d] + unit:
                section_avg_by_comment[d] = section_avg_by_comment[d] + 1
                break

    for d in range(5):
        reader_seti_all = reader_seti_all + section_avg_by_comment[d]
    for d in range(5):
        section_avg_by_comment[d] = (section_avg_by_comment[d] * 1.0 / reader_seti_all) if reader_seti_all else 0


    # compute avg by user seti_score
    sql = "select timems, seti_score from comtab_small where STRCMP(timems, '1420141743') >= 0;"  # data since 2015-01-01
    # sql = "select timems, seti_score from comtab where STRCMP(timems, '1420141743') >= 0;"

    count = cur.execute(sql)  # number of items Mysql returned
    datas = cur.fetchallDict()


    data = {}
    data['name'] = 'Emotional distribution'
    data['unit'] = unit
    data['section_start'] = section_start
    data['section_avg_by_score'] = section_avg_by_comment
    data['section_avg_by_user'] = section_avg_by_user

    cur.close()
    conn.close()

    return data


def getdata_single_user_seti_distribution():

    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gghacker', port=3306)
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    sql = "select timems, seti_score from comtab_small where STRCMP(timems, '1420141743') >= 0;" # data since 2015-01-01
    # sql = "select timems, seti_score from comtab where STRCMP(timems, '1420141743') >= 0;"

    count = cur.execute(sql)  # number of items Mysql returned
    datas = cur.fetchallDict()  # x in datas is dict which contains {"textcon": 'xxx', "ranking": 'x', ...}

    data = {}
    data['name'] = 'comment length and setiscore'

    cur.close()
    conn.close()

    return data


def update_db(id, seti_value):
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gghacker', port=3306)
    cur = conn.cursor()

    sql = "update comtab set seti_score=%s where id = %d;" % (str(seti_value), id)

    cur.execute(sql)

    # conn.commit()
    cur.close()
    conn.close()


def all_user_seti_distribution(request):

    content = getdata_all_user_seti_distribution()

    return render_to_response('all_users.html', content)


def single_user_seti_distribution(request):

    content = {}

    return render_to_response('singleuser.html', content)


def commentlength_and_setiscore(request):

    content = getdata_commentlength_and_setiscore()

    return render_to_response('test.html', content)


def score_and_setiscore(request):

    content = {}

    return render_to_response('score.html', content)


def index(request):
    content = {}
    return render_to_response('index.html', content)


def test(request):

    content = getdata_commentlength_and_setiscore()

    return render_to_response('test.html', content)


if __name__ == '__main__':
    getdata_commentlength_and_setiscore()
