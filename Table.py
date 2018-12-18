class Table:
    """表格类，一个TRS报表中的单张表
    """
    def __init__(self, name="", id="", bbq=""):
        self.__rows = 0   # 行数（包含文字行）
        self.__cols = 0   # 列数（包含文字行）
        self.__id = id
        self.__bbq = bbq
        self.__name = name

        self.__datastr = ""   # 字符串形式的数据
        self.__data = []   # 数组形式的数据
        self.__areas = 2   # 数据块数量

    def display(self):
        print("Table %s: rows = %s, cols = %s"%(self.__name, self.__rows, self.__cols))

    def __str__(self):
        return self.__datastr

    @property
    def rows(self):
        return self.__rows

    def set_rows(self, rows):
        if 0 < rows < 10000:
            self.__rows = rows
        else:
            self.__rows = 0

    @property
    def cols(self):
        return self.__cols

    def set_cols(self, cols):
        if 0 < cols < 1000:
            self.__cols = cols
        else:
            self.__cols = 0

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def bbq(self):
        return self.__bbq

    @property
    def t1(self):
        return self.__bbq[:4]

    def getdata(cellname):  #根据行列名返回数据
        return 0.00

