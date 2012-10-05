import signal

class Expired(Exception):
    pass

def wrap(func, timeout_seconds):
    def wrapper(*args):
        '''Basically how timeouts in Python work is:
        1. You use signal.signal to run a function after a certain amount of time.
           1a. That function will raise an exception.
        2. You run your target method, the `func` arg to this wrap() method.
           2a. Hope it runs quickly.
        3. As soon as func exits, tell `signal.signal` "just kidding, dont run that function after all"
        4. I.e. Cancel the scheduled signal from step 1, and put the old handler back in place.
        '''
        def new_alrm_handler(signum, frame):
            raise Expired()
        old_alrm_handler = signal.signal(signal.SIGALRM, new_alrm_handler)
        signal.alarm(timeout_seconds)
        try:
            result = func(*args)
        finally:
            signal.signal(signal.SIGALRM, old_alrm_handler)
        signal.alarm(0)
        return result
    return wrapper

def run(func, timeout_seconds, *args):
    # if your function always returns a value (never None),
    # you can just check for a None result and not worry about the try/except
    try:
        result = wrap(func, timeout_seconds)(*args)
    except Expired:
        result = None
    return result
