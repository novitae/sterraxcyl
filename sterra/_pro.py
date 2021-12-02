import re

class babilities:
    def __init__(self, ld, pa, io = 10000, dd = False, pt = 0, sz=None) -> dict:
        '''- ld: List of dics
        - pa: Probability asked -> personnal - interests
        - io: Ignore over -> Amount of followers over wich the account is considerated as non-personnal
        - dd: Return by descending order ? True - False
        - pt: Percentage
        - sz: Size of the list returned'''

        if type(ld) != list: raise TypeError('InputTypeException: "lofdic" must be a list.')
        if ld == []: raise ValueError('InputTypeException: "lofdic" must be a not empty list.')
        if type(ld[0]) != dict: raise TypeError('elements of "lofdic" must be dictionnaries.')
        if type(io) != int: raise ValueError('"ignore_over" must be an integer.')
        
        self.ld = ld
        self.pa = pa
        self.io = io
        self.pt = pt
        self.dd = False if dd is True else True
        self.sz = sz if sz is not None else len(ld)

    def sort(self, l):
        srt = sorted(l, key=lambda item: item['%'], reverse=self.dd)
        srt = [x for x in srt if int(x['%']) >= self.pt]
        return srt[:self.sz]

    def coef(p, c, v): #c = coefficient
        for _ in range(c):
            p.append(v)
        return p

    def personnal(self):
        o = []
        for D in self.ld:
            try:
                d = {}
                for key in list(D.keys()):
                    try:
                        d[key] = int(D[key])
                    except (ValueError, TypeError):
                        d[key] = D[key]

                '''Objective probababilities'''
                p = []
                repv = r'([pP]{1,4}[rR]{1,4}([iI]{0,4}[vV]{1,4}[aAéÉeE]{1,10}[tT]{0,4}[eE]{0,4}|[vV]{1,4}[tT]{1,4}[eE]{0,9})|[pP][vV]{1,4})' # PRIVATE / PRIVÉ
                if d['biography'] != None:
                    if re.findall(repv, str(d['biography'])) != []:
                        p = babilities.coef(p, c=2, v=100)

                if d['name'] != None:
                    if re.findall(repv, str(d['name'])) != []:
                        p = babilities.coef(p, c=2, v=100)

                if re.findall(repv, str(d['username'])) != []:
                    p = babilities.coef(p, c=2, v=100)
                p = babilities.coef(p, c=4, v=(100 if d['is_private'] else 0))
                p = babilities.coef(p, c=5, v=(100 - (int(d['followers'] if int(d['followers']) < self.io else self.io) * 100) / self.io))
                p = babilities.coef(p, c=1, v=(100 - (int(d['following'] if int(d['following']) < 1500 else 1500) * 100) / 1500))
                p = babilities.coef(p, c=1, v=(0 if d['external_url'] != None else 100))

                '''Subjective probababilities
                Data is added in function of the first estimations'''
                sub = 0
                for i in p:
                    sub += i
                SUB = int(sub / len(p))

                p = babilities.coef(p, c=1, v=100) if not d['is_professional_account'] else babilities.coef(p, c=1, v=(100 if SUB > 75 else 0))
                p = babilities.coef(p, c=1, v=100) if not d['is_business_account'] else babilities.coef(p, c=1, v=(100 if SUB > 75 else 0))
                p = babilities.coef(p, c=2, v=100) if not d['is_verified'] else babilities.coef(p, c=3, v=(100 if SUB > 60 else 0))
                p = babilities.coef(p, c=2, v=(100 if int(d['posts']) > 50 and SUB > 92 else 0))

                t = 0
                for i in p: t += i
                T = int(t / len(p))
                T = T if T != 100 else 99

                oa = {'%': int(str(T if T > 9 else '0'+str(T)))}
                kys = list(d.keys())
                for k in range(len(kys)):
                    oa[kys[k]] = list(d.values())[k]
                o.append(oa)

            except TypeError:
                print('    -> TypeError (non fatal), this error at line 59/58 of _pro.py is well known\n       It is about a corrupted value during the export that placed a\n       null element that probbaility module can\'t read. It will be fixed.')
                pass
        return o

    def interests(self):
        pass

    def d(self):
        '''Destination'''
        if self.pa == 'personnal':
            return babilities.sort(self, babilities.personnal(self))
        elif self.pa == 'interests':
            return babilities.sort(self, babilities.interests(self))