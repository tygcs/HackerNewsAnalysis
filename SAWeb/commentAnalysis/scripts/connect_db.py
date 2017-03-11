import json
import codecs
import MySQLdb


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


def import_data_main():
    for i in range(2, 32):
        dir = '/Users/ty/codes/gg_hackathon/data/comments/comments_0000000000' + ('0' if i < 10 else '') + str(i)
        print "current on: ", dir
        import_data(dir)


def read_from_db():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gghacker', port=3306)
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    sql = "select * from comtab where byw = 'js2'; "
    # sql = "update comtab set seti_score=%s where byw = %d;" % (seti_score, byw)

    count = cur.execute(sql)
    datas = cur.fetchallDict() # datas is a tuple
    # datas = cur.fetchoneDict()
    print type(datas)
    for x in datas[:5]:  # x in datas is dict which contains {"textcon": 'xxx', "ranking": 'x', ...}
        print x['ranking'], x['seti_score'], type(x)  # if null in MySQL, x['xxx'] = None
    print "count: ", count

    # conn.commit()
    cur.close()
    conn.close()


def write_id_comt_file():
    """
    :return: generate json file {'id': xxx, 'textcon': xxx}
    """
    dir = '/Users/ty/codes/gg_hackathon/data/comment_small/' + 'comment1'

    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='gghacker', port=3306)
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    sql = 'select id, textcon from comtab limit 10; '
    cur.execute(sql)
    datas = cur.fetchallDict()

    f = open(dir, "w+")

    for data in datas:
        f.write(json.dumps(data))
        f.write('\n')

    f.close()
    cur.close()
    conn.close()


def read_file(dir=""):
    if dir == "":
        dir = '/Users/ty/codes/gg_hackathon/data/comment_small/comment1'

    f = open(dir, 'r')
    for line in f.readlines():
        print line, type(line) # str
    f.close()

if __name__ == '__main__':
    read_file()


"""
db overview:

count(*) : 8398999
count(x) where textcon != null : 8170810
number of users whose comment count > 10 : 56209
number of users whose comment count > 30 : 31220
number of users whose comment count > 50 : 22716
number of users whose comment count > 100 : 14033
"""