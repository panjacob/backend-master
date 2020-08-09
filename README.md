Jak uruchomić:
Trzeba dodać 3 biblioteki - peewee, click i pytest

pip install -U peewee
pip install -U click
pip install -U pytest

Polecenia:
insert offline [nazwa_pliku] - dodawanie danych z pliku json (domyślnie nazwa_pliku = persons.json)
insert online [ile] - dodawanie danych z api (0 < ile < 5000)
remove-db [nazwa_pliku] - usunięcie pliku .db, domyślnie people.db
gender - wyświetlenie procenta mężczyzn i kobiet w bazie
average-age [płeć] (płeć = m,f,a)
most-common-cities [limit] - najpopularniejsze miasta, limit ile wyśiwetlić
most-common-passwords [limit] - najpopularniejsze hasła, limit ile wyśiwetlić
most-secure-passwords [limit] - najmocniejsze hasła, limit ile wyśiwetlić
born-between [YYYY-MM-DD] [YYYY-MM-DD] - użytkownicy urodzeni pomiędzy datami