Creamos el ambiente para la aplicacion
virtualenv scraperCRAS


scraperCRAS/bin/pip install requisites/html5lib-0.9999999.tar.gz
scraperCRAS/bin/pip install requisites/lxml-3.5.0.tar.gz 
scraperCRAS/bin/pip install requisites/beautifulsoup4-4.4.1.tar.gz
scraperCRAS/bin/pip install requisites/requests-2.10.0.tar.gz
scraperCRAS/bin/pip install requisites/dryscrape-1.0.tar.gz


//Hay que meter lo de postgresql

scraperCRAS/bin/python scraper.py


http://mundogeek.net/archivos/2008/04/15/interactuar-con-webs-en-python/


from bs4 import BeautifulSoup
import urllib
r = urllib.urlopen('http://preopendata.aragon.es/apps/cras/scrapea_trayecto/?filtroCRA=1&filtroMuni=50199').read()
soup = BeautifulSoup(r)

soup.prettify()




htmlResumen = soup.find_all(class_='section-title')

section-title

soup.find_all(class_='adp-summary')


 for nom in soup.select('.nomEstacio'):
 
        # Metemos el nombre de la parada en el array correspondiente
        arrayNoms.append(nom.string)


from bs4 import BeautifulSoup
import urllib
import urllib2

# Creamos el opener y le añadimos los headers
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

response = opener.open('http://preopendata.aragon.es/apps/cras/scrapea_trayecto/?filtroCRA=1&filtroMuni=50199')
# Leemos el contenido y lo cargamos en BeautifulSoup
data = response.read()
soup = BeautifulSoup(data)




---------------------------------------------------



from bs4 import BeautifulSoup
import urllib
import urllib2

params = urllib.urlencode({"filtroCRA": "1", "filtroMuni": "50199"})  
f = urllib2.urlopen("http://preopendata.aragon.es/apps/cras/scrapea_trayecto/", params)  







import urllib
import urllib2

url = 'http://preopendata.aragon.es/apps/cras/scrapea_trayecto/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {"filtroCRA": "1", "filtroMuni": "50199"}
headers = { 'User-Agent' : user_agent }

data  = urllib.parse.urlencode(values)
data = data.encode('utf-8')
req = urllib.request.Request(url, data, headers)
response = urllib.request.urlopen(req)
the_page = response.read()



import requests, bs4
values = {"filtroCRA": "1", "filtroMuni": "50199"}
r = requests.get('http://preopendata.aragon.es/apps/cras/scrapea_trayecto/', params=values, timeout=0.001)









--------------------------------------------------------------------------------
https://www.google.es/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=get+html+code+after+load+page+python









