import sys
from importlib.metadata import version, PackageNotFoundError

print("python", sys.version.split()[0])
for pkg in ["pandas", "polars", "pyarrow", "requests", "psycopg[binary]", "pytest", "pyspark"]:
    try:
        print(pkg, version(pkg))
    except PackageNotFoundError:
        print(pkg, "not installed")