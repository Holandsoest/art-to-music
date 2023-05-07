"""Script that helps to interact with OS Sleep, Reboot & Shutdown functions"""

import os
import sys
import time
import psutil

def computer_sleep(seconds_until_sleep=5, verbose=1):
    """Function will put the computer in sleep mode.

    Implemented for OSX and LINUX and WINDOWS.

    Args:
        seconds_until_sleep: The number of seconds until the computer 
            goes to sleep.
        verbose: Verbosity mode, 0, 1. verbose=1 displays a countdown.

    """
    
    range_top = int(seconds_until_sleep * 10) - 1    
    spinner_1 = spinning_cursor()
    spinner_2 = spinning_cursor()
    
    if verbose:
        
        for _ in range(range_top, 0, -1):
            sys.stdout.write("\r" + spinner_1.__next__() + " Sleep in "+ \
                             str(1+(_//10))+ " seconds "+ spinner_2.__next__())
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")
            sys.stdout.flush()

        sys.stdout.write('\rGoodnight                                 ')
        time.sleep(1)
        sys.stdout.write('\r                                          ')

    else:
        time.sleep(seconds_until_sleep)

    if psutil.OSX:
        os.system("pmset sleepnow")
    else:
        if psutil.LINUX:
            os.system("systemctl suspend")
        else:
            if psutil.WINDOWS:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")   
            
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor
