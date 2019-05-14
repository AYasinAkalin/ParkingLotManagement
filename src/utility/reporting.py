# reporting.py
''' Contains simple functions to mainstream reporting.'''
import config as cfg


def report_at_once(message, status):
    if cfg.VERBOSE:
        if status == 'OK':
            print('{m:.<70}> \033[92m{s:<6}\033[00m'.format(
                                                        m=message, s=status))
        elif status == 'ERROR':
            print('{m:.<70}> \033[91m{s:<6}\033[00m'.format(
                                                        m=message, s=status))
        else:
            print('{m:.<70}> \033[93m{s:<6}\033[00m'.format(
                                                        m=message, s=status))


def report(func, message, *args, **kwargs):
    '''
    Prints event messages to terminal while a function executes.
    This function runs passed function, 'func'
        Pass parameters of 'func' to report() after 'message' argument.
        They will be picked automatically by *args and **kwargs
    '''
    error, err_msg = False, ''  # Set up some variables for error reporting

    # Start reporting before executing the function
    if cfg.VERBOSE:
        string = '{m:.<70}'.format(m=message)
        print(string, end='')

    # Run the Function
    try:
        status = func(*args, **kwargs)
        if not status:
            status = 'OK'
    except Exception as e:
        error = True
        err_msg = str(e)
        status = 'ERROR'

    # Finalize the report
    if cfg.VERBOSE:
        if status == 'OK':
            print('> \033[92m{s:<6}\033[00m'.format(s=status))
        elif status == 'ERROR':
            print('> \033[91m{s:<6}\033[00m'.format(s=status))
        else:
            print('> \033[93m{s:<6}\033[00m'.format(s=status))
    if error:
        print(err_msg)
