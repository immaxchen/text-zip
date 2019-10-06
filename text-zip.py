import os, zlib, base64, argparse
from hashlib import scrypt
from cryptography.fernet import Fernet

def get_agent(password):
    key = base64.urlsafe_b64encode(scrypt(password.encode(), salt=b's'*16, n=2**14, r=8, p=1, dklen=32))
    return Fernet(key)

def compress(filename, verbose=False, password=None):
    with open(filename, 'rb') as f:
        data = f.read()
    zipped = zlib.compress(data, zlib.Z_BEST_COMPRESSION)

    if password:
        text = get_agent(password).encrypt(zipped)
    else:
        text = base64.urlsafe_b64encode(zipped)

    with open('compressed.txt', 'wb') as f:
        f.write(text)

    if verbose:
        print('Compression ratio: {0:0.2f}'.format(len(text)/len(data)))

def extract(filename, verbose=False, password=None):
    with open(filename, 'rb') as f:
        text = f.read()

    if password:
        zipped = get_agent(password).decrypt(text)
    else:
        zipped = base64.urlsafe_b64decode(text)

    data = zlib.decompress(zipped)
    with open('decompressed.dat', 'wb') as f:
        f.write(data)

    if verbose:
        print('Compression ratio: {0:0.2f}'.format(len(text)/len(data)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='filename to compress or extract')
    parser.add_argument('-c', '--compress', help='compress the file', action='store_true')
    parser.add_argument('-x', '--extract', help='extract the file', action='store_true')
    parser.add_argument('-v', '--verbose', help='display information', action='store_true')
    parser.add_argument('-p', '--password', help='password protection')
    args = parser.parse_args()

    if args.compress & args.extract:
        parser.error('--compress and --extract can not be given at the same time')

    if args.compress:
        compress(args.filename, args.verbose, args.password)

    if args.extract:
        extract(args.filename, args.verbose, args.password)
