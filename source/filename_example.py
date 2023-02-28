def bake_eggs_and_spam(name_of_the_cook):
    print (name_of_the_cook + ' is baking eggs and spam.')


# try running `python.exe .\source\filename_example.py` in stead of ``
if __name__ == "__main__":
    print('This only runs if this example is run as the "__main__"')
    print('This runs if we press play on this file, otherwise it does not.')
    print('Place your demo here.')

    bake_eggs_and_spam(name_of_the_cook = 'Koen')
    # NOTE: Adding the variable with an equals helps to make the code more clear in this case



