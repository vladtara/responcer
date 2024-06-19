import os
import pathlib

print(os.path.join(os.path.dirname(__file__), "templates"))
print(__file__)
print(pathlib.Path(__file__).parent.parent / "templates")

print(os.getcwd())
