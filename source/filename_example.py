def bake_eggs_and_spam(name_of_the_cook):
    print (name_of_the_cook + ' is baking eggs and spam.')

# try running `python.exe .\source\filename_example.py`
if __name__ == "__main__":
    print('This only runs if this example is run as the "__main__"')
    print('Normaly it is not as this is not actualy our main.py,\nbut it is a good place to place a little demo.')
    print('\nIn other words. This runs if we press play on this file, otherwise it does not.')

    bake_eggs_and_spam('Koen')
