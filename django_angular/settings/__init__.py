import sys

try:
    from .production import *
except:
    try:
        from .testing import *
    except:
        from .development import *
    