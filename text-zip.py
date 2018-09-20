import zlib
import base64

text = open('example.txt','rb').read()

data = zlib.compress(text, zlib.Z_BEST_COMPRESSION)
tzip = base64.b64encode(data)

f = open('compressed.txt','wb')
f.write(tzip)
f.close()

data = base64.b64decode(tzip)
text = zlib.decompress(data)

f = open('decompressed.txt','wb')
f.write(text)
f.close()

print('Compression Ratio: {0:0.2f}'.format(len(tzip)/len(text)))
