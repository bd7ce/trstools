# -*- coding: utf-8 -*-
# 类---TRS报表
import numpy as np
import pandas as pd

class Table:
    """表格类，一个TRS报表中的单张表
    """
    def __init__(self, name=""):
        self.__rows = 0   # 行数（包含文字行）
        self.__cols = 0   # 列数（包含文字行）
        self.__keystr = ""# 数据区域字符串，以句号隔开，如："C3:D4,F3:G4"
        self.__keys = []  # 数据区域列表（1或多个）
        self.__cells = [] # 所有的数据标签
        self.__name = name

        self.__datastr = ""   # 字符串形式的数据
        self.__data = {}   # 字典形式的数据
        #self.__df = pd.DataFrame()  # dataframe形式的数据,在读取时初始化，此处留空

    def display(self):
        print("Table %s: rows = %s, cols = %s\n"%(self.__name, self.__rows, self.__cols))
        print(self.__df)

    def __str__(self):
        result = ""

        for key in self.__data:
            result = result + key + ":" + self.__data[key] + ","
        return result

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    def set_rc(self, rows, cols):
        if (0 < rows < 1000) and (0 < cols <= 26):  # TRS限定26列1000行
            self.__rows = rows
            self.__cols = cols
            cs = []
            for c in range(0, cols):      # 列号从A开始，非数据部分为NaN
                cs.append(chr(65 + c))
            rs = []
            for r in range(1, rows + 1):  # 行号从1开始
                rs.append(r)
            self.__df = pd.DataFrame(index = rs, columns = cs, dtype=float)
        else:
            self.__rows = 0
            self.__cols = 0

    @property
    def name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    @property
    def datastr(self):
        return self.__datastr

    def set_datastr(self, datastr):  # df 数据集的表示： c3 ==> __df['C'][3]
        if len(datastr) > 1 and "," in datastr:
            self.__datastr = datastr
            i = 0
            datas = self.__datastr.split(",")

            for r in range(1, self.__rows+1):
                for c in range(1, self.__cols+1):
                    if self.in_area(c, r):
                        self.__data[chr(c + 64) + str(r)]=datas[i]
                        self.__df[chr(c + 64)][r] = self.safefloat(datas[i])
                        i += 1
    @property
    def keystr(self):
        return self.__keystr

    def set_keystr(self, keystr):  #设置数据区域
        self.__keystr = keystr
        self.__keys = keystr.split(",")
        for key in self.__keys:
            p = key.partition(":")
            leftop = self.lab2rc(p[0])
            rightb = self.lab2rc(p[2])
            for r in range(leftop[1], rightb[1]+1):
                for c in range(leftop[0], rightb[0]+1):
                    self.__cells.append(chr(c) + str(r))
        self.__data.fromkeys(self.__cells,0.00)

    def in_area(self, x, y=0):  #判断单元格是否在数字区域, C3 in_area C3:D4, C2 not in_area C3:D4
        if y == 0:
            c = self.lab2rc(x)  #以默认参数重载该函数。 单参数为"C3"字符串形式，双参数为 x,y形式
        else:
            c = (x, y)
        result = False

        for key in self.__keys:
            p = key.partition(":")
            leftop = self.lab2rc(p[0])
            rightb = self.lab2rc(p[2])
            result = result or ((leftop[0] <= c[0] <= rightb[0]) and (leftop[1] <= c[1] <= rightb[1]))

        return result

    @staticmethod
    def c2n(colname):  # 字符列号转为数字号，从1开始 c ==> 3
        ch = colname.upper()

        if len(ch) == 1:    # TRS的列号限制不能超过Z
            return ord(ch) - 64
        else:
            return -1

    @staticmethod
    def lab2rc(lab):  # 名称转换为行列号 C3 ==> 3, 3
        cname = lab.upper()
        if len(lab) > 1:
            return ord(cname[:1]) - 64, int(cname[1:])
        else:
            return -1, -1

    @staticmethod
    def safefloat(s):  # 字符串转浮点数
        try:
            a = float(s)
        except:
            a = np.NaN
        finally:
            return a

    """
    表有行列大小，如 SJ_01 有 14行7列， A1：G14
    有两个数据块C3:D14和F3:G7
    产生的TXT上报数据格式：从左到右，从上到下，跳过非数据块
    几种形式表示：
    C3 -- 单元格
    c3+c4+c5  -- 连加公式
    sum(c3,c5,C7:D14) -- sum函数
    SJ_02->C3  -- 跨表数据
    @-1C3  -- 跨报表期
    @-12SJ_01->C3  -- 跨报表期跨表数据
    """
    def getdata(self, cellname):  #计算公式，根据行列名返回数据
        cn = cellname.upper()
        if ":" in cn: # 数组, A1:B4 ==> __df.loc[1:4,'A':'B']
            pass
        elif "->" in cn:  # 表间
            pass
        elif "@" in cn:  # 期间
            pass
        else:  #直接
            return self.safefloat(self.__data[cn])

    # 审核公式： C3 > D4, [C3:C8] > [D3:D8]
    def audit(self, formula):
        if "=" in formula:
            p = formula.partition("=")
            left = p[0]
            right = p[2]