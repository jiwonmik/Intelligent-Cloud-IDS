#!/usr/bin/env python3 

import datetime, psutil, get, platform, uuid, re
import os from pymongo 
import MongoClient from requests 
import netifaces as ni 
def main(): 
  try: 
    client=MongoClient(host='0.0.0.0:27017', username="dbadmin", password="dbadmin") 
    db=client.CloudIDS print('MongoDB Connected.') 

    #collect some stats from psuti 
    boot_time=psutil.boot_time() 

    #get public IP 
    public_ip=get('https://api.ipify.org').text 

    #get privet IP 
    private_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'] 
    #create data 
    metrics={ 
          'bootTime':datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
          'users_info' : psutil.users(), 
          'host_public_ip' : public_ip, 
          'host_private_ip' : private_ip, 
          'MAC_address' : ':'.join(re.findall('..', '%012x' % uuid.getnode())),
          'os' : os.name, 
          'platform' : platform.system(), 
          'platform_version' : platform.release(), 
          'date' : datetime.datetime.now(), 
    } 
    result=db.default.insert_one(metrics) 
    #print to the console the ObjectID of the new document 
    print('Created host metrics as {0}'.format(result.inserted_id)) 
    print('finished creating host metrics') 

  except Exception as e:
    print(traceback.format_exc()) 
  finally: 
    client.close() 
    print('MongoDB Closed.') 
if __name__ == "__main__": 
  main()


