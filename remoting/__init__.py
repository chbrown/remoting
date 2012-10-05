import sys
import subprocess

def stderr(s):
    sys.stderr.write(s)
    sys.stderr.write('\n')
    sys.stderr.flush()

def add_host_key(hostname):
    returncode = subprocess.call(['ssh', '-o', 'StrictHostKeyChecking no', '-q', hostname, 'exit'])
    print 'ssh', hostname, returncode
