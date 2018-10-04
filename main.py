import urllib2
import json
import xml.etree.ElementTree as ET
import os
from os.path import expanduser
from crontabs import Cron, Tab
import ConfigParser


api_url = 'https://www.namesilo.com/api/'

Config = ConfigParser.ConfigParser()
Config.read("ddns.conf")

api_key = Config.get("common", 'api_key')
host_name = Config.get("common", 'host_name')
domain_name = Config.get("common", 'domain_name')
rrhost = Config.get("common", 'rrhost')

try:
    time_interval = Config.getint('common', 'time_interval', 20)
except Exception as e :
    time_interval = 20

def update():

    real_ip = json.loads(urllib2.urlopen("http://v4.ipv6-test.com/api/myip.php?json").read())['address']
    print('your wan ip is: ' + real_ip)

    home_dir = expanduser("~")
    filename = os.path.join(home_dir, ".namesilo_cache.json")

    cache_ip = ''
    if os.path.isfile(filename):
        with open(filename) as f:
            try:
                cache_ip = json.loads(f.read()).get('address')
            except Exception as e:
                print(e)
            f.close()

    if cache_ip != real_ip:
        req = urllib2.Request(api_url + 'dnsListRecords?version=1&type=xml&key=' + api_key + '&domain=' + domain_name,
                        headers={'User-Agent': "Magic Browser"})

        r = urllib2.urlopen(req).read()

        dns_list_tree = ET.fromstring(r)
        record = [x for x in dns_list_tree[1] if len(x) >= 3 and x[2].text == host_name]

        record_id = record[0][0].text

        req = urllib2.Request(api_url + 'dnsUpdateRecord?version=1&type=xml&key=' + api_key + '&domain=' + domain_name +
            '&rrid=' + record_id + '&rrhost=' + rrhost + '&rrvalue=' + real_ip + '&rrttl=7207', headers={'User-Agent': "Magic Browser"})

        print(urllib2.urlopen(req).read())

        with open(filename, 'w+') as f:
            f.write(json.dumps({
                "address": real_ip
            }))
            f.close()
    else:
        print('ip not change')
update()
Cron().schedule(
    Tab(name='run_my_job').every(minutes=time_interval).run(update)
).go()
