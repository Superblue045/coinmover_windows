import sys
sys.path.append(".")

from access.bybit_data_access import bybit_perps


# Test : OK
for p in bybit_perps:
    print(p.Name)