#! /usr/bin/python3.8
# coding = utf-8
from ping3 import ping
import threading
from socket import *
import os
import time
# 定义最大并发线程数, 并发数太多会报错
max_connections = 1000
pool_sema = threading.Semaphore(max_connections)


# 重写threading获取函数的返回值
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        # join主进程等待子进程运行完才退出
        # 需要调用join才能获取get_result函数，但是join写在这里每次调用都会等待，导致多线程变单线程，所以我放在外面去调用
        # threading.Thread.join(self)
        try:
            return self.result
        except Exception:
            return None


def ping_check(ip):
    # 线程加锁
    pool_sema.acquire()
    result = ping(ip, timeout=1)
    # 线程解锁
    pool_sema.release()
    if result:
        return ip
    else:
        return None


def th_ping():
    ip = input('please into check ip or vlan: ')
    global start_time
    start_time = time.time()
    ip_num = '.'.join(ip.split('.')[0:3])
    mask_num = ip.split('.')[-1]
    if mask_num == '0':
        threads = [None] * 256
        for i in range(1, 256):
            ip = ip_num + '.' + str(i)
            threads[i] = MyThread(ping_check, (ip,))
            threads[i].start()
        for i in range(1, 256):
            threads[i].join()
            if threads[i].get_result():
                print(threads[i].get_result(), 'is up')
    else:
        result = ping_check(ip)
        if result:
            print(f'{ip} is up')
        else:
            print(f'{ip} is down')


def port_check(ip, port, port_type):
    pool_sema.acquire()
    if port_type == 'TCP' or port_type == 'tcp':
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        tcp_socket.settimeout(3)
        result = tcp_socket.connect_ex((ip, port))
        tcp_socket.close()
        pool_sema.release()
        if result == 0:
            print(f'{ip} TCP:{port} is up')
        else:
            return os.strerror(result)
    elif port_type == 'UDP' or port_type == 'udp':
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        udp_socket.settimeout(3)
        result = udp_socket.connect_ex((ip, port))
        udp_socket.close()
        pool_sema.release()
        if result == 0:
            print(f'{ip} UDP:{port} is up')
        else:
            return os.strerror(result)
    else:
        pool_sema.release()
        return 'port type error'


def th_port():
    ip = input('please into check ip or vlan: ')
    begen_port = int(input('please into begen port[1-65535]: '))
    end_port = int(input(f'please into end port[{begen_port}-65535]: '))
    port_type = input('please into port type[TCP/UDP]: ')
    global start_time
    start_time = time.time()
    ip_num = '.'.join(ip.split('.')[0:3])
    mask_num = ip.split('.')[-1]
    if mask_num == '0':
        threads = [None] * 256
        for i in range(1, 256):
            ip = ip_num + '.' + str(i)
            threads[i] = MyThread(ping_check, (ip,))
            threads[i].start()
        for i in range(1, 256):
            threads[i].join()
            ip = threads[i].get_result()
            if ip:
                for port in range(begen_port, end_port+1):
                    th2 = threading.Thread(target=port_check, args=(ip, port, port_type))
                    th2.start()
            else:
                pass
    else:
        try:
            ip = gethostbyname(ip)
            for port in range(begen_port, end_port+1):
                th2 = threading.Thread(target=port_check, args=(ip, port, port_type))
                th2.start()
        except:
            print(f'{ip} is down')


if __name__ == '__main__':
    print('1. host ping check')
    print('2. host port check')
    num = input('please into num: ')
    if num == '1':
        th_ping()
    elif num == '2':
        th_port()
    else:
        print('not in option')
    end_time = time.time()
    print('Time consumed:', round(end_time - start_time, 3), 's')
