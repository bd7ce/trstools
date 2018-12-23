# -*- coding: utf-8 -*-
from Book import Book

b = Book()
b.readpara()
b.readfromtxt("testdata/KT19010220000.txt")
print(b.bbq)

t2 = b.gettablebyname("SJ_01")
t2.display()
print(t2.name)
print(t2.getdata("C3"))
