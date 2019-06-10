import requests, re, codecs
outputName = "rezRel.txt"

def pocket(s):
    import requests, datetime
    url = 'https://db.chgk.info/tour' + s
    r = requests.get(url).text
    #with open('test.html', 'wb') as fo:
        #fo.write(r.encode('utf-8'))
    #reg = re.compile('<p>(<strong class="Answer">)?Ответ:(</strong>)? *"?([A-Za-zА-Яа-я0-9: /-]+)[^A-Za-zА-Яа-я0-9: /-][^<]*</p>')
    ssd = '([12][09][0129][0-9])\-([01][0-9])\-([0123][0-9])'
    sss = '<p>\s*(<strong class="Answer">)?\s*(<i>)?\s*ответ:\s*(</strong>)?\s*(</i>)?\s*(\[.*\])*\s*(\(.*\))*\s*"*\s*([^ <"\.][A-Za-zА-Яа-я0-9: /-/.]+[^ /.",\(])\s*(\[.*\])*\s*(\(.*\))*[^A-Za-zА-Яа-я0-9:/-][^<]*</p>'
    reg = re.compile(sss, re.I)
    regD = re.compile(ssd)
    a = re.findall(reg, r)
    a = list(map(lambda s: s[6].strip().upper(), a))
    c = re.findall(regD, r)
    y, m, d = 1990, 1, 1
    try:
        y, m, d = map(int, c[0])
    except IndexError:
        pass
    d = datetime.datetime(y, m, d)
    beg = datetime.datetime(1989, 1, 1)
    delta = d - beg
    rez = delta.days
    return (a, rez)

def getRez():
    fi = codecs.open(outputName, "r", "utf-8")
    a = fi.read().split(';\n')
    if len(a[0]) == 0 and len(a) == 1:
        return dict()
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
    ret = []
    for i in d:
        ret.append([d[i], i])
    rez = sorted(ret, key=lambda x: -x[0])
    with codecs.open(outputName, "w", "utf-8") as stream:
        stream.write(";\n".join(i[1] + ' ' + str(i[0]) for i in rez))
        stream.close()
    #print(";\n".join(i[1] + ' ' + str(i[0]) for i in rez))

a = getRez()
#a = {}
main(a)
