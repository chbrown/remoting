# remoting

Some examples below.

## remoting.browser:

Call `your.js`, returning the phantomjs return code, with some arguments and the socksv5 proxy port that can be found at localhost:8070:

    phantomjs('your.js', ['-user=me', '-pass=that'], socks_proxy_port=8070, timelimit=60)

## remoting.curl:

Use pycurl, with socks! I don't think this works because pycurl is stupid.

    curl(url, socks_host=None, socks_port=None)

## remoting.socks:

Start an socks proxy through "gandalf", using localhost:7080 as the local proxy connection point.

    start_proxy('gandalf', 7080)

Run through a list of proxies and use the first one that works to make an outgoing proxy.
Each attempt to create a proxy times out after trying for 15 seconds.

    find_proxy(['gandalf', 'gollum'], 7080)

If no hosts in the list work, return None.

## remoting.ssh:

    # Use your local .ssh/id_rsa to login to `golem`, and add golem's host name to your known_hosts.
    add_host_key('golem')

## remoting.timeout:

Not really a remoting feature, but mostly useful because networking takes forever.

Run the function `def monkeywrenchit(a):` and raise `remoting.timeout.Expired` if it doesn't
return a value within 45 seconds. The `a` argument gets set to "the rusty knob".

    doit = wrap(monkeywrenchit, 45)
    doit('the rusty knob')

Do the same thing, but instead of raising an error, simply returning none when it times out, *if* it times out.
`monkeywrenchit` should not ever return `None` when it works, or else you can't know if it times out or not.

    run(monkeywrenchit, 45, 'the rusty knob')


