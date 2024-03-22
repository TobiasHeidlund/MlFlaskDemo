import bz2
import gzip
import lzma
import pickle

filename = 'finalized_model.sav'
try:
    data = pickle.load(open(filename, 'rb'))
except EOFError as e:
    print("Error loading pickled data:", e)



with gzip.open("gzip_test.gz", "wb") as f:
    pickle.dump(data, f)

with bz2.BZ2File('bz2_test.pbz2', 'wb') as f:
    pickle.dump(data, f)

with lzma.open("lzma_test.xz", "wb") as f:
    pickle.dump(data, f)
