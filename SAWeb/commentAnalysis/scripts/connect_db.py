import json
import codecs
import MySQLdb

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



if __name__ == '__main__':
    read_from_db()


"""
db overview:

count(*) : 8398999
number of users whose comment count > 10 : 56209
number of users whose comment count > 30 : 31220
number of users whose comment count > 50 : 22716
number of users whose comment count > 100 :
"""