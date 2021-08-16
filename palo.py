from lars import apache
from collections import Counter
from urllib.parse import urlparse

logfile1="/Users/praneshvenkatraman/Desktop/My_Mac/palo_alto/access1.log"
site=[]
with open(logfile1) as log:
    for line in log:
        if len((line.split()[10:12:2]))!=0:
            var_site = (line.split()[10:12:2][0][1:-1])
            if var_site.startswith('http'):           
                parsed_uri = urlparse(var_site)
                site.append('{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri))
                
dict1=Counter(site)               
site_tuple = sorted(dict1.items(),key=lambda x:x[1], reverse=True)[0:10]

print ('-'*70)
print ("Top 10 requested pages and the number of requests made for each")
print ('-'*70)
for site,hit in site_tuple:
    print (f"{site} - {hit} Hits")
print ('-'*70)
with open(logfile1) as log:
    with apache.ApacheSource(log) as hits:
        print (dir(hits))
        response_200=[]
        response_unsuc=[]
        total_host=[]
        total = 0 
        for row in hits:
            total += 1 
            total_host.append(str(row.remote_host))
            if row.status>=200 and row.status<=399:
                response_200.append(row)
            else:
                response_unsuc.append(row)
                
res_200 = (len(response_200))
total_success =  ((res_200/total)*100)
print (f"Total Successful Response % = {total_success:1.2f}")
print (f"Total Un-Successful Response % = {100-total_success:1.2f}")
host = Counter(sorted(total_host))
ip_tuple = sorted(host.items(), key = lambda x:x[1], reverse=True)[0:10]
print ('-'*40)
print ("Top 10 hosts making the most requests")
print ('-'*40)
for ip,per in ip_tuple:
    print (f"{ip} - {per} Requests")
