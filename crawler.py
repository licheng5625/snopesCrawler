__author__ = 'licheng5625'
from bs4 import BeautifulSoup
import urllib.request
import zlib
import datetime
import json
import time

class SnoperCrawler:
    __mydictdata =list()

    def CrawOnePage(self,websitepage=1):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),('DNT', "1"),('Accept-Language', "en-US;q=0.8,en;q=0.2"),('Accept-Encoding', "gzip, deflate, sdch")]
        url=opener.open('http://www.snopes.com/info/whatsnew.asp?page='+str(websitepage)).read()
        decompressed_data=zlib.decompress(url, 16+zlib.MAX_WBITS)
        #print (decompressed_data.decode('utf-8'))
        #url= urllib.request.urlopen().read()
        soup = BeautifulSoup(decompressed_data)
        #soup = BeautifulSoup(open("/Users/licheng5625/Desktop/What's New _ snopes.com.htm"))

        #fff=soup.find_all("a","img-wrapper")
        postlist =soup.find(attrs={"class": "post-list"})
        items=postlist.find_all("li")
        i=0
        for item in items:
            onepost=item.find("span","label")
            if onepost is not None:
                i=i+1
                print ('NO:'+ str(i))
                link=item.find(attrs={"class": "title"}).find('a') .get('href')
                link ="http://www.snopes.com"+link
                print (link)
                print (onepost.text)
                contentdict=self.__CrawContent(link,onepost.text)
                contentdict["ID"]=i


                self.__mydictdata.append(contentdict)
    def __CrawContent(self,link,kind):
        mydict = dict()
        mydict["Label"]=kind
        url2= urllib.request.urlopen(link).read()
        soup2 = BeautifulSoup(url2)
        if len(soup2.find_all("div","claim-old old-mfalse"))!=0:
            print ('result: MOSTLY FALSE' )
            mydict["Result"]="MOSTLY FALSE"
        if len(soup2.find_all("div","claim-old old-false"))!=0:
            print ('result: FALSE' )
            mydict["Result"]="FALSE"
        if len(soup2.find_all("div","claim-old old-mixture"))!=0:
            print ('result: MIXTURE' )
            mydict["Result"]="MIXTURE"
        if len(soup2.find_all("div","claim-old old-undetermined"))!=0:
            print ('result: UNDETERMINED' )
            mydict["Result"]="UNDETERMINED"

        clams=soup2.find_all("span","green-label")
        for clam in clams:
            if clam.text == 'Claim:':
                clamtext=clam.parent.text.replace('Claim: ','')
                print (clamtext)
                mydict["Claim"]=clamtext

            if clam.text =='Originally published:':
                timetext =  clam.parent.text.replace("Originally published: ","")
                time = datetime.datetime.strptime(timetext,"%d %B %Y")
                print ("Originally published: "+time.strftime("%d %B %Y"))
                mydict["Originally published Time"]=timetext

        taglist=soup2.find("div","article-tags clearfix")
        print ("tags:")
        tagtextlist =list()
        if taglist is not None:
            tags =taglist.find_all("a")
            for tag in tags:
                tagtextlist.append(tag.text)
                print (tag.text.encode('utf-8'))
        mydict["Tags"]=tagtextlist
        return mydict

    def __MakeJSON(self,mydic):
            JSON = json.dumps(mydic, ensure_ascii=False)
            return JSON
    def WriteJSON(self,path=''):
         with open(path + 'journal' + self.gettimestamp() + '.txt', encoding='utf-8', mode='w+') as reporter:
             for onestory in self.__mydictdata:
                JSON = self.__MakeJSON(onestory)
                reporter.write(JSON + '\n')
    def gettimestamp(self):
        format_type = u'%Y_%m_%d_%H_%M_%S'
        return time.strftime(format_type, time.localtime(time.time()))
s=SnoperCrawler();
for i in range(1,30):
    s.CrawOnePage(i);
    s.  WriteJSON()