from subprocess import Popen, PIPE, call

from remoting import timeout, curl

def start_proxy(hostname, local_port):
    pkill_args = ['pkill', '-f', 'ssh -D %s' % local_port]
    pkill_returncode = call(pkill_args)
    if pkill_returncode == 0:
        print 'Existing ssh tunnel killed'
    else:
        print 'No ssh tunnel exists: %d' % pkill_returncode

    # start_proxy returns a process, or hangs trying to get one
    socks_args = ['ssh', '-D', str(local_port), hostname, '-N', '-v']
    print '$ %s' % ' '.join(socks_args)
    process = Popen(socks_args, stderr=PIPE)

    print 'Waiting for tunnel'
    tunnel_output = ''
    while True:
        tunnel_output += process.stderr.read(32)
        if 'Local forwarding listening on 127.0.0.1 port 5090' in tunnel_output:
            break

    print 'Tunnel established!'

    ip_response = curl.curl('http://ipv4.icanhazip.com', socks_port=local_port)
    print 'IP', ip_response.strip()

    return process

def find_proxy(hostname_iterator, local_port):
    for hostname in hostname_iterator:
        process = timeout.run(start_proxy, 15, hostname, local_port)
        if process == None:
            # it timed out...
            print 'Tunnel creation timed out after 15s.'
        else:
            return process

    print 'Could not find a valid hostname.'
    return None
