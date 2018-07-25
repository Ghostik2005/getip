# getip
Python module to get client internal and external ip address from multiple sources using async requests

# usage

import getip

if "__main__" == __name__:
    ips = None
    ips = getip.ip()
    if ips:
        print(ips)
