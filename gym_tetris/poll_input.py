import sys
import select

p = open('/dev/input/js0','r')
e = select.epoll()
e.register(p, select.EPOLLIN | select.EPOLLET)


for i in range(100):
    #r, _, _ = select.select([sys.stdin], [], [], 1)
    r = e.poll(1)
    print(r)
