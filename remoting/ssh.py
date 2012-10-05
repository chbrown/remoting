import subprocess

def add_host_key(hostname):
    returncode = subprocess.call(['ssh', '-o', 'StrictHostKeyChecking no', '-q', hostname, 'exit'])
    print 'ssh', hostname, returncode
