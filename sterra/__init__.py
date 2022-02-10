from sterra.sterools import checkPaths
from sterra._outputs_ import _

created_path = checkPaths()
if created_path:
    for path in created_path:
        _().p(path, logo="Python")