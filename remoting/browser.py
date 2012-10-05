import subprocess
from remoting import timeout

def phantomjs(script, args, socks_proxy_port=None, timelimit=60):
    # returns the <returncode> returned by phantomjs, or None if it timed out
    options = []
    if socks_proxy_port:
        options = ['--proxy-type=socks5', '--proxy=localhost:%s' % str(socks_proxy_port)]
    command = ['phantomjs'] + options + [script] + list(args)
    print '$ %s' % ' '.join(command)
    return timeout.run(subprocess.call, timelimit, command)
