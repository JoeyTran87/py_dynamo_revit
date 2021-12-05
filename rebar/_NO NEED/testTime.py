import time

t = time.strftime("%d-%m-%y %H:%M:%S",time.localtime(time.time()))


print (t)

t2 = time.strptime(t,"%d-%m-%y %H:%M:%S")

print (t2)

t3 = time.strftime("%y%m%d %H%M%S",time.strptime(t,"%d-%m-%y %H:%M:%S"))

print(t3)