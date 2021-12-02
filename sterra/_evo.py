class lutio:
    def __init__(self, f1, f2, arg) -> None:
        self.f1 = f1
        self.f2 = f2
        self.rg = arg

    def not_twice(l) -> list:
        r = []
        for i in l:
            if i not in r:
                r.append(i)
        return r

    def n(self) -> list:
        '''comparing the id of the account to avoid not equal dict between default and all-infos datas,
        and to avoid not same account between two list if an username changed its biography or something else'''
        if self.rg == 'common_usernames':
            common_usernames = []
            u2ids = [U['id'] for U in self.f2]
            for u1 in self.f1:
                if u1['id'] in u2ids:
                    common_usernames.append(u1)
            
            return lutio.not_twice(common_usernames)
        
        elif self.rg == 'not_common_usernames':
            not_common_usernames = []
            u2ids = [U['id'] for U in self.f2]
            for u1 in self.f1:
                if not u1['id'] in u2ids:
                    not_common_usernames.append(u1)
            
            return lutio.not_twice(not_common_usernames)