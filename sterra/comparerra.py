class _compare:
    def __init__(self,*args) -> None:
        self._, self.l1, self.l2 = args
        try:
            self.idl = [i["id"] for i in self.l1]
        except KeyError:
            self._.r(KeyError("The input list must contain (at least) the key \"id\""))

    def _not_twice(self,l:list[dict]) -> list[dict]:
        r = []
        for i in l:
            if i not in r:
                r.append(i)
        return r

    def common_usernames(self) -> list[dict]:
        """Return list of not common dicts between two list of dicts"""
        return self._not_twice([d for d in self.l2 if d["id"] in self.idl])
    
    def not_common_usernames(self) -> list[dict]:
        """Return list of not common dicts between two list of dicts"""
        return self._not_twice([d for d in self.l2 if d["id"] not in self.idl])

    def detail_common(self) -> list[dict]:
        """Returns list of dict"""
    #+ faire un detail_common;
    #  il retourne non seulement un dict des commons mais aussi un dict des commons qui ont des différences entre la première et la seconde liste 