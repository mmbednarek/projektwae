# Projekt na przedmiot Wstęp do algorytmów Ewolucyjnych

Funkcje implementujące algorytmy ewolucyjne znajdują się w module `evolution`.
Testy można uruchmomić przez polecenie `make`. 

```bash
make test
```

Należy pamiętać o właściwym ustawieniu zmiennej środowiskowej `PYTHONPATH`.
np. `PYTHONPATH=.. make test`. Przebieg iteracji będzie dostępny w katalogu logs w postaci plików csv.

Z plików csv można wygenerować wykresy przy użyciu polecenia.

```bash
make plots
```




## Windows
Do uruchomienia testów wymagane jest zainstalowanie Pythona 2 dostępnego na
stronie https://www.python.org/downloads/release/python-2718/

Do uruchomienia generacji wykresów wymagane jest zainstalowanie R dostępnego
na stronie https://cran.r-project.org/

Na systemach Windows do instalowania niezbędnych zależności oraz uruchamiania testów
można użyć plików .bat znajdujących się w podkatalogu /windows.
* **tests_dependencies.bat** - instaluje zależności niezbędne do uruchomienia testów
* **tests.bat** - uruchamia testy i generuje logi z nich w podkatalogu /logs, 
  wymaga wcześniejszego uruchomienia tests_dependencies.bat, jeśli jako argument zostanie podana liczba,
  stanie się ona ziarnem generatora liczb losowych
* **plots_dependencies.bat** - instaluje zależności niezbędne do uruchomienia generacji wykresów
* **tests.bat** - generuje wykresy w podkatalogu /plots na podstawie danych z podkatalogu /logs,
  wymaga wcześniejszego uruchomienia plots_dependencies.bat
* **benchmark_dependencies.bat** - instaluje zależności niezbędne do skorzystania z frameworku coco
  jako argument należy podać wynik kompilacji frameworku coco, plik .egg dostępny w katalogu
  %katalog_bazowy_coco%\build/\python\dist (patrz sekcja **Coco**), wymaga wcześniejszego uruchomienia
  tests_dependencies.bat
* **benchmark.bat** - uruchamia benchmark bbob z frameworku coco i wyniki zapisuje w katalogu exdata\benchmark-output,
  jako argument należy podać typ benchmarku (classic - standardowy algorytm różnicowy, dg - algorytm używający
  diversity guided), jeśli jako drugi argument zostanie podana liczba, stanie się ona ziarnem generatora liczb losowych
* **benchmark_analyze_dependencies.bat** - instaluje zależności niezbędne do analizy wyników wywołania benchmarka 
  coco. Wymaga pythona3
* **benchmark_analyze.bat** - analizuje wyniki wywołania benchmarka coco. Wymaga wcześniejszego uruchomienia 
  benchmark_analyze_dependencies.bat oraz pythona3. Wymaga także wywołania benchmark.bat dla obu metod
  i odpowiedniego nazwania katalogów z wynikami benchmarka. Wyniki zostaną zaprezentowane na ekranie po analize, a także będą
  dostępne w ppdata/index.html

## Coco
Wykonanie testów z użyciem frameworku coco wymaga jego pobrania i kompilacji.

Kod frameworku można pobrać poprzez sklonowanie jego repozytorium:
git clone https://github.com/numbbo/coco.git

Do kompilacji wymagane jest zainstalowanie pakietów pip:
```bash
python -m pip install numpy
python -m pip install scipy
```
Oraz w przypadku używania systemu windows Microsoft compiler package for Python 2.7 containing VC9
dostępnego na stronie https://web.archive.org/web/20190720195601/http://www.microsoft.com/en-us/download/confirmation.aspx?id=44266

Framework można następnie skompilować za pomocą polecenia
```bash
python do.py run-python
```
