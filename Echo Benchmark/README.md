# Echo Benchmark

System do pomiaru wydajności i porównania czasu egzekucji operacji w środowiskach Python oraz C++. Projekt:
1. Automatycznie uruchamia wszystkie wymagane skrypty.
2. Tworzy w sposób deterministyczny wartości losowe:
   1. Losuje według *random.seed(42)*.
   2. Zapisuje je do plików .csv o różnych wielkościach w `/data`.
3. Zbiera dostępne informację o maszynie użytkownika i wersjach oprogramowania.
4. Kompiluje program **c++** samodzielnie znajdując wymagane elementy.
5. Uruchamia obie programy testowe **c++** i **python** które:
    1. Wczytują te same wartości z plików `.csv`.
    2. Wykonują sortowanie bąbelkowe i sortowanie z domyślnej funkcji sortowania.
    3. Mierzą czas wykonania.
    4. Wykonują test funkcjonalny, weryfikują poprawność sortowania.
    5. Zapisują wynik.
    6. Wszystkie pomiary są powtarzane 5 razy dla dodatkowych danych.
6. Zbiera wyniki i tworzy raport dostępny w `/reports`.

## Wyniki i raporty

Po zakończeniu działania skryptu `run_benchmark.py`, wszystkie wyniki zostaną przetworzone i zapisane w katalogu `/reports`.

W katalogu znajdują się 2 raporty uruchomione na różnych maszynach wraz z wyciągniętymi wnioskami.

## Instrukcja uruchomienia

Aby uruchomić pełny system, wykonaj poniższe kroki w terminalu (zakładając system Windows):

1. **Rozpakuj archiwum ZIP** do wybranego folderu.
2. **Otwórz terminal** (np. PowerShell lub CMD) w folderze głównym projektu.
3. **Aktywuj środowisko wirtualne i uruchom skrypt:**

```bash
# Aktywacja środowiska wirtualnego
.\.venv\Scripts\activate

# Uruchomienie głównego skryptu benchmarku
python run_benchmark.py
```

---

## Struktura projektu

| Katalog / Plik     | Opis zawartości                                                              |
|--------------------|------------------------------------------------------------------------------|
| `/.venv`           | Środowisko wirtualne Pythona z zainstalowanymi bibliotekami.                 |
| `/data`            | Przechowuje pliki `.csv` z wygenerowanymi losowo zestawami liczb.            |
| `/logs`            | Dzienniki zdarzeń (logi) służące do debugowania i śledzenia pracy systemu.   |
| `/reports`         | **Miejsce docelowe raportów końcowych wraz z wyciągniętymi wnioskami.**      |
| `/results`         | Surowe dane z pomiarów oraz informacje o specyfikacji środowiska testowego.  |
| `/runners`         | Zbiór 6 skryptów sterujących poszczególnymi etapami działania systemu.       |
| `/src_cpp`         | Kod źródłowy projektu Visual Studio (implementacja modułu mierzącego w C++). |
| `/src_python`      | Kod źródłowy modułu mierzącego zaimplementowanego w języku Python.           |
| `run_benchmark.py` | Skrypt uruchomieniowy                                                        |

---

## Podział zadań w zespole

Pluton Echo funkcjonował według poniższego podziału zadań:

| Tytus Barański                                               | Gabriel Lisiecki                                              |
|--------------------------------------------------------------|---------------------------------------------------------------|
| Utworzenie skryptu uruchomieniowego                          | Utworzenie skryptu tworzącego raporty                         |
| Podstawowa wersja kompilacji c++                             | Dodanie flag kompilacji i ustawienie zmiennych środowiskowych |
| Programy testowe wraz z pomiarem czasu i weryfikacją wyników | Zebranie danych środowiskowych                                |
| Implementacja sortowania bąbelkowego                         | Implementacja Sortowania bibliotekowego                       |
| System logowania                                             | Zebranie rezultatów pomiarów, wygenerowanie wykresów          |