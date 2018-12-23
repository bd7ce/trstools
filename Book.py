# -*- coding: utf-8 -*-
from Table import Table

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