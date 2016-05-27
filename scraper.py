# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import re
import urllib
import dryscrape
import json
import sys



#Codigo de http://carlosvin.github.io/en/posts/delete-html-tags-py-django.html
def strip_tags(value):
	return re.sub(r'<[^>]*?>', '', value)


#Metodo que parsea el resumen del trayecto. Devuelve [trayecto km, trayecto tiempo]
def parseaResumen(rutaResumen):
	strip_tags(rutaResumen)
	dev = []
	dev = strip_tags(rutaResumen).split('.')
	resumen=[]
	for a in dev:
		resumen.append(a.strip())
	return resumen

#Metodo que captura el resumen del trayecto
def getResumen(url):
	session = dryscrape.Session()
	session.visit(url)
	response = session.body()
	soup = BeautifulSoup(response)
	htmlResumen = soup.find_all(class_='adp-summary')
	#print 'El resumen es '+str(htmlResumen[0])
	resumenParseado =parseaResumen(str(htmlResumen[0]))
	resumenParseadaJSON = {
		'distancia': resumenParseado[0],
		'tiempo': resumenParseado[1]
	}
	return json.dumps(resumenParseadaJSON)

#Metodo que parsea  un paso de ruta, que estara separada por &
def parseaPasoRuta(pasoString):
	paso = []
	paso = pasoString.split('&') #se debe de borrar el primer y el ultimo elemento, el primero es por motivo del icono que meten y el ultimo es por motivo de haber hecho el replace 
	
	paso.pop(len(paso)-1)
	if len(paso)>1:
		paso.pop(0)
	return paso


#Metodo que parsea una ruta completa
def parseaRuta(rutaString):
	dev=[]
	pasos=rutaString.split('@')
	for paso in pasos:
		dev.append(parseaPasoRuta(paso))
	dev.pop(len(dev)-1)
	return dev


#Metodo que se le pasa como parametro la una ruta de google con codigo html y este dividido en los pasos de 
def ruta(rutaGoogle):
	rutaGoogle = rutaGoogle.replace('</td>', '</td>&')
	rutaGoogle = rutaGoogle.replace('</tr>', '</tr>@')
	rutaParseada =[]

	rutaParseada = parseaRuta(strip_tags(rutaGoogle))

	return rutaParseada

#metodo que captura los pasos de la ruta
def getRuta(url):
	session = dryscrape.Session()
	session.visit(url)
	response = session.body()
	soup = BeautifulSoup(response)
	htmlResumen = soup.find_all(class_='adp-directions')
	rutaParseada = ruta(str(htmlResumen[0]))
	rutaPorPasosJSON=[]

	for paso in rutaParseada:
		pasoJSON={
			'numero_paso':paso[0].replace('.', ''),
			'descripcion_recorrido':paso[1],
			'distancia_recorrida':paso[2]
		}
		rutaPorPasosJSON.append(pasoJSON)
	return json.dumps(rutaPorPasosJSON)

#https://pythonadventures.wordpress.com/tag/unicodeencodeerror/
def encode(text):
    """
    For printing unicode characters to the console.
    """
    return text.encode('utf-8')

