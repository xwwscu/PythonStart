#!/usr/bin/python
a = eval(input("请输入数字:"))
print("input number: ", a, "type: ", type(a))
b = eval(input("请输入数字:"))
print('input another number: ', b, 'type:', type(b))

def getMax(a, b):
    "find max value"
    if a>=b:
        return a
    else:
        return b
print("input max value:", getMax(a, b))

if (type(a) == int and type(b) == int):
    print('a+b=', (a + b))
elif (type(a) == float and type(b) == float):
    print('a+b-->', (a + b))
else:
    print('not suport format:', a, b)

