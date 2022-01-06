import requests, codecs
import xml.etree.ElementTree as Et
import os.path
import threading
import time
source = "src/%s.xml"

from os import listdir


def rec(s="", force=False):
	try:
		ss = s
		if ss != "":
			ss += "/"
		txt = None
		if not force and os.path.isfile(source % s):
			with codecs.open(source % s, "r", "utf-8") as stream:
				txt = stream.read()
				stream.close()
		else:
			url = 'https://db.chgk.info/tour/%sxml'
			r = requests.get(url % ss)
			if r.status_code != 200:
				fi = open("bad.txt", "a")
				fi.write(s + "\n")
				fi.close()
				return
			txt = r.text
			with codecs.open(source % s, "w", "utf-8") as stream:
				stream.write(txt)
		stream.close()
		root = Et.fromstring(txt)
		ff = root.findall("tour/TextId")
		if len(ff) == 0:
			return
		for i in ff:
			time.sleep(0.1)
			threading.Thread(target=rec, args=(i.text, force)).start()
	except Exception as e:
		print(e, type(e))
		fi = open("bad.txt", "a")
		fi.write(s + "\n")
		fi.close()
		exit(0)


def check():
	for i in listdir("src"):
		try:
			fi = codecs.open("src/" + i, "r", "utf-8")
			txt = fi.read()
			fi.close()
			root = Et.fromstring(txt)
		except Exception as e:
			print(e)
			print(i)
			rec(i[:-4])


check()