import sys
import doctest
from http009 import http_response

sys.setrecursionlimit(10000)

# NO ADDITIONAL IMPORTS!

CHUNK_SIZE = 8192

def download_file(loc, cache=None):
    """
    Yield the raw data from the given URL, in segments of CHUNK_SIZE bytes.

    If the request results in a redirect, yield bytes from the endpoint of the
    redirect.

    If the given URL represents a manifest, yield bytes from the parts
    represented therein, in the order they are specified.

    Raises a RuntimeError if the URL can't be reached, or in the case of a 500
    status code.  Raises a FileNotFoundError in the case of a 404 status code.
    """

    # Try implementing cache as dictionary mapping "url" -> file data

    # Hint: consider making another function to handle manifests
    # Hint: b''.decode("utf-8") decodes a bytestring to a python string
    #       use this when deciding what URLs in the manifest to download again
    if cache == None:
        cache = {}
    try:
        r = http_response(loc)
    except:
        raise RuntimeError
    if r.status == 404:
        raise FileNotFoundError
    if r.status == 500:
        raise RuntimeError
    if r.status == 301 or r.status == 302 or r.status == 307:
        for result in download_file(r.getheader('location')):
            yield result
    elif r.getheader('content-type') == 'text/parts-manifest' or loc[-6:] == '.parts':
        text = r.read()
        # print(text)
        clumps = text.split(b'--')
        file_worked = False
        for clump in clumps:
            #For each group of links, create a list of all the urls.
            to_cache = False
            if b'(*)' in clump:
                to_cache = True
            urls = clump.split(b'\n')
            urls_to_remove = []
            for i in range(len(urls.copy())):
                if urls[i] == b'':
                    urls_to_remove.append(urls[i])
                else:
                    urls[i] = urls[i].decode("utf-8")
            for removal in urls_to_remove:
                urls.remove(removal)
            tag = False
            #Checks if the url is in cache, if so, yield from the cache
            for url in urls:
                if url in cache and to_cache:
                    yield from cache[url]
                    tag = True
                    break
            if tag:
                continue
            #Yields results from file and adds to cache is
            for url in urls:
                if not file_worked:
                    try:
                        add_to_cache = []
                        for result in download_file(url, cache):
                            add_to_cache.append(result)
                            yield result
                        if to_cache:
                            cache[url] = add_to_cache
                        file_worked = True
                    except:
                        continue
                file_worked = False
                break
    else:
        result = None
        while result != b'':
            result = r.read(CHUNK_SIZE)
            if result == b'':
                break
            # cache[loc].add(result)
            yield result



def files_from_sequence(stream):
    """
    Yield the files from the sequence in the order they are specified.

    stream: the return value (a generator) of a download_file
                        call that represents a file sequence
    """

    # Use next(stream) to yield the more data.
    ba = bytearray()
    try:
        while True:
            while len(ba) < 4:
                ba.extend(next(stream))
            length_of_bytes = int.from_bytes(ba[:4], byteorder = 'big')
            ba = ba[4:]
            while len(ba) < length_of_bytes:
                ba.extend(next(stream))
            yield ba[:length_of_bytes]
            ba = ba[length_of_bytes:]
    except:
        return







if __name__ == '__main__':
    """
    Remember you can use python3 gui.py URL_NAME to test your images!
    """
    # print(list(download_file('http://scripts.mit.edu/~6.009/lab9/delayed.py/happycat.png\n')))
    r = http_response('http://hz.mit.edu/009_lab9/cat_poster.jpg-part0')
    print(r.read())
    print(r.status)
    pass
