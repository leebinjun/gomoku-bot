#! /usr/bin/env python3  
# -*- coding: utf-8 -*-  
import sys


def print_all(module_):
    modulelist = dir(module_)
    length = len(modulelist)
    for i in range(0,length,1):
        print(getattr(module_,modulelist[i]))


'''
Python多线程详解 - monster_ygs - 博客园 https://www.cnblogs.com/monsteryang/p/6592385.html
'''

'''
# encoding: UTF-8
import threading

# print_all(threading)


# 方法1：将要执行的方法作为参数传给Thread的构造方法
def func():
    print('func() passed to Thread')

t = threading.Thread(target=func)
t.start()
print(threading.currentThread())
print(threading.enumerate())
print(threading.activeCount())


# 方法2：从Thread继承，并重写run()
class MyThread(threading.Thread):
    def run(self):
        print('MyThread extended from Thread')

t = MyThread()
t.start()




# encoding: UTF-8
import threading
import time

def context(tJoin):
    print  ('in threadContext.')
    tJoin.start()
    # 将阻塞tContext直到threadJoin终止。
    tJoin.join()
    # tJoin终止后继续执行。
    print ('out threadContext.   1')

    # tJoin.start()
    # tJoin.join()
    # print ('out threadContext.   2')
    # RuntimeError: threads can only be started once



def join():
    print ('in threadJoin.')
    time.sleep(1)
    print ('out threadJoin.')

# tJoin和tContext分别为两个不同的线程
tJoin = threading.Thread(target=join)
tContext = threading.Thread(target=context, args=(tJoin,))

tContext.start()


# encoding: UTF-8
import threading
import time

data = 0
lock = threading.Lock()

def func():
    global data
    print(data)
    print ('%s acquire lock...' % threading.currentThread().getName())

    # 调用acquire([timeout])时，线程将一直阻塞，
    # 直到获得锁定或者直到timeout秒后（timeout参数可选）。
    # 返回是否获得锁。
    if lock.acquire():
        print ('%s get the lock.' % threading.currentThread().getName())
        data += 1
        time.sleep(5)
        print ('%s release lock...' % threading.currentThread().getName())

        # 调用release()将释放锁。
        lock.release()

    print(data)

t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t3 = threading.Thread(target=func)
t1.start()
t2.start()
t3.start()
'''

'''
# encoding: UTF-8
import threading
import time

rlock = threading.RLock()

def func():
    # 第一次请求锁定
    print ('%s acquire lock...' % threading.currentThread().getName())
    if rlock.acquire():
        print ('%s get the lock.' % threading.currentThread().getName())
        time.sleep(2)

        # 第二次请求锁定
        print ('%s acquire lock again...' % threading.currentThread().getName())
        if rlock.acquire():
            print ('%s get the lock.' % threading.currentThread().getName())
            time.sleep(2)

        # 第一次释放锁
        print ('%s release lock...' % threading.currentThread().getName())
        rlock.release()
        time.sleep(2)

        # 第二次释放锁
        print ('%s release lock...' % threading.currentThread().getName())
        rlock.release()

t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t3 = threading.Thread(target=func)
t1.start()
t2.start()
t3.start()
'''

'''

# encoding: UTF-8
import threading
import time

# 商品
product = None
# 条件变量
con = threading.Condition()

# 生产者方法
def produce():
    global product

    if con.acquire():
        while True:
            if product is None:
                print('produce...')
                product = 'anything'

                # 通知消费者，商品已经生产
                con.notify()

            # 等待通知
            con.wait()
            time.sleep(2)

# 消费者方法
def consume():
    global product

    if con.acquire():
        while True:
            if product is not None:
                print('consume...')
                product = None

                # 通知生产者，商品已经没了
                con.notify()

            # 等待通知
            con.wait()
            time.sleep(2)

t1 = threading.Thread(target=produce)
t2 = threading.Thread(target=consume)
t2.start()
t1.start()

'''

