import numpy as np

m = re.search(patt, "ababa")
for i in range(0, 4):
  print(f"group({i}):", m.group(i))