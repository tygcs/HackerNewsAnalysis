from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
import codecs
import MySQLdb


def test(request):
    content = {"a": 1}
    return render_to_response('test.html', content);


def import_data(dir):
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gghacker', port=3306)
        cur = conn.cursor()

        data = []
        with open(dir) as f:
            for line in f:
                line = line.replace('\'u', '')
                line = line.replace('\n', '')
                line = line.replace('\'', '')
                try:
                    data.append(json.loads(line))
                except:
                    continue

        print len(data)

        for item in data:
            try:
                idint = int(item['id'])
            except KeyError as e:
                idint = 0
            try:
                parentint = int(item['parent'])
            except KeyError as e:
                parentint = 0
            try:
                rankingint = int(item['ranking'])
            except KeyError as e:
                rankingint = 0
            try:
                byw = item['by']
            except KeyError as e:
                byw = ""
            try:
                author = item['author']
            except KeyError as e:
                author = ""
            try:
                timems = item['time']
            except KeyError as e:
                timems = ""
            try:
                timesp = item['time_ts']
            except KeyError as e:
                timesp = ""
            try:
                textcon = item['text']
                textcon = textcon.replace('\\', '')

            except KeyError as e:
                textcon = ""
            try:
                deleted = item['dead']
            except KeyError as e:
                deleted = True
            # print item

            sql = "insert into comtab(id, byw, timems, timesp, textcon, parent, dead, ranking, author) VALUES "
            sql = sql + "('%d','%s','%s','%s','%s','%d','%d','%d','%s');" % \
                        (idint, byw, timems, timesp, textcon, parentint, deleted, rankingint, author)

            try:
                cur.execute(sql)
            except:
                print "pass one line"
                continue
            try:
                conn.commit()
            except MySQLdb.Error, e:
                print "ERROR: ", e
                print "sql: ", sql

        cur.close()
        conn.close()

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    print "success"


def read_from_db():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gghacker', port=3306)
    cur = conn.cursor()

    sql = 'select * from comtab'
    # sql = "update comtab set seti_score=%s where byw = %d;" % (seti_score, byw)

    count = cur.execute(sql)
    datas = cur.fetchall()
    for x in datas:
        print x, type(x), x[0], x[1]
    print "count: ", count

    try:
        conn.commit()
    except MySQLdb.Error, e:
        print "ERROR: ", e
        print "sql: ", sql

    conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':
    for i in range(2, 32):
        dir = '/Users/ty/codes/gg_hackathon/data/comments/comments_0000000000' + ('0' if i < 10 else '') + str(i)
        print "current on: ", dir
        import_data(dir)
