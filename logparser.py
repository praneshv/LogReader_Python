from collections import Counter
from urllib.parse import urlparse
from optparse import OptionParser

# defining options
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="log file to parse", metavar="FILE")
parser.add_option("-a", "--all",
                  action="store_true", dest="all", default=False,
                  help="Default print all info")
parser.add_option("-r", "--toprequests",
                  action="store_true", dest="top_request", default=False,
                  help="Top requests")
parser.add_option("-d", "--tophosts",
                  action="store_true", dest="top_hosts", default=False,
                  help="Top Hosts")
parser.add_option("-s", "--success",
                  action="store_true", dest="success", default=False,
                  help="Success percentage")

parser.add_option("-u", "--failure",
                  action="store_true", dest="failure", default=False,
                  help="Failure percentage")
(options, args) = parser.parse_args()


logfile = options.filename

# print (options)
# index to value mapping
name_to_index = {"hostname": 0, "status": 8, "method": 5, "url": 10}

required_data = []
with open(logfile) as log:
    for line in log:
        # print (line.split(), "-->", len(line.split()))
        row = line.split()
        r = {}
        for key,value in name_to_index.items():
            if key == "url":
                r[key] = row[value][1:-1]
            else:
                r[key] = row[value]

        required_data.append(r)

# print (required_data)

result = {}
sites = []
success_hit_count = 0
failure_hit_count = 0
failure_request_obj = []
host_info = []

for data in required_data:
    # data["url"]
    url = data["url"]
    # top requests made
    if data["url"].startswith('http'):
        # trim the suffix         
        parsed_uri = urlparse(url)
        sites.append('{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri))

    if int(data["status"]) >= 200 and data["status"] <= "399":
        success_hit_count += 1
    else:
        failure_hit_count += 1
        if data["url"].startswith('http'):
            failed_uri = urlparse(url)
            failure_request_obj.append('{uri.scheme}://{uri.netloc}/'.format(uri=failed_uri))        
            # failure_request_obj.append(data["url"])
    # top hosts        
    host_info.append(data["hostname"])

# Handle all options - can be done in better way. 
if options.all:

    _sort_data=Counter(sites)               
    site_tuple = sorted(_sort_data.items(),key=lambda x:x[1], reverse=True)[0:10]
    # print (site_tuple)
    print ("Top 10 requested pages and the number of requests made for each")
    print ('-'*70)
    for site,hit in site_tuple:
        print (f"{site} - {hit} Hits")

    # success percentage
    total_req = len(required_data)
    success_percent =  ((success_hit_count/total_req)*100)
    print ('-'*70)
    print (f"Total Successful Response % = {success_percent:1.2f}")

    # failure percent
    failure_percent =  ((failure_hit_count/total_req)*100)
    print ('-'*70)
    print (f"Total Un-Successful Response % = {failure_percent:1.2f}")

    # top 10 failure
    print ('-'*70)
    print ("Top 10 Un-Successful requests")
    _sort_data_f=Counter(failure_request_obj)               
    f_site_tuple = sorted(_sort_data_f.items(),key=lambda x:x[1], reverse=True)[0:10]
    for site,hit in f_site_tuple:
        print (f"{site} - {hit} Hits")

    print ('-'*70)
    print ("Top 10 hosts making the most requests")
    print ('-'*70)
    host = Counter(sorted(host_info))
    ip_tuple = sorted(host.items(), key = lambda x:x[1], reverse=True)[0:10]
    for ip,per in ip_tuple:
        print (f"{ip} - {per} Requests")

elif options.top_hosts:

    print ("Top 10 hosts making the most requests")
    print ('-'*70)
    host = Counter(sorted(host_info))
    ip_tuple = sorted(host.items(), key = lambda x:x[1], reverse=True)[0:10]
    for ip,per in ip_tuple:
        print (f"{ip} - {per} Requests")

elif options.top_request:
    _sort_data=Counter(sites)               
    site_tuple = sorted(_sort_data.items(),key=lambda x:x[1], reverse=True)[0:10]
    print ("Top 10 requested pages and the number of requests made for each")
    print ('-'*70)
    for site,hit in site_tuple:
        print (f"{site} - {hit} Hits")

elif options.success:
    # success percentage
    total_req = len(required_data)
    success_percent =  ((success_hit_count/total_req)*100)
    print ('-'*70)
    print (f"Total Successful Response % = {success_percent:1.2f}")

elif options.failure:    
    # top 10 failure
    print ("Top 10 Un-Successful requests")
    print ('-'*70)
    _sort_data_f=Counter(failure_request_obj)               
    f_site_tuple = sorted(_sort_data_f.items(),key=lambda x:x[1], reverse=True)[0:10]
    for site,hit in f_site_tuple:
        print (f"{site} - {hit} Hits")
