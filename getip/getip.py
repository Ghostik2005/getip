#coding: utf-8

import re
import ssl
import socket
import asyncio
import urllib.request
import concurrent.futures as Futures

def ip():
    #list of the services to detect external client ip
    SERVICES = [
        'https://sklad71.org/consul/ip/',
        'http://ip-address.ru/show',
        'http://yandex.ru/internet',
        'http://ip-api.com/line/?fields=query',
        'http://icanhazip.com',
        'http://ipinfo.io/ip',
        'https://api.ipify.org'
        ]

    async def getIp(service):
        """
        get ip's function
        """
        ssl._create_default_https_context = ssl._create_unverified_context #cancel the certificate verification for SSL requests
        search_re = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" #regular expression template for looking the ip in response
        eip = "not available"
        iip = "not available"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as se: #connect via IPv4  with datagram based protocol
                se.connect(("77.88.8.8", 80)) #connect to Yandex DNS Server
                iip = se.getsockname()[0]
        except Exception as e:
            print("internal getip ERROR:%s" %str(e), flush=True)
        r = None
        data = ""
        try:
            with urllib.request.urlopen(service, timeout=5) as r: #ask the service
                data = str(r.headers)
                data += r.read().decode()
                eip = re.findall(search_re, data)[0].strip() #look for ip in response
        except Exception as e:
            print("external getip ERROR:%s" % str(e), flush=True)
        return {"service": service, "ext_ip": eip, "int_ip": iip}

    async def async_ip():
        response = {
            "service": "No results",
            "ext_ip": "not available",
            "int_ip": "not available"
        }
        futures = [getIp(service) for service in SERVICES] #make the list of futures: one future for one service
        done, pending = await asyncio.wait(
            futures, return_when=Futures.FIRST_COMPLETED, timeout=4) #waiting for first answer
        for future in pending:
            future.cancel() #cancel all incomleted calls
        for future in done:
            f = future.result() #get the result from completed calls
            response.update(f)
        return response

    loop = asyncio.get_event_loop() #create the async loop
    ip = loop.run_until_complete(async_ip()) #get the response from function when loop completed
    loop.close()
    return ip
