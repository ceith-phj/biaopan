import tkinter as tk
from turtle import *
from datetime import datetime

mode("logo")

class Clock(object):
    def __init__(self):
        # 创建窗体
        self.second_hand = Turtle()
        self.minute_hand = Turtle()
        self.hour_hand = Turtle()
        self.writer = Turtle()
        self.writer.getscreen().bgcolor("gray90")
        self.writer.color("gray20", "gray20")

        self.thisday = None
        self.thissecond = None

        tracer(False)# 隐藏绘图
        self.setup()
        tracer(False) # 重新打开
        self.tick()

        mainloop()

    def jump(self, distanz, winkel=0):
        penup()
        right(winkel)
        forward(distanz)
        left(winkel)
        pendown()


    # laenge: 指针长度 width: 指针宽度 spitze: 箭头边长
    def hand(self, laenge, spitze, width):
        lt(90)
        fd(width)
        rt(90)
        fd(laenge * 1.15)
        rt(90)
        fd(width * 2)
        rt(90)
        fd(laenge * 1.15)
        rt(90)
        fd(width)
        rt(90)
        fd(laenge * 1.15)
        rt(90)
        fd(spitze / 2.0)
        lt(120)
        fd(spitze)
        lt(120)
        fd(spitze)
        lt(120)
        fd(spitze / 2.0)

    def make_hand_shape(self, name, laenge, spitze, width):
        reset()
        self.jump(-laenge * 0.15)  # 指针靠近表盘中心的末端，但不与圆心重合
        begin_poly()
        self.hand(laenge, spitze, width)
        end_poly()
        hand_form = get_poly()
        register_shape(name, hand_form)

    # 表盘
    def clockface(self, radius):
        reset()
        # 外圆周
        pensize(1) # 画笔大小
        #colors = ['green3', 'green2', 'gray98']
        colors = ['pink1', 'pink1', 'pink1']
        # 从外向内fill
        for i in range(3):
            self.jump(radius + 7 + (2 - i) * 4, 90)
            fillcolor(colors[i])
            begin_fill()
            circle(radius + 7 + (2 - i) * 4, steps=1000)
            end_fill()
            self.jump(-radius - 7 - (2 - i) * 4, 90)
        # 刻度
        pensize(10) # 画笔大小
        colors = ["gray60", "gray60"]
        # 经验值
        params = [-35, -40, -40, -25, -15, -5, 0, -5, -15, -25, -40, -40]  # 距离
        angles = [0, -15, -25, -40, -35, -30, 0, 30, 35, 40, 25, 15]  # 角度
        for i in range(60):
            self.jump(radius)
            if i % 5 == 0:
                fd(-1)# 大刻度点1
                # 下面三行写表盘数字
                self.jump(params[i//5], angles[i//5])
                write(12 if i//5 == 0 else i//5, align="center", font=("Courier", 20, "bold"))
                self.jump(params[i//5], 180 + angles[i//5])
                self.jump(-radius + 1)#大刻度点1数字一样
            else:
                dot(5)  # 表盘点大小
                self.jump(-radius)
            rt(6)

    def setup(self):
        # 自定义形状
        self.make_hand_shape("hour_hand", 90, 14, 2)
        self.make_hand_shape("minute_hand", 115, 12, 1.6)
        self.make_hand_shape("second_hand", 140, 10, 1.2)

        # 画表盘
        self.clockface(160)

        self.hour_hand.shape("hour_hand")
        self.hour_hand.color("gray30", "black")

        self.minute_hand.shape("minute_hand")
        self.minute_hand.color("gray40", "blue")

        self.second_hand.shape("second_hand")
        self.second_hand.color("red4", "red4")

        for hand in self.hour_hand, self.minute_hand, self.second_hand:
            hand.resizemode("user")
            hand.shapesize(1, 1, 1)
            hand.speed(1)
        ht()

        self.writer.ht()
        self.writer.pu()
        self.writer.bk(85)

    def wochentag(self, t):
        wochentag = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        return wochentag[t.weekday()]


    def get_mmdd(self, z):
        m = z.month
        t = z.day
        return "%d月%d日" % (m, t)

    def get_yyyy(self, z):
        j = z.year
        return "%d" % (j)

    #星期和日期
    def write_date(self, t):
        x = t.day
        if self.thisday != x:
            thisday = x
            self.writer.clear()
            self.writer.home()
            self.writer.forward(65)
            self.writer.write(self.wochentag(t), align="center",
                              font=("Courier", 16, "bold"))
            self.writer.back(150)
            self.writer.write(self.get_mmdd(t), align="center",
                              font=("Courier", 16, "normal"))
            self.writer.back(15)
            self.writer.write(self.get_yyyy(t), align="center",
                              font=("Courier", 12, "normal"))
            self.writer.forward(100)

    def tick(self):
        t = datetime.today()
        if self.thissecond != t.second:
            self.thissecond = t.second

            # print t
            sekunde = t.second + t.microsecond * 0.000001
            minute = t.minute + sekunde / 60.0
            stunde = t.hour + minute / 60.0
            tracer(False)
            self.write_date(t)
            tracer(True)
            self.hour_hand.setheading(30 * stunde)
            self.minute_hand.setheading(6 * minute)
            self.second_hand.setheading(6 * sekunde)
        ontimer(self.tick, 10)  # 安装定时器 10ms后执行


if __name__ == '__main__':
    # 实例化对象
    clock = Clock()
