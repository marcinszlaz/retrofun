import experyment2

def wydruk():
    print(f'drukuje tylko gdy plik {__file__} jest __main__')

experyment2.podruk()

if __name__ == '__main__':
    wydruk()
