# Remoting

Some examples regarding using this package are below.

## remoting:

    # Use your local .ssh/id_rsa to login to `golem`, and add golem's host name to your known_hosts.
    from remoting import add_host_key
    add_host_key('golem')

## remoting.browser:

Call `your.js`, returning the phantomjs return code, with some arguments and the socksv5 proxy port that can be found at localhost:8070:

    from remoting import browser
    browser.phantomjs('your.js', ['-user=me', '-pass=that'], socks_proxy_port=8070, timelimit=60)

## remoting.curl:

Use pycurl, with socks! This sort of works, but you're probably better off with subprocess.

    from remoting import curl
    curl.curl(url, socks_host=None, socks_port=None)

## remoting.socks:

Start an socks proxy through "gandalf", using localhost:7080 as the local proxy connection point.

    from remoting import socks
    sock_proc = socks.start_proxy('gandalf', 7080)
    # use it:
    html = subprocess.check_output(['curl', 'http://henrian.com', '-s',
      '--socks5', 'localhost:%s' % proxy_port])
    # done, so kill it:
    sock_proc.kill()

Run through a list of proxies and use the first one that works to make an outgoing proxy.
Each attempt to create a proxy times out after trying for 15 seconds.

    # ...
    sock_proc = socks.find_proxy(['gandalf', 'gollum', 'gillian'], 7080)

If no hosts in the list work, return None.

## remoting.timeout:

Not really a remoting feature, but mostly useful because networking takes forever.

Run the function `def monkeywrenchit(target, intensity):` and raise `remoting.timeout.Expired` if it doesn't
return a value within 45 seconds. The `a` argument gets set to "the rusty knob".

    from remoting import timeout
    doit = timeout.wrap(monkeywrenchit, 45)
    doit('the rusty knob', 98)

Do the same thing, but instead of raising an error, simply returning none when it times out, *if* it times out.
`monkeywrenchit` should not ever return `None` when it works, or else you can't know if it times out or not.

    # ...
    timeout.run(monkeywrenchit, 45, 'the rusty knob', 98)
