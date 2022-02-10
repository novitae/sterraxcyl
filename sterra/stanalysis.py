from re import findall

# Coeff:
_PERSONNAL_PRIVATE_IN_DESC = 2
_PERSONNAL_PRIVATE_IN_NAME = 3
_PERSONNAL_IS_PRIVATE = 6
_PERSONNAL_FOLLOWERS_COUNT = 4
_PERSONNAL_FOLLOWING_COUNT = 1
_PERSONNAL_EXTERNAL_URL = 1
_PERSONNAL_IS_PROFESSIONAL = 3
_PERSONNAL_IS_BUSINESS = 3
_PERSONNAL_IS_VERIFIED = 3
_PERSONNAL_POSTS = 3

_INTERESTS_PRIVATE_IN_DESC = 1
_INTERESTS_PRIVATE_IN_NAME = 1
_INTERESTS_IS_PRIVATE = 7
_INTERESTS_FOLLOWERS_COUNT = 7
_INTERESTS_FOLLOWING_COUNT = 1
_INTERESTS_EXTERNAL_URL = 3
_INTERESTS_IS_PROFESSIONAL = 4
_INTERESTS_IS_BUSINESS = 5
_INTERESTS_IS_VERIFIED = 3
_INTERESTS_POSTS = 2

class _analysis:
    def __init__(self,_:object, data:list, **kwargs) -> None:
        self._ = _
        self.data = data
        
        self.invert = kwargs.get("invert")
        self.ignore_over = kwargs.get("ignore_over") if kwargs.get("ignore_over") else 10000
        self.pctg = kwargs.get("pctg") if kwargs.get("pctg") else 0
        self.size = kwargs.get("size") if kwargs.get("size") else len(self.data)

    def __call__(self, target:str) -> list:
        return self._order(getattr(self, target)())

    def _order(self, l:list):
        order = sorted(l, key=lambda item: item['%'], reverse=self.invert)
        order = order[-self.size:]
        return [x for x in order if x['%'] >= self.pctg]

    def _dictFormat(self, d:dict) -> dict:
        rtr = {}
        for k, v in d.items():
            if v in ["True","False","None"]:
                v = True if v == "True" else False if v == "False" else None
            if k in ["posts","followers","following","mutual_followed_by_count"]:
                rtr[k] = 0 if v is None else int(v)
            else:
                rtr[k] = v
        return rtr

    def personnal(self) -> list:
        """Data analysis to get probas of personnal accounts"""
        def fais_le_boulot(acc:dict) -> dict:
            """Objective probabilities"""
            probas = []
            repv = r'([pP]{1,4}[rR]{1,4}([iI]{0,4}[vV]{1,4}[aAéÉeE]{1,10}[tT]{0,4}[eE]{0,4}|[vV]{1,4}[tT]{1,4}[eE]{0,9})|[pP][vV]{1,4})' # PRIVATE / PRIVÉ
            
            if acc['biography']:
                if findall(repv, acc['biography']):
                    probas += [100]*_PERSONNAL_PRIVATE_IN_DESC
            
            if acc["full_name"]:
                if findall(repv, acc["full_name"]):
                    probas += [100]*_PERSONNAL_PRIVATE_IN_NAME
            
            probas += [100 if acc['is_private'] else 0]*_PERSONNAL_IS_PRIVATE
            probas += [100 if acc['followers'] < (self.ignore_over / 15) else (50 if acc['followers'] < self.ignore_over else 0)]*_PERSONNAL_FOLLOWERS_COUNT
            probas += [100 if acc['following'] < 50 else (50 if acc["following"] < 500 else 0)]*_PERSONNAL_FOLLOWING_COUNT
            probas += [0 if acc['external_url'] else 100]*_PERSONNAL_EXTERNAL_URL

            """Subjective probbailities"""
            sub = 0
            for i in probas:
                sub += i
            SUB = int(sub / len(probas))
            
            probas += [100 if not acc['is_professional_account'] else (50 if SUB > 75 else 0)]*_PERSONNAL_IS_PROFESSIONAL
            probas += [100 if not acc['is_business_account'] else (50 if SUB > 75 else 0)]*_PERSONNAL_IS_BUSINESS
            probas += [100 if not acc['is_verified'] else (100 if SUB > 90 else 0)]*_PERSONNAL_IS_VERIFIED
            probas += [100 if acc['posts'] > 50 and SUB > 85 else 0]*_PERSONNAL_POSTS

            final = 0
            for p in probas:
                final += p
            final /= len(probas)
            final = final if final < 100 else 99

            retour = {"%": final}
            retour.update(acc)
            return retour

        return [fais_le_boulot(self._dictFormat(acc)) for acc in self.data if acc["id"]]

    def interests(self) -> list:
        """"""
        def fais_le_boulot(acc:dict) -> dict:
            """Objective probabilities"""
            probas = []
            repv = r'([pP]{1,4}[rR]{1,4}([iI]{0,4}[vV]{1,4}[aAéÉeE]{1,10}[tT]{0,4}[eE]{0,4}|[vV]{1,4}[tT]{1,4}[eE]{0,9})|[pP][vV]{1,4})' # PRIVATE / PRIVÉ
            
            if acc['biography']:
                if findall(repv, acc['biography']):
                    probas += [0]*_INTERESTS_PRIVATE_IN_DESC
            
            if acc["full_name"]:
                if findall(repv, acc["full_name"]):
                    probas += [0]*_INTERESTS_PRIVATE_IN_NAME

            probas += [0 if acc['is_private'] else 100]*_INTERESTS_IS_PRIVATE
            probas += [100 if acc['followers'] > self.ignore_over else (50 if acc['followers'] > (self.ignore_over/2) else 0)]*_INTERESTS_FOLLOWERS_COUNT
            probas += [100 - ((acc['following'] if acc['following'] < 1500 else 1500) * 100) / 1500]*_INTERESTS_FOLLOWING_COUNT
            probas += [0 if acc['external_url'] else 100]*_INTERESTS_EXTERNAL_URL
            probas += [100 if not acc['is_verified'] else 0]*_INTERESTS_IS_VERIFIED
            probas += [100 if acc['posts'] > 50 else 0]*_INTERESTS_POSTS

            """Subjective probbailities"""
            sub = 0
            for i in probas:
                sub += i
            SUB = int(sub / len(probas))
            
            probas += [100 if acc['is_professional_account'] else (50 if SUB > 75 else 0)]*_INTERESTS_IS_PROFESSIONAL
            probas += [100 if acc['is_business_account'] else (50 if SUB > 75 else 0)]*_INTERESTS_IS_BUSINESS

            final = 0
            for p in probas:
                final += p
            final /= len(probas)
            final = final if final <= 100 else 99

            retour = {"%": final}
            retour.update(acc)
            return retour

        return [fais_le_boulot(self._dictFormat(acc)) for acc in self.data if acc["id"]]