'''
# encoding: UTF-8
import threading
import time

# 计数器初值为2
semaphore = threading.Semaphore(2)

def func():

    # 请求Semaphore，成功后计数器-1；计数器为0时阻塞
    print ('%s acquire semaphore...' % threading.currentThread().getName())
    if semaphore.acquire():

        print ('%s get semaphore' % threading.currentThread().getName())
        time.sleep(4)

        # 释放Semaphore，计数器+1
        print ('%s release semaphore' % threading.currentThread().getName())
        semaphore.release()
        print()

t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t3 = threading.Thread(target=func)
t4 = threading.Thread(target=func)
t1.start()
t2.start()
t3.start()
t4.start()

time.sleep(2)

# 没有获得semaphore的主线程也可以调用release
# 若使用BoundedSemaphore，t4释放semaphore时将抛出异常
print ('MainThread release semaphore without acquire')
semaphore.release()

'''


'''

# encoding: UTF-8
import threading
import time

event = threading.Event()

def func():
    # 等待事件，进入等待阻塞状态
    print ( '%s wait for event...' % threading.currentThread().getName())
    event.wait()

    # 收到事件后进入运行状态
    print ('%s recv event.' % threading.currentThread().getName())

t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t1.start()
t2.start()

time.sleep(2)

# 发送事件通知
print ('MainThread set event.')
event.set()

'''

'''
# encoding: UTF-8
import threading

def func():
    print ('hello timer!')

timer = threading.Timer(5, func)
timer.start()

'''

# encoding: UTF-8
import threading


'''
alist = None
condition = threading.Condition()

def doSet():
    if condition.acquire():
        while alist is None:
            condition.wait()
        for i in range(len(alist))[::-1]:
            alist[i] = i
            # print(threading.enumerate())
        condition.release()
        # print(threading.enumerate())
        for i in threading.enumerate():
            print(i.getName())

def doPrint():
    if condition.acquire():
        while alist is None:
            condition.wait()
        for i in alist:
            print (i)
        print()
        # print(threading.enumerate())
        for i in threading.enumerate():
            print(i.getName())
        print('%s release' % threading.currentThread().getName())
        condition.release()
        for i in threading.enumerate():
            print(i.getName())

def doCreate():
    global alist
    if condition.acquire():
        if alist is None:
            alist = [0 for i in range(10)]
            condition.notifyAll()
            # print(threading.enumerate())
        condition.release()
        print('%s release' % threading.currentThread().getName())
        # print(threading.enumerate())
        for i in threading.enumerate():
            print(i.getName())


tset = threading.Thread(target=doSet,name='tset')
tprint = threading.Thread(target=doPrint,name='tprint')
tcreate = threading.Thread(target=doCreate,name='tcreate')
tset.start()
tprint.start()
tcreate.start()
for i in threading.enumerate():
    print(i.getName())



'''







class MyTest(threading.Thread):

    def __init__(self):
        self.alist = None
        self.condition = threading.Condition()

    def func_a(self):
        if self.condition.acquire():
            while self.alist == None:
                print("func_a is waiting.")
                self.condition.wait()
            print('func_a', self.alist)
            self.condition.release()

    def func_b(self):
        if self.condition.acquire():
            while self.alist == None:
                print("func_b is waiting.")
                self.condition.wait()
            print('func_b', self.alist)
            self.condition.release()

    def func_c(self):
        if self.condition.acquire():
            if self.alist is None:
                self.alist = [0 for i in range(10)]
                self.condition.notifyAll()
            print("func_c 886.")
        self.condition.release()


temp_a = MyTest()

tset = threading.Thread(target=temp_a.func_a,name='tset')
tprint = threading.Thread(target=temp_a.func_b,name='tprint')
tcreate = threading.Thread(target=temp_a.func_c,name='tcreate')
tset.start()
tprint.start()
tcreate.start()