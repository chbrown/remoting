import subprocess

from remoting import stderr, timeout, curl

def pkill(proc_name):
    try:
        pkill_args = ['pkill', '-f', proc_name]
        return_code = subprocess.call(pkill_args)
    except:
        return_code = 10
    return return_code

def start_proxy(hostname, local_port):
    '''
    `start_proxy` returns a process, or hangs trying to get one.
    You should always wrap this with a timeout, because it'll infinitely loop otherwise.

    '''

    if pkill('ssh -D %s' % local_port) == 0:
        stderr('Existing ssh tunnel killed')

    socks_args = ['ssh', '-D', str(local_port), hostname, '-N', '-v']
    stderr('$ %s' % ' '.join(socks_args))
    process = subprocess.Popen(socks_args, stderr=subprocess.PIPE)

    stderr('Waiting for tunnel')
    tunnel_output = ''
    while True:
        tunnel_output += process.stderr.read(32)
        if 'Local forwarding listening on 127.0.0.1' in tunnel_output:
            break

    stderr('Tunnel established!')

    try:
        ip_response = curl.curl('http://ipv4.icanhazip.com', socks_port=local_port)
        stderr('IP: %s' % ip_response.strip())
    except:
        stderr('Failed to get IP',)

    return process

def find_proxy(hostname_iterator, local_port):
    for hostname in hostname_iterator:
        process = timeout.run(start_proxy, 15, hostname, local_port)
        if process == None:
            # it must have timed out, other process would be a Popen process
            stderr('Tunnel creation timed out after 15s.')
        else:
            return process

    stderr('Could not find a valid hostname.')
    return None
