#输入三角形的三边长
a=float(input('输入三角形第一边长： '))
b=float(input('输入三角形第二边长： '))
c=float(input('输入三角形第三边长： '))
p=(a+b+c)/2   #计算三角形的半周长
s=(p*(p-a)*(p-b)*(p-c))**0.5 #计算三角形的面积
print('三角形面积为：',s) #输出三角形的面积
