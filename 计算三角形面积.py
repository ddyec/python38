
# 输入三条边长
a = float(input("输入三角形第一边长: "))
b = float(input("输入三角形第二边长: "))
c = float(input("输入三角形第三边长: "))
 
#若构成三角形，则求三角形面积
if  a+b>c and b+c>a and a+c>b:                             
    p= (a + b + c) / 2
    area = (p*(p-a)*(p-b)*(p-c)) ** 0.5
    print("三角形面积为：",area)
else:
    print("输入的三条边，不能构成三角形！")

