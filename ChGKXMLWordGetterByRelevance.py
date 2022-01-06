import requests, codecs, datetime
import xml.etree.ElementTree as Et
from os import listdir
outputName = "rezRelXML.txt"
linkList = "outXML.txt"
default_date = datetime.datetime(2000, 1, 1)


def precalc():
    stream = None
    cnt = 0

    def rec(s=""):
        if s != "":
            s += "/"
        url = 'https://db.chgk.info/tour/%sxml'
        r = requests.get(url % s)
        root = Et.fromstring(r.text)    
        ff = root.findall("tour/TextId")
        if len(ff) == 0:
            nonlocal stream, cnt
            stream.write(s + ";")
            cnt += 1
            if cnt % 25 == 0:
                print(cnt)
        else:
            for i in ff:
                rec(i.text)
    
    try:
        stream = codecs.open(linkList, "w", "utf-8")
        rec()
    finally:
        stream.close()



def getRez():
    fi = codecs.open(outputName, "r", "utf-8")
    a = fi.read().split(';\n')
    fi.close()
    if len(a[0]) == 0 and len(a) == 1:
        return dict()

    d = {}
    for i in a:
        q = " ".join(i.split(' ')[:-1])
        if ord(q[0]) == 10:
            q = q[1:]
        w = int(i.split(' ')[-1])
        d[q] = w
    return d


def get_all(text):
    def up(ans):
        ans = ans.strip().replace("\"", "").replace('\'', "")
        while ans.endswith('.'):
            ans = ans[:-1]
        return ans.upper()

    root = Et.fromstring(text)
    ff = root.findall("question")
    num = len(ff)
    if num < 0:
        return [], 0

    beg = datetime.datetime(1989, 1, 1)
    d = root.find("PlayedAt")
    dat = None
    try:
        if d is None or d.text is None:
            d = root.find("CreatedAt")
            if d is None or d.text is None:
                dat = default_date
            else:
                dat = datetime.datetime(*[int(i) for i in d.text.split("-")])
        else:
            dat = datetime.datetime(*[int(i) for i in d.text.split("-")])
    except ValueError:
        dat = default_date

    rez = []
    import re
    si_re = "^\s*1\.\s*(.*)\s*2\.\s*(.*)\s*3\.\s*(.*)\s*4\.\s*(.*)\s*5\.\s*(.*)\s*$"
    dup_re = "^\s*1\.\s*(.*)\s*2\.\s*(.*)\s*$"
    bl_re = "^\s*1\.\s*(.*)\s*2\.\s*(.*)\s*3\.\s*(.*)\s*$"
    r = re.compile(si_re)
    for i in ff:
        ans = i.find("Answer").text.replace("\n", ' ')
        if re.match(si_re, ans):
            rs = re.search(si_re, ans)
            for i in range(5):
                rez.append(up(rs.group(i + 1)))
        elif re.match(dup_re, ans):
            rs = re.search(dup_re, ans)
            for i in range(2):
                rez.append(up(rs.group(i + 1)))
        elif re.match(bl_re, ans):
            rs = re.search(bl_re, ans)
            for i in range(3):
                rez.append(up(rs.group(i + 1)))
        else:
            rez.append(up(ans))

    return rez, (dat - beg).days


def pocket(s):
    if s is None:
        s = ""
    url = 'https://db.chgk.info/tour/%sxml'
    r = requests.get(url % s)
    return get_all(r.text)
    

def save_dict(d):
    ret = []
    for i in d:
        ret.append([d[i], i])
    rez = sorted(ret, key=lambda x: -x[0])
    with codecs.open(outputName, "w", "utf-8") as stream:
        stream.write(";\n".join(i[1] + ' ' + str(i[0]) for i in rez))
        stream.close()


def main(d):
    try:
        K1 = 0
        # K1 = 3500
        #K = 600
        K = 100
        fi = open(linkList, "r")
        a = fi.read().split(';')
        fi.close()
        t = K1
        for i in a[K1: K1 + K]:
            b, ad = pocket(i)
            for j in b:
                if len(j) < 2:
                    continue
                try:
                    d[j] += ad
                except Exception:
                    d[j] = ad
            t += 1
            if t % 20 == 0:
                print(t)
    except KeyboardInterrupt:
        pass
    save_dict(d)



def main_local():
    d = dict()
    for i in listdir("src"):
        fi = codecs.open("src/" + i, "r", "utf-8")
        txt = fi.read()
        fi.close()
        b, ad = get_all(txt)
        for j in b:
            if len(j) < 2:
                continue
            d[j] = d.get(j, 0) + ad
    save_dict(d)


# a = getRez()
# main(a)
# precalc()
main_local()

# fi = codecs.open("src/" + "provi15.2.xml", "r", "utf-8")  # duplet
# fi = codecs.open("src/" + "grishov.xml", "r", "utf-8")  # svoyak
# fi = codecs.open("src/" + "otv04ek.xml", "r", "utf-8")  # svoyak with /n
# fi = codecs.open("src/" + "izsup08l.3.xml", "r", "utf-8")  # blitz
# txt = fi.read()
# fi.close()
# print(get_all(txt))