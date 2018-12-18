class Table:
    """表格类，一个TRS报表中的单张表
    """
    def __init__(self, name=""):
        self.__rows = 0   # 行数（包含文字行）
        self.__cols = 0   # 列数（包含文字行）
        self.__keystr = ""
        self.__keys = []
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

    @property
    def keystr(self):
        return self.__keystr

    def set_keystr(self, keystr):
        self.__keystr = keystr
        if "," in keystr:  # 多区域
            k = keystr.split(",")
            for area in k:
                pass

    @staticmethod
    def get_keys(keys):
        for k in keys.split(":"):
            pass

    @staticmethod
    def c2n(self, colname):  # 字符列号转为数字号，从1开始
        ch = colname.upper()

        if len(ch) == 1:    # TRS的列号限制不能超过Z
            return ord(ch) - 64
        else:
            return -1

    @staticmethod
    def lab2rc(self, lab):  # 名称转换为行列号
        if len(lab) > 1:
            return self.c2n(lab[:1]), int(lab[1:])
        else:
            return -1, -1

    #def area(self, alabel):
        #for i in
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
    def getdata(cellname):  #根据行列名返回数据
        return 0.00

