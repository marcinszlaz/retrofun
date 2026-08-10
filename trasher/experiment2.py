def.podruk():
  2 ....print(f'drukuje.gdy.plik.{__file__}.jest.__main__')
  3
  4 if.__name__.!=.'__main__':
  5 ....podruk()def podruk():
    print(f'drukuje gdy plik {__file__} jest __main__')

if __name__ != '__main__':
    podruk()