def main():
	URL = 'http://preopendata.aragon.es/apps/cras/scrapea_trayecto/'
	parametrosURL = ['?filtroCRA=74&filtroMuni=22001', '?filtroCRA=74&filtroMuni=22003', '?filtroCRA=71&filtroMuni=22007', '?filtroCRA=61&filtroMuni=22008', '?filtroCRA=73&filtroMuni=22009', '?filtroCRA=73&filtroMuni=22016', '?filtroCRA=1&filtroMuni=22018', '?filtroCRA=60&filtroMuni=22022', '?filtroCRA=1&filtroMuni=22023', '?filtroCRA=74&filtroMuni=22024', '?filtroCRA=72&filtroMuni=22025', '?filtroCRA=64&filtroMuni=22027', '?filtroCRA=53&filtroMuni=22028', '?filtroCRA=70&filtroMuni=22035', '?filtroCRA=63&filtroMuni=22040', '?filtroCRA=74&filtroMuni=22041', '?filtroCRA=71&filtroMuni=22052', '?filtroCRA=70&filtroMuni=22053', '?filtroCRA=69&filtroMuni=22054', '?filtroCRA=58&filtroMuni=22055', '?filtroCRA=57&filtroMuni=22057', '?filtroCRA=74&filtroMuni=22058', '?filtroCRA=68&filtroMuni=22059', '?filtroCRA=67&filtroMuni=22060', '?filtroCRA=66&filtroMuni=22066', '?filtroCRA=66&filtroMuni=22069', '?filtroCRA=53&filtroMuni=22076', '?filtroCRA=59&filtroMuni=22077', '?filtroCRA=65&filtroMuni=22080', '?filtroCRA=60&filtroMuni=22082', '?filtroCRA=59&filtroMuni=22083', '?filtroCRA=69&filtroMuni=22084', '?filtroCRA=74&filtroMuni=22088', '?filtroCRA=73&filtroMuni=22089', '?filtroCRA=64&filtroMuni=22096', '?filtroCRA=67&filtroMuni=22099', '?filtroCRA=63&filtroMuni=22102', '?filtroCRA=63&filtroMuni=22103', '?filtroCRA=73&filtroMuni=22105', '?filtroCRA=66&filtroMuni=22109', '?filtroCRA=63&filtroMuni=22110', '?filtroCRA=54&filtroMuni=22112', '?filtroCRA=57&filtroMuni=22114', '?filtroCRA=63&filtroMuni=22115', '?filtroCRA=1&filtroMuni=22116', '?filtroCRA=62&filtroMuni=22116', '?filtroCRA=55&filtroMuni=22119', '?filtroCRA=58&filtroMuni=22124', '?filtroCRA=65&filtroMuni=22129', '?filtroCRA=53&filtroMuni=22131', '?filtroCRA=58&filtroMuni=22135', '?filtroCRA=62&filtroMuni=22136', '?filtroCRA=61&filtroMuni=22137', '?filtroCRA=65&filtroMuni=22142', '?filtroCRA=69&filtroMuni=22143', '?filtroCRA=57&filtroMuni=22144', '?filtroCRA=70&filtroMuni=22157', '?filtroCRA=60&filtroMuni=22158', '?filtroCRA=63&filtroMuni=22160', '?filtroCRA=71&filtroMuni=22167', '?filtroCRA=68&filtroMuni=22170', '?filtroCRA=59&filtroMuni=22172', '?filtroCRA=58&filtroMuni=22174', '?filtroCRA=57&filtroMuni=22182', '?filtroCRA=74&filtroMuni=22186', '?filtroCRA=65&filtroMuni=22187', '?filtroCRA=60&filtroMuni=22193', '?filtroCRA=1&filtroMuni=22197', '?filtroCRA=69&filtroMuni=22200', '?filtroCRA=74&filtroMuni=22201', '?filtroCRA=68&filtroMuni=22204', '?filtroCRA=67&filtroMuni=22205', '?filtroCRA=57&filtroMuni=22207', '?filtroCRA=53&filtroMuni=22208', '?filtroCRA=61&filtroMuni=22213', '?filtroCRA=62&filtroMuni=22220', '?filtroCRA=64&filtroMuni=22222', '?filtroCRA=72&filtroMuni=22225', '?filtroCRA=55&filtroMuni=22226', '?filtroCRA=64&filtroMuni=22228', '?filtroCRA=70&filtroMuni=22229', '?filtroCRA=66&filtroMuni=22230', '?filtroCRA=54&filtroMuni=22234', '?filtroCRA=54&filtroMuni=22245', '?filtroCRA=53&filtroMuni=22901', '?filtroCRA=53&filtroMuni=22902', '?filtroCRA=60&filtroMuni=22903', '?filtroCRA=72&filtroMuni=22909', '?filtroCRA=42&filtroMuni=44004', '?filtroCRA=34&filtroMuni=44006', '?filtroCRA=75&filtroMuni=44007', '?filtroCRA=52&filtroMuni=44009', '?filtroCRA=38&filtroMuni=44010', '?filtroCRA=30&filtroMuni=44012', '?filtroCRA=51&filtroMuni=44013', '?filtroCRA=32&filtroMuni=44016', '?filtroCRA=50&filtroMuni=44017', '?filtroCRA=49&filtroMuni=44022', '?filtroCRA=38&filtroMuni=44026', '?filtroCRA=40&filtroMuni=44027', '?filtroCRA=32&filtroMuni=44028', '?filtroCRA=49&filtroMuni=44029', '?filtroCRA=46&filtroMuni=44033', '?filtroCRA=40&filtroMuni=44037', '?filtroCRA=48&filtroMuni=44039', '?filtroCRA=36&filtroMuni=44040', '?filtroCRA=45&filtroMuni=44042', '?filtroCRA=42&filtroMuni=44044', '?filtroCRA=52&filtroMuni=44045', '?filtroCRA=47&filtroMuni=44049', '?filtroCRA=46&filtroMuni=44050', '?filtroCRA=32&filtroMuni=44053', '?filtroCRA=30&filtroMuni=44054', '?filtroCRA=50&filtroMuni=44055', '?filtroCRA=45&filtroMuni=44056', '?filtroCRA=44&filtroMuni=44059', '?filtroCRA=42&filtroMuni=44061', '?filtroCRA=36&filtroMuni=44063', '?filtroCRA=37&filtroMuni=44066', '?filtroCRA=43&filtroMuni=44068', '?filtroCRA=42&filtroMuni=44071', '?filtroCRA=41&filtroMuni=44074', '?filtroCRA=28&filtroMuni=44075', '?filtroCRA=33&filtroMuni=44077', '?filtroCRA=43&filtroMuni=44080', '?filtroCRA=40&filtroMuni=44086', '?filtroCRA=50&filtroMuni=44093', '?filtroCRA=36&filtroMuni=44096', '?filtroCRA=36&filtroMuni=44100', '?filtroCRA=41&filtroMuni=44103', '?filtroCRA=44&filtroMuni=44106', '?filtroCRA=42&filtroMuni=44107', '?filtroCRA=39&filtroMuni=44108', '?filtroCRA=27&filtroMuni=44109', '?filtroCRA=45&filtroMuni=44112', '?filtroCRA=30&filtroMuni=44113', '?filtroCRA=33&filtroMuni=44114', '?filtroCRA=32&filtroMuni=44115', '?filtroCRA=36&filtroMuni=44116', '?filtroCRA=52&filtroMuni=44117', '?filtroCRA=42&filtroMuni=44118', '?filtroCRA=27&filtroMuni=44119', '?filtroCRA=27&filtroMuni=44120', '?filtroCRA=41&filtroMuni=44121', '?filtroCRA=50&filtroMuni=44123', '?filtroCRA=44&filtroMuni=44126', '?filtroCRA=35&filtroMuni=44137', '?filtroCRA=40&filtroMuni=44141', '?filtroCRA=38&filtroMuni=44143', '?filtroCRA=37&filtroMuni=44144', '?filtroCRA=36&filtroMuni=44146', '?filtroCRA=47&filtroMuni=44147', '?filtroCRA=36&filtroMuni=44151', '?filtroCRA=33&filtroMuni=44154', '?filtroCRA=35&filtroMuni=44160', '?filtroCRA=34&filtroMuni=44161', '?filtroCRA=27&filtroMuni=44163', '?filtroCRA=30&filtroMuni=44165', '?filtroCRA=48&filtroMuni=44168', '?filtroCRA=45&filtroMuni=44169', '?filtroCRA=38&filtroMuni=44171', '?filtroCRA=34&filtroMuni=44172', '?filtroCRA=36&filtroMuni=44173', '?filtroCRA=52&filtroMuni=44174', '?filtroCRA=32&filtroMuni=44177', '?filtroCRA=33&filtroMuni=44179', '?filtroCRA=32&filtroMuni=44182', '?filtroCRA=44&filtroMuni=44183', '?filtroCRA=41&filtroMuni=44185', '?filtroCRA=39&filtroMuni=44187', '?filtroCRA=31&filtroMuni=44191', '?filtroCRA=30&filtroMuni=44192', '?filtroCRA=35&filtroMuni=44193', '?filtroCRA=39&filtroMuni=44194', '?filtroCRA=28&filtroMuni=44196', '?filtroCRA=27&filtroMuni=44198', '?filtroCRA=30&filtroMuni=44201', '?filtroCRA=31&filtroMuni=44205', '?filtroCRA=38&filtroMuni=44206', '?filtroCRA=29&filtroMuni=44209', '?filtroCRA=27&filtroMuni=44215', '?filtroCRA=28&filtroMuni=44216', '?filtroCRA=48&filtroMuni=44219', '?filtroCRA=48&filtroMuni=44220', '?filtroCRA=43&filtroMuni=44221', '?filtroCRA=29&filtroMuni=44226', '?filtroCRA=27&filtroMuni=44229', '?filtroCRA=43&filtroMuni=44230', '?filtroCRA=45&filtroMuni=44232', '?filtroCRA=27&filtroMuni=44235', '?filtroCRA=31&filtroMuni=44237', '?filtroCRA=37&filtroMuni=44238', '?filtroCRA=30&filtroMuni=44240', '?filtroCRA=43&filtroMuni=44241', '?filtroCRA=35&filtroMuni=44244', '?filtroCRA=47&filtroMuni=44245', '?filtroCRA=39&filtroMuni=44247', '?filtroCRA=29&filtroMuni=44251', '?filtroCRA=27&filtroMuni=44257', '?filtroCRA=44&filtroMuni=44260', '?filtroCRA=29&filtroMuni=44261', '?filtroCRA=41&filtroMuni=44262', '?filtroCRA=28&filtroMuni=44263', '?filtroCRA=28&filtroMuni=44264', '?filtroCRA=31&filtroMuni=44265', '?filtroCRA=32&filtroMuni=44266', '?filtroCRA=5&filtroMuni=50004', '?filtroCRA=18&filtroMuni=50013', '?filtroCRA=23&filtroMuni=50022', '?filtroCRA=24&filtroMuni=50023', '?filtroCRA=10&filtroMuni=50027', '?filtroCRA=26&filtroMuni=50029', '?filtroCRA=17&filtroMuni=50032', '?filtroCRA=25&filtroMuni=50034', '?filtroCRA=24&filtroMuni=50039', '?filtroCRA=18&filtroMuni=50043', '?filtroCRA=11&filtroMuni=50044', '?filtroCRA=4&filtroMuni=50051', '?filtroCRA=18&filtroMuni=50053', '?filtroCRA=7&filtroMuni=50056', '?filtroCRA=23&filtroMuni=50059', '?filtroCRA=16&filtroMuni=50061', '?filtroCRA=22&filtroMuni=50062', '?filtroCRA=18&filtroMuni=50064', '?filtroCRA=13&filtroMuni=50071', '?filtroCRA=4&filtroMuni=50078', '?filtroCRA=26&filtroMuni=50079', '?filtroCRA=25&filtroMuni=50081', '?filtroCRA=17&filtroMuni=50086', '?filtroCRA=5&filtroMuni=50088', '?filtroCRA=2&filtroMuni=50090', '?filtroCRA=21&filtroMuni=50095', '?filtroCRA=5&filtroMuni=50098', '?filtroCRA=20&filtroMuni=50100', '?filtroCRA=19&filtroMuni=50102', '?filtroCRA=1&filtroMuni=50104', '?filtroCRA=18&filtroMuni=50107', '?filtroCRA=17&filtroMuni=50110', '?filtroCRA=16&filtroMuni=50113', '?filtroCRA=9&filtroMuni=50116', '?filtroCRA=48&filtroMuni=50117', '?filtroCRA=15&filtroMuni=50119', '?filtroCRA=14&filtroMuni=50121', '?filtroCRA=18&filtroMuni=50123', '?filtroCRA=13&filtroMuni=50125', '?filtroCRA=13&filtroMuni=50129', '?filtroCRA=14&filtroMuni=50130', '?filtroCRA=24&filtroMuni=50136', '?filtroCRA=12&filtroMuni=50137', '?filtroCRA=24&filtroMuni=50139', '?filtroCRA=11&filtroMuni=50146', '?filtroCRA=18&filtroMuni=50147', '?filtroCRA=4&filtroMuni=50148', '?filtroCRA=11&filtroMuni=50150', '?filtroCRA=20&filtroMuni=50151', '?filtroCRA=10&filtroMuni=50153', '?filtroCRA=10&filtroMuni=50156', '?filtroCRA=6&filtroMuni=50157', '?filtroCRA=9&filtroMuni=50159', '?filtroCRA=9&filtroMuni=50162', '?filtroCRA=22&filtroMuni=50164', '?filtroCRA=17&filtroMuni=50166', '?filtroCRA=9&filtroMuni=50169', '?filtroCRA=1&filtroMuni=50170', '?filtroCRA=9&filtroMuni=50176', '?filtroCRA=3&filtroMuni=50177', '?filtroCRA=8&filtroMuni=50178', '?filtroCRA=24&filtroMuni=50179', '?filtroCRA=7&filtroMuni=50181', '?filtroCRA=8&filtroMuni=50183', '?filtroCRA=19&filtroMuni=50189', '?filtroCRA=6&filtroMuni=50190', '?filtroCRA=13&filtroMuni=50192', '?filtroCRA=1&filtroMuni=50193', '?filtroCRA=1&filtroMuni=50199', '?filtroCRA=5&filtroMuni=50200', '?filtroCRA=9&filtroMuni=50201', '?filtroCRA=12&filtroMuni=50206', '?filtroCRA=20&filtroMuni=50207', '?filtroCRA=11&filtroMuni=50211', '?filtroCRA=16&filtroMuni=50216', '?filtroCRA=11&filtroMuni=50228', '?filtroCRA=4&filtroMuni=50230', '?filtroCRA=11&filtroMuni=50231', '?filtroCRA=53&filtroMuni=50232', '?filtroCRA=6&filtroMuni=50234', '?filtroCRA=3&filtroMuni=50241', '?filtroCRA=3&filtroMuni=50243', '?filtroCRA=16&filtroMuni=50249', '?filtroCRA=9&filtroMuni=50253', '?filtroCRA=14&filtroMuni=50254', '?filtroCRA=17&filtroMuni=50255', '?filtroCRA=4&filtroMuni=50267', '?filtroCRA=11&filtroMuni=50269', '?filtroCRA=2&filtroMuni=50271', '?filtroCRA=15&filtroMuni=50278', '?filtroCRA=6&filtroMuni=50280', '?filtroCRA=9&filtroMuni=50284', '?filtroCRA=1&filtroMuni=50285', '?filtroCRA=8&filtroMuni=50287', '?filtroCRA=26&filtroMuni=50293', '?filtroCRA=15&filtroMuni=50296', '?filtroCRA=12&filtroMuni=50298']
	parametrosIDS=[[74, 22001], [74, 22003], [71, 22007], [61, 22008], [73, 22009], [73, 22016], [1, 22018], [60, 22022], [1, 22023], [74, 22024], [72, 22025], [64, 22027], [53, 22028], [70, 22035], [63, 22040], [74, 22041], [71, 22052], [70, 22053], [69, 22054], [58, 22055], [57, 22057], [74, 22058], [68, 22059], [67, 22060], [66, 22066], [66, 22069], [53, 22076], [59, 22077], [65, 22080], [60, 22082], [59, 22083], [69, 22084], [74, 22088], [73, 22089], [64, 22096], [67, 22099], [63, 22102], [63, 22103], [73, 22105], [66, 22109], [63, 22110], [54, 22112], [57, 22114], [63, 22115], [1, 22116], [62, 22116], [55, 22119], [58, 22124], [65, 22129], [53, 22131], [58, 22135], [62, 22136], [61, 22137], [65, 22142], [69, 22143], [57, 22144], [70, 22157], [60, 22158], [63, 22160], [71, 22167], [68, 22170], [59, 22172], [58, 22174], [57, 22182], [74, 22186], [65, 22187], [60, 22193], [1, 22197], [69, 22200], [74, 22201], [68, 22204], [67, 22205], [57, 22207], [53, 22208], [61, 22213], [62, 22220], [64, 22222], [72, 22225], [55, 22226], [64, 22228], [70, 22229], [66, 22230], [54, 22234], [54, 22245], [53, 22901], [53, 22902], [60, 22903], [72, 22909], [42, 44004], [34, 44006], [75, 44007], [52, 44009], [38, 44010], [30, 44012], [51, 44013], [32, 44016], [50, 44017], [49, 44022], [38, 44026], [40, 44027], [32, 44028], [49, 44029], [46, 44033], [40, 44037], [48, 44039], [36, 44040], [45, 44042], [42, 44044], [52, 44045], [47, 44049], [46, 44050], [32, 44053], [30, 44054], [50, 44055], [45, 44056], [44, 44059], [42, 44061], [36, 44063], [37, 44066], [43, 44068], [42, 44071], [41, 44074], [28, 44075], [33, 44077], [43, 44080], [40, 44086], [50, 44093], [36, 44096], [36, 44100], [41, 44103], [44, 44106], [42, 44107], [39, 44108], [27, 44109], [45, 44112], [30, 44113], [33, 44114], [32, 44115], [36, 44116], [52, 44117], [42, 44118], [27, 44119], [27, 44120], [41, 44121], [50, 44123], [44, 44126], [35, 44137], [40, 44141], [38, 44143], [37, 44144], [36, 44146], [47, 44147], [36, 44151], [33, 44154], [35, 44160], [34, 44161], [27, 44163], [30, 44165], [48, 44168], [45, 44169], [38, 44171], [34, 44172], [36, 44173], [52, 44174], [32, 44177], [33, 44179], [32, 44182], [44, 44183], [41, 44185], [39, 44187], [31, 44191], [30, 44192], [35, 44193], [39, 44194], [28, 44196], [27, 44198], [30, 44201], [31, 44205], [38, 44206], [29, 44209], [27, 44215], [28, 44216], [48, 44219], [48, 44220], [43, 44221], [29, 44226], [27, 44229], [43, 44230], [45, 44232], [27, 44235], [31, 44237], [37, 44238], [30, 44240], [43, 44241], [35, 44244], [47, 44245], [39, 44247], [29, 44251], [27, 44257], [44, 44260], [29, 44261], [41, 44262], [28, 44263], [28, 44264], [31, 44265], [32, 44266], [5, 50004], [18, 50013], [23, 50022], [24, 50023], [10, 50027], [26, 50029], [17, 50032], [25, 50034], [24, 50039], [18, 50043], [11, 50044], [4, 50051], [18, 50053], [7, 50056], [23, 50059], [16, 50061], [22, 50062], [18, 50064], [13, 50071], [4, 50078], [26, 50079], [25, 50081], [17, 50086], [5, 50088], [2, 50090], [21, 50095], [5, 50098], [20, 50100], [19, 50102], [1, 50104], [18, 50107], [17, 50110], [16, 50113], [9, 50116], [48, 50117], [15, 50119], [14, 50121], [18, 50123], [13, 50125], [13, 50129], [14, 50130], [24, 50136], [12, 50137], [24, 50139], [11, 50146], [18, 50147], [4, 50148], [11, 50150], [20, 50151], [10, 50153], [10, 50156], [6, 50157], [9, 50159], [9, 50162], [22, 50164], [17, 50166], [9, 50169], [1, 50170], [9, 50176], [3, 50177], [8, 50178], [24, 50179], [7, 50181], [8, 50183], [19, 50189], [6, 50190], [13, 50192], [1, 50193], [1, 50199], [5, 50200], [9, 50201], [12, 50206], [20, 50207], [11, 50211], [16, 50216], [11, 50228], [4, 50230], [11, 50231], [53, 50232], [6, 50234], [3, 50241], [3, 50243], [16, 50249], [9, 50253], [14, 50254], [17, 50255], [4, 50267], [11, 50269], [2, 50271], [15, 50278], [6, 50280], [9, 50284], [1, 50285], [8, 50287], [26, 50293], [15, 50296], [12, 50298]]
	#parametrosURL = ['?filtroCRA=74&filtroMuni=22001']
	#parametrosIDS=[[74, 22001]]
	#resumen=getResumen('http://preopendata.aragon.es/apps/cras/scrapea_trayecto/?filtroCRA=1&filtroMuni=50199')
	#print 'El resumen es '+str(resumen)
	fResumen=open("resumen.csv","w")
	fRuta=open("ruta.csv","w")
	i=0
	for parametros in parametrosURL:
		print URL+parametros
		resumen=json.loads(getResumen(URL+parametros))
		rutaParseada = json.loads(getRuta(URL+parametros))
		fResumen.write(''+str(parametrosIDS[i][0])+';'+str(parametrosIDS[i][1])+';'+resumen['distancia']+';'+resumen['tiempo']+'\n')
		for paso in rutaParseada:
			fRuta.write(str(parametrosIDS[i][0])+';'+str(parametrosIDS[i][1])+';'+encode(paso['numero_paso'])+';'+encode(paso['descripcion_recorrido'])+';'+encode(paso['distancia_recorrida'])+'\n')
			#print paso['descripcion_recorrido']

		i=i+1
	fResumen.close()
	fRuta.close()
main()