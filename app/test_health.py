# test_health.py

from app import utils
import inspect

print(">>> health module loaded from:", uh.__file__)
print("\n>>> First 60 lines of utils/health.py:\n")
source = inspect.getsource(uh)
print("\n".join(source.splitlines()[:60]))

from app.utils.health import init_dashboard

def main():
    gc, sh = init_dashboard()
    print("Final sheet ID:", sh.id)
    print("Header row:", sh.get_worksheet(0).row_values(1))

if __name__ == "__main__":
    main()
