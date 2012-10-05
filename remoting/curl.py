import pycurl
import StringIO

def curl(url, headers=None, socks_host=None, socks_port=None):
    # if socks_port is given, it should be an integer
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)

    if socks_host or socks_port:
        c.setopt(pycurl.PROXY, socks_host or 'localhost')
        c.setopt(pycurl.PROXYPORT, socks_port or 5090)
        c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)

    if headers:
        header_list = ['%s: %s' % (key, val) for key, val in headers.items()]
        c.setopt(pycurl.HTTPHEADER, header_list)

    output = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, output.write)
    c.perform()

    return output.getvalue()
