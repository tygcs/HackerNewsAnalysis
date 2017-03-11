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
                section_seti_avg[d] = section_seti_avg[d] + float(x['seti_score'])
                break

    for d in range(100):
        section_seti_avg[d] = (section_seti_avg[d] / section_comt_cnt[d]) if section_seti_avg[d] else 0


    data = {}
    data['name'] = "Correlation between Comments' length and Users' Sentiment"
    data['unit'] = unit
    data['section_start'] = sections_start
    data['section_comt_cnt'] = section_comt_cnt
    data['section_seti_avg'] = section_seti_avg

    cur.close()
    conn.close()

    # mock data
    # data = {'section_start': [0, 567, 1134, 1701, 2268, 2835, 3402, 3969, 4536, 5103, 5670, 6237, 6804, 7371, 7938, 8505, 9072, 9639, 10206, 10773, 11340, 11907, 12474, 13041, 13608, 14175, 14742, 15309, 15876, 16443, 17010, 17577, 18144, 18711, 19278, 19845, 20412, 20979, 21546, 22113, 22680, 23247, 23814, 24381, 24948, 25515, 26082, 26649, 27216, 27783, 28350, 28917, 29484, 30051, 30618, 31185, 31752, 32319, 32886, 33453, 34020, 34587, 35154, 35721, 36288, 36855, 37422, 37989, 38556, 39123, 39690, 40257, 40824, 41391, 41958, 42525, 43092, 43659, 44226, 44793, 45360, 45927, 46494, 47061, 47628, 48195, 48762, 49329, 49896, 50463, 51030, 51597, 52164, 52731, 53298, 53865, 54432, 54999, 55566, 56133], 'section_seti_avg': [0.5239945136214138, 0.49972555121874945, 0.4182666098515782, 0.4831479444702801, 0.316675808983, 0.627622041134, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'name': 'comment length and setiscore', 'unit': 567, 'section_comt_cnt': [403, 71, 23, 5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


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
        section_start[d] = float("%.1f" % (float(section_start[d - 1]) + float(unit)))

    # compute avg by comment seti_score
    sql = "select timems, seti_score from comtab_small;"  # data since 2015-01-01
    # sql = "select timems, seti_score from comtab where STRCMP(timems, '1420141743') >= 0;"

    count = cur.execute(sql)  # number of items Mysql returned
    datas = cur.fetchallDict()  # x in datas is dict which contains {"textcon": 'xxx', "ranking": 'x', ...}
    for x in datas:
        # print x['timems'], x['seti_score']
        for d in range(5):
            if float(x['seti_score']) >= section_start[d] and float(x['seti_score']) < section_start[d] + unit:
                section_avg_by_comment[d] = section_avg_by_comment[d] + 1
                break

    for d in range(5):
        reader_seti_all = reader_seti_all + section_avg_by_comment[d]
    for d in range(5):
        section_avg_by_comment[d] = (section_avg_by_comment[d] * 1.0 / reader_seti_all) if reader_seti_all else 0


    # compute avg by user seti_score
    sql = "select count(*), sum(seti_score),byw from comtab_small group by byw having count(*)>1;"  # data since 2015-01-01
    # sql = "select count(*), sum(seti_score), byw from comtab where STRCMP(timems, '1420141743') >= 0 group by byw having count(*)>1;"

    count = cur.execute(sql)  # number of items Mysql returned
    datas = cur.fetchallDict()

    for x in datas:
        avg_score = float(x['sum(seti_score)']) / float(x['count(*)'])
        for d in range(5):
            if avg_score >= section_start[d] and avg_score < section_start[d] + unit:
                section_avg_by_user[d] = section_avg_by_user[d] + 1
                break

    reader_seti_all = 0
    for d in range(5):
        reader_seti_all = reader_seti_all + section_avg_by_user[d]
    for d in range(5):
        section_avg_by_user[d] = (section_avg_by_user[d] * 1.0 / reader_seti_all) if reader_seti_all else 0

    data = {}
    data['name'] = 'Emotional distribution'
    data['unit'] = unit
    data['section_start'] = section_start
    data['section_avg_by_comment'] = section_avg_by_comment
    data['section_avg_by_user'] = section_avg_by_user

    cur.close()
    conn.close()

    # mock data
    # data = {'section_avg_by_comment': [0.20833333333333334, 0.1746031746031746, 0.1765873015873016, 0.2261904761904762, 0.21428571428571427], 'section_start': [0, 0.2, 0.4, 0.6, 0.8], 'name': 'Emotional distribution', 'unit': 0.2, 'section_avg_by_user': [0.03225806451612903, 0.1935483870967742, 0.5, 0.24193548387096775, 0.03225806451612903]}
    return data


def getdata_single_user_seti_distribution():

    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gghacker', port=3306)
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    # todo
    sql = "select count(*), sum(seti_score),byw from comtab_small where byw = 'bd';"
    # sql = "select timems, seti_score from comtab where STRCMP(timems, '1420141743') >= 0;"

    count = cur.execute(sql)  # number of items Mysql returned
    datas = cur.fetchallDict()  # x in datas is dict which contains {"textcon": 'xxx', "ranking": 'x', ...}

    section_start = [0] * 5
    section_comt_counts = [0] * 5
    unit = 0.2
    section_start[1] = unit
    for d in range(2, 5):
        section_start[d] = float("%.1f" % (float(section_start[d - 1]) + float(unit)))



    data = {}
    data['name'] = "Sentiment Distribution Based on Single User's History"
    data['unit'] = unit
    data['section_start'] = section_start
    data['section_comt_counts'] = section_comt_counts

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

    return render_to_response('singer_user.html', content)


def commentlength_and_setiscore(request):

    content = getdata_commentlength_and_setiscore()

    return render_to_response('test.html', content)


def score_and_setiscore(request):

    content = {}

    return render_to_response('score.html', content)


def about(request):

    content = {}

    return render_to_response('our_team.html', content)


def index(request):
    content = {}
    return render_to_response('index.html', content)


def test(request):

    content = getdata_commentlength_and_setiscore()

    return render_to_response('test.html', content)


if __name__ == '__main__':
    getdata_commentlength_and_setiscore()
