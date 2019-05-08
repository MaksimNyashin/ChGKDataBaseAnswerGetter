import requests
import re
import codecs

def precalc():
    url = 'https://db.chgk.info/tree'
    r = requests.get(url)
    #with open('test.html', 'wb') as fo:
        #fo.write(r.text.encode('utf-8'))
    reg = re.compile('<a href="/tour([A-Za-z0-9/]+)">')
    a = re.findall(reg, r.text)
    '''try:
        a = list(map(lambda s: s[9: -2], ))
    except Exception:
        print(a)'''
    fo = open("out.txt", "w")
    fo.write(";".join(a))
    fo.close()

def pocket(s):
    import requests
    url = 'https://db.chgk.info/tour' + s
    r = requests.get(url).text
    #with open('test.html', 'wb') as fo:
        #fo.write(r.encode('utf-8'))
    #reg = re.compile('<p>(<strong class="Answer">)?Ответ:(</strong>)? *"?([A-Za-zА-Яа-я0-9: /-]+)[^A-Za-zА-Яа-я0-9: /-][^<]*</p>')
    sss = '<p>\s*(<strong class="Answer">)?\s*(<i>)?\s*ответ:\s*(</strong>)?\s*(</i>)?\s*(\[.*\])*\s*(\(.*\))*\s*"*\s*([^ <"][A-Za-zА-Яа-я0-9: /-/.]+[^ /.",])\s*(\[.*\])*\s*(\(.*\))*[^A-Za-zА-Яа-я0-9:/-][^<]*</p>'
    reg = re.compile(sss, re.I)
    a = re.findall(reg, r)
    a = list(map(lambda s: s[6].strip().upper(), a))
    return a

def getRez():
    fi = codecs.open("rez.txt", "r", "utf-8")
    a = fi.read().split(';\n')
    fi.close()
    d = {}
    for i in a:
        q = " ".join(i.split(' ')[:-1])
        #print(i)
        if ord(q[0]) == 10:
            q = q[1:]
        w = int(i.split(' ')[-1])
        d[q] = w
    return d

def main(d):
    #K1 = 3500
    K1 = 3500
    #K = 600
    K = 600
    fi = open("out.txt", "r")
    a = fi.read().split(';')
    fi.close()
    #d = {}
    t = K1
    for i in a[K1: K1 + K]:
        b = pocket(i)
        for j in b:
            if len(j) < 2:
                continue
            try:
                d[j] += 1
            except Exception:
                d[j] = 1
        t += 1
        if t % 20 == 0:
            print(t)
    ret = []
    for i in d:
        ret.append([d[i], i])
    rez = sorted(ret, key=lambda x: -x[0])
    with codecs.open("rez.txt", "w", "utf-8") as stream:
        stream.write(";\n".join(i[1] + ' ' + str(i[0]) for i in rez))
        stream.close()
    #print(";\n".join(i[1] + ' ' + str(i[0]) for i in rez))

a = getRez()
'''for i in a:
    if a[i] > 15:
        print(i, a[i])'''
main(a)
