#coding: utf-8

import getip

if "__main__" == __name__:
    ips = None
    ips = getip.ip()
    if ips:
        print(ips)


    

