class parentException(Exception):
    def __init__(self, *args: object) -> None:
        self.args = args
        super().__init__(*args)

    def __str__(self) -> str:
        return ": ".join(self.args)

#+ essayer de formuler les erreurs avec de la couleur avant qu'elles ne soient print

# Global
class RateLimitError(parentException):
    def __init__(self,msg:str="") -> None:
        super().__init__(f"""Rate limit {f"at {msg}" if msg else msg} blocks the program. Wait a bit, or change of login account.""")

# Defaut
class UserNotFoundError(parentException):
    def __init__(self,userPointer:str) -> None:
        super().__init__(f"User not found. Verify its {userPointer}.")
class PrivateAccError(parentException):
    def __init__(self,u:str=None) -> None:
        super().__init__((u if u else "Your target")+" is a private account that you're not following.")
class NoFollowError(parentException):
    def __init__(self,m:str=None) -> None:
        super().__init__(m if m else "Your target has not followers nor following.")
class MutualsError(parentException):
    def __init__(self,m:str) -> None:
        super().__init__(m)
class BadListOfDictError(parentException):
    def __init__(self,m:str) -> None:
        super().__init__(f"The input list doesn't contain the key \"{m}\" used for the analysis.")
class NoSuchLogoError(parentException):
    def __init__(self,m:str) -> None:
        super().__init__(f"The logo \"{m}\" doesn't exist.")
class ExportDataError(parentException):
    def __init__(self,m:str) -> None:
        super().__init__(f"The file can't be exported; {m}.")
class EmptyResultError(parentException):
    def __init__(self) -> None:
        super().__init__(f"The result is empty.")

# Custom
class LoginError(parentException):
    pass