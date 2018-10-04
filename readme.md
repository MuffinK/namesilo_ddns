# namesilo_ddns
ddns for namesilo using python2 or docker on linux, mac or windows

## How to use
### using python2
1. get namesilo [api_key](https://www.namesilo.com/account_api.php), from namesilo
2. rename ddns.conf.example to ddns.conf
3. edit namesilo_api_key rrhost, host_name and domain_name in ddns.conf file
4. pip install crontabs
5. python main.py

### or using docker
1. edit ddns.conf

```apacheconf
[common]
api_key = 1234567890abcdef1234
host_name = test.example.com
domain_name = example.com
rrhost = test
#time_interval = 20 #Optional
```
2. run
```bash
docker run --name namesilo_ddns --rm -v $(pwd)/ddns.conf:/app/ddns.conf -d namesilo_ddns:latest
```

it will update domain dns recode to your ip every 20(can be configed) minutes
