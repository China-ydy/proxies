url = 'https://proxycompass.com/cn/free-proxies/asia/china/#:~:text=%E5%85%8D%E8%B4%B9%E4%B8%AD%E5%9B%BD%E4%BB%A3%E7%90%86.%20%E6%B5%8F%E8%A7%88'
test_url = 'https://httpbin.org'
test_url_ip = 'https://httpbin.org/ip'
true_url = 'https://ping0.cc'
time=0.5
import requests
import parsel

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
     }

proxies = []  #{"协议":"地址:port"}
can_use_proxy = []
def check_ip(proxies):
    for proxy in proxies:
        print(f"当前测试IP为{proxy}")
        try:
            test_response = requests.get(test_url, proxies=proxy, headers=headers,timeout=time)
            if test_response.status_code == 200:
                test_response_ip =requests.get(test_url_ip, proxies=proxy, headers=headers,timeout=time)
                can_use_proxy.append(proxy)
                print(test_response_ip.json())
                print(f'{proxy} 测试为可访问，状态码为 {test_response.status_code},返回本地IP为{test_response_ip.text}')
        except Exception as e:
            print(f'异常状态{e},IP {proxy}测试为不可访问')



#请求数据
response = requests.get(url, headers=headers)
#转换parsel实例
data_parsel = parsel.Selector(response.text)
#查询到tr级
tr_content = data_parsel.xpath('//div[@class="table-responsive"]/table[@id="proxylister-table"]/tbody/tr')
#循环遍历 二次提取
for tr in tr_content:
    http_type=tr.xpath('.//td/text()')[2].extract()
    ip_num = tr.xpath('.//td/text()')[0].extract()
    ip_port = tr.xpath('.//td/text()')[1].extract()
    http_type_dict = [http_type]
    for i in http_type_dict:
        if "HTTP" in i:
            # 构建代理IP字典
            proxies_dist = {'http': 'http://'+ip_num + ':' + ip_port}
            proxies.append(proxies_dist)
print(f'获取到的IP数量为 {len(proxies)} 个')
#print(proxies)
check_ip(proxies)
print(f'可用IP数量为{len(can_use_proxy)}')


