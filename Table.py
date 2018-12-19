# -*- coding: utf-8 -*-
# 类---TRS报表

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

    def display(self):
        print("Table %s: rows = %s, cols = %s"%(self.__name, self.__rows, self.__cols))

    def __str__(self):
        result = ""

        for key in self.__data:
            result = result + key + ":" + self.__data[key] + ","
        return result

    @property
    def rows(self):
        return self.__rows

    def set_rows(self, rows):
        if 0 < rows < 1000:
            self.__rows = rows
        else:
            self.__rows = 0

    @property
    def cols(self):
        return self.__cols

    def set_cols(self, cols):
        if 0 < cols <= 26:  # 不能超过26列（A-Z)
            self.__cols = cols
        else:
            self.__cols = 0

    @property
    def name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    @property
    def datastr(self):
        return self.__datastr

    def set_datastr(self, datastr):
        if len(datastr) > 1 and "," in datastr:
            self.__datastr = datastr
            i = 0
            datas = self.__datastr.split(",")

            for r in range(1, self.__rows+1):
                for c in range(1, self.__cols+1):
                    if self.in_area(c, r):
                        self.__data[chr(c + 64) + str(r)]=datas[i]
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
    def c2n(colname):  # 字符列号转为数字号，从1开始
        ch = colname.upper()

        if len(ch) == 1:    # TRS的列号限制不能超过Z
            return ord(ch) - 64
        else:
            return -1

    @staticmethod
    def lab2rc(lab):  # 名称转换为行列号
        cname = lab.upper()
        if len(lab) > 1:
            return ord(cname[:1]) - 64, int(cname[1:])
        else:
            return -1, -1

    """
    表有行列大小，如 SJ_01 有 14行7列， A1：G14
    有两个数据块C3:D14和F3:G7
    产生的TXT上报数据格式：从左到右，从上到下，跳过非数据块
    几种形式表示：
    C3 -- 单元格
    C3:D14 -- 数据块
    SJ_02->C3  -- 跨表数据
    @-12SJ_01->C3  -- 跨报表期数据
    """
    def getdata(self, cellname):  #根据行列名返回数据
        if ":" in cellname: # 数组
            pass
        elif "->" in cellname:  # 表间
            pass
        elif "@" in cellname:  # 期间
            pass
        else:  #直接
            return float(self.__data[cellname])

    # 审核公式： C3 > D4, [C3:C8] > [D3:D8]
    def audit(self, formula):
        if "=" in formula:
            p = formula.partition("=")
            left = p[0]
            right = p[2]