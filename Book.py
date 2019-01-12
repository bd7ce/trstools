# -*- coding: utf-8 -*-
from Table import Table
import pymysql

# 类---TRS任务，相当于excel的工作簿
class Book:
    def __init__(self):
        self.__tablenum = 0
        self.__tables = []
        self.__id = ""
        self.__name = ""
        self.__bbq = ""

    @property
    def id(self):
        return self.__id

    @property
    def bbq(self):
        return self.__bbq

    @property
    def t1(self):
        return int(self.__bbq[0:4])

    @property
    def t2(self):
        return int(self.__bbq[4:6])

    @property
    def t3(self):
        try:
            day = int(self.__bbq[6:])
        except ValueError:
            return -1
        else:
            return day

    @property
    def tables(self):
        return self.__tables

    def gettablebynum(self, tn):
        if tn < self.__tablenum:
            return self.__tables[tn]

    def gettablebyname(self, tn):
        for tt in self.__tables:
            if tt.name == tn:
                return tt

    def readfromtxt(self, filename):  # 从TXT文件读入数据
        try:
            with open(filename, "r") as fn:
                lines = fn.readline().strip("\n")
                t = lines.split("=")
                self.__id = t[1]

                lines = fn.readline().strip("\n")
                t = lines.split("=")
                self.__name = t[1]

                lines = fn.readline().strip("\n")
                t = lines.split("=")
                self.__bbq = t[1]

                lines = fn.readline()  # upid
                lines = fn.readline()  # btype
                lines = fn.readline()  # blank

                while True:
                    lines = fn.readline().strip("\n")
                    if not lines:
                        break
                        pass

                    if lines[-1:] == ",":
                        lines = lines.strip(",")

                    tmp = lines.partition(":")
                    for tt in self.__tables:
                        if tt.name == tmp[0]:
                            tt.set_datastr(tmp[2])
        except IOError:
            print("File Error")
        finally:
            fn.close()

    def readpara(self):  #读入参数表，确定数据块
        fn = open("params/paras.txt")
        for line in fn.readlines():
            line = line.strip("\n")
            p = line.partition("=")  # 表名=左下角;左上1:右下1，左上2:右下2...
            if len(p) == 3:
                tt = Table()
                tt.set_name(p[0])

                q = p[2].partition(";")  #每个表有两个参数：最大行列；数据块1，2，3...
                tt.set_rc(int(q[0][1:]), ord(q[0][:1])-64)
                tt.set_keystr(q[2])

                self.__tables.append(tt)
                self.__tablenum += 1

    # 审核公式： C3 > D4, [C3:C8] > [D3:D8]
    # [C3:U3] > SUM([C4:U4]:[C6:U6]) ==> C3 > SUM(C4:C6) .. D3 > SUM(D4:D6)
    # [C3:U4] + [C8:U8] > ...
    # IF 函数 if(a,b,c)  -- 不实现
    # SUM 函数 sum(a,b,c,d)  => sum((a,b,c,d))转换成元组
    # 逻辑组合 （a=b)|(c=d)&(e=f)  -- 不实现
    # 返回：公式，提示，左边，右边, 逻辑， 数组
    # 数组公式标志： []
    # TRS公式与python相差较大，为利用eval函数，不考虑直接实现TRS的全部公式，而是改用python的语法
    def audit(self, formulas):
        for f in formulas:
            return eval(f)

    def getconn():
        return pymysql.connect(host="localhost", user="rpt", password="rpt", database="trsdata")

    def savedb(self):
        conn = self.getconn()
        items = []
        cur = conn.cursor()
        try:
            cur.executemany("insert into rptdata (bbq,dw,tname,cname,pval) values ('','','',%s,%s)", items)
            assert cur.rowcount == len(items), "Insert error"
            conn.commit()
        except:
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def readdb(self):
        conn = self.getconn()
        cur = conn.cursor()
        rows = cur.execute("select * from rptdata")
