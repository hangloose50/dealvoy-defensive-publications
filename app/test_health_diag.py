# test_health_diag.py

import inspect

print("health module path:", uh.__file__)
print("\n----- First 20 lines of that file -----\n")
src = inspect.getsource(uh).splitlines()
print("\n".join(src[:20]))
