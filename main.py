# -*- coding: utf-8 -*-

from Table import Table
from Book import Book

b = Book()
b.readpara()
print(b.tables[0].in_area("F7"))

b.readfromtxt("KT19010220000.txt")
print(b.bbq)

t2 = b.gettablebyname("SJ_03")
print(t2.name)
print(t2.datastr)

tt = b.gettablebynum(1)
print(tt.name)
print(tt.datastr)
