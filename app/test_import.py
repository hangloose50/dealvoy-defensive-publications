import test_
print(" sys.path:", *sys.path, sep="\n  - ")

from app import app
print("\nLoaded schemas from:", app.schemas.__file__)

print("\nAvailable Webhook* classes:",
      [name for name in dir(app.schemas) if name.startswith("Webhook")])

