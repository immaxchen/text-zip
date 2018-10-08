import zlib
import base64
import argparse

def compress(filename, verbose=False):
    file = open(filename,'rb').read()
    data = zlib.compress(file, zlib.Z_BEST_COMPRESSION)
    text = base64.b64encode(data)

    f = open('compressed.txt','wb')
    f.write(text)
    f.close()

    if verbose:
        print('Compression ratio: {0:0.2f}'.format(len(text)/len(file)))

def extract(filename, verbose=False):
    text = open(filename,'rb').read()
    data = base64.b64decode(text)
    file = zlib.decompress(data)

    f = open('decompressed.dat','wb')
    f.write(file)
    f.close()

    if verbose:
        print('Compression ratio: {0:0.2f}'.format(len(text)/len(file)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='filename to compress or extract')
    parser.add_argument('-c', '--compress', help='compress the file', action='store_true')
    parser.add_argument('-x', '--extract', help='extract the file', action='store_true')
    parser.add_argument('-v', '--verbose', help='display information', action='store_true')
    args = parser.parse_args()

    if args.compress & args.extract:
        parser.error('--compress and --extract can not be given at the same time')

    if args.compress:
        compress(args.filename, args.verbose)

    if args.extract:
        extract(args.filename, args.verbose)
