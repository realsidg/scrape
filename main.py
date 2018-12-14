from bs4 import BeautifulSoup
import requests
import html

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

q=html.escape(input("Enter Search Query:"))
url="http://www.flipkart.com/search?q="+q
page= requests.get(url, headers=hdr)
soup=BeautifulSoup(page.text, 'html.parser')
containers=soup.findAll('div',{"class":"_1UoZlX"})

pgs=int(soup.find("div", {"class":"_2zg3yZ"}).find('span').text[10:]) if len(containers) else 0

Results=[]

for pg in range(1, pgs+1):

    print("Parsing page ", pg, "/", pgs)

    qp="http://www.flipkart.com/search?q="+q+"&page="+str(pg)
    page= requests.get(qp)
    soup=BeautifulSoup(page.text, 'html.parser')
    containers=soup.findAll('div',{"class":"_1UoZlX"})

    if len(containers)==0:
        containers=soup.findAll('div',{"class":"_3liAhj _1R0K0g"})
        for c in containers:
            result={}
            result['name']=c.find("a", {"class":"_2cLu-l"}).text.replace(',','')
            result['price']=int(c.find("div", {"class":"_1vC4OE"}).text[1:].replace(',',''))
            result['rating']=c.find("div", {"class":"hGSR34"}).text.replace(',','')      
            Results.append(result)
            

    else:
        for c in containers:
            result={}
            result['name']=c.find("div", {"class":"_3wU53n"}).text.replace(',','')
            result['price']=int(c.find("div", {"class":"_1vC4OE _2rQ-NK"}).text[1:].replace(',',''))
            result['rating']=c.find("div", {"class":"hGSR34"}).text.replace(',','')      
            Results.append(result)

    if pg == pgs:
        print("\nParse Complete!\n")

if len(Results):
    ch=1
    while ch in [1,2,3,4]:
        ch=int(input("1.Display Data \n2.Display Cheapest Products\n3.Display Most expensive products \n4.Export to csv\n5.Exit\n\n"))
        
        if ch==1:
            for r in Results:
                print('%50s'%r['name'], "\t", '%10s'%r['price'],'\t', r['rating'])

        
        elif ch==2:
            min=[Results[0]]
            for r in Results[1:]:

                if r['price']==min[0]['price']:
                    min.append(r)
                elif r['price']<min[0]['price']:
                    min=[r]
            
            for r in min:
                print('%50s'%r['name'], "\t", '%10s'%r['price'],'\t', r['rating'])
  
        elif ch==3:
            max=[Results[0]]
            for r in Results[1:]:
                if r['price']==max[0]['price']:
                    max.append(r)
                elif r['price']>max[0]['price']:
                    max=[r]
            
            for r in max:
                print('%50s'%r['name'], "\t", '%10s'%r['price'],'\t', r['rating'])
  
            
        elif ch==4:
            fil=open(q+".csv", 'w')
            fil.write("Name,Price,Rating\n")
            for r in Results:
                fil.write(r['name']+","+str(r['price'])+','+r['rating'][:-1]+'\n')
            fil.close()
            print("\nExported to "+q+".csv\n")
else:
    print("Product not found")