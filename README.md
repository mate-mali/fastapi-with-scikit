**I - Krótki opis systemu/usługi (jaki problem rozwiązuje):** Jest to system oparty na datasecie iris, dostepnym w pakiecie sklearn - model przewiduje typ kwiatu poprzez anlize czterech wynierow tych kwiatow, dokonujac klasycikacji do jesnej z trzech kategorii 

**II - Instrukcję instalacji i uruchomienia:** 

1. stworzenie srodowiska wirtualnego .venv - "uv venv .venv"

2. uruchomic "uv pip install -r requirements.txt" 
3. po instalacji aktywowac venv poprzez uruchomienie komendy w terminalu (cmd) ".venv\Scripts\activate"
4. uruchomic server fatapi, mozna to zrobic wykonujac z poziomu folderu projektu "uvicorn main:app"
5. uruchomienie strony pod adresem przypisanym do servera uvicorn, domyslnei bedzie to albo localhost:8000 albo 127.0.0.1:8000

**II - wymagania sposób przygotowania środowiska (`uv`)** 

1. "uv venv .venv" - zainicjowanie wirtualnego srodowiska 
2. "uv pip install -r requirements.txt"

3. jesli z jakiegos powodu reqirements.txt nie istnieje, mozna go wygenerowac komenda "uv export --no-hashes > requirements.txt"

III - sposób uruchomienia serwera FastAPI 
uvicorn main:app

**III - Instrukcję użycia:** glownym endpointem apliakcji jest "/input/predict_dict" ktory akceptuje requesty typu POST ktore jako payload przyjmuja slownik z czterema elementami w nastepujacym formacie:
{
  "sepal_length_cm": 5.1,
  "sepal_width_cm": 3.5,
  "petal_length_cm": 1.4,
  "petal_width_cm": 0.2
}

*przykladowy request ma postac podobna do tego:*
curl -X 'POST' \
  'http://localhost:8000/input/predict_dict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sepal_length_cm": 5.1,
  "sepal_width_cm": 3.5,
  "petal_length_cm": 1.4,
  "petal_width_cm": 0.2
}'

*zwracany jest dict ktory zawiera dwie wartosci:* 
- sklasyfikowany numer przypisany do kategorii kwiatu 0-2 (trzy mozliwe kategorie)
- oparta na sklowniku wartosci doceloweych nazwa kwiatu
przykladowy response:
{
  "message": {
    "prediction_class": 0,
    "prediction_name": "setosa"
  }
}

**IV - opis endpointów:**
 - /docs (GET)- Json Swagger dokumentujacy endpointy i pozwalajacy na podglad i wykonywanie komend get i post (w tym przypadku)
 - /retrain (GET)- enpoint ktory uruchamia funkcje retrainmodel - ona uruchamia sklearn ktory wykonuje model.fit() dla modelu SVC uzytego w tym projekcie i eksportuje wytrenowany model do modelx.joblib oraz ekportuje target_names.joblib, ktorego uzywamy d przetlumaczenia wyniku predykcji na koncowa nazwe kwiatu
 - /input/raw (GET)- enpoint ktory zwraca dataset uzyty do trenowania w jego oryginalnej psotaci - jest to funkcjonalnosc kotra sie przydaje w celu pobierania danych lub ich podgladu 
 - /input/predict_dict (POST) - enpoint akceptuje slownik z czterema kluczami/json z czterema kluczami - ktore nastepnei są podawane do wbudowanej funkcji modelx.predict() - winikowa pomyslnego POST-a jest zwracany jest json ktory zawiera wewnatrz dwa klucze: prediction_class - ktory jest numerem sklasyfikowanego kwiatu, i prediction_name, ktory jest wynikie mzestawienia prediction_class z lista trzyelementowa target_names

**V - Iprzykład zapytania i odpowiedzi (np. JSON):**
*Zapytanie:*
curl -X 'POST' \
  'http://localhost:8000/input/predict_dict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sepal_length_cm": 5.1,
  "sepal_width_cm": 3.5,
  "petal_length_cm": 1.4,
  "petal_width_cm": 0.2
}'
*Odpowiedz:*
{
  "message": {
    "prediction_class": 0,
    "prediction_name": "setosa"
  }
}

**VI - Informację o:**     
*użytym modelu:* model to sklearn.svm.svc - czyli support vector classifier, bedacy czescia komponentu support vector machine - jest to klasyfikator wspomagajacy klasyfikacjie wieloklasowa - takiej tu porzebowalismy poniewaz nie mamy doczynienia z wartoscia binarna ale z taka ktora moze nalezec do jednaj z trzech kategorii - model zwraca ta klase ktorej porawdopodobienstwo jest najwieksze
Model jest przetrenowany na danych ktore mozna przejrzec i wyeksportowac poprzez endpoint /input/raw 

*danych wejściowych i wyjściowych:*
wejsciowe: cztery rozmiary kwiatow podane w postaci slownika z tymi kluczami:
{
  "sepal_length_cm": 5.1, *//dlugosc wiekszych dolnych platkow w cm, float albo double*
  "sepal_width_cm": 3.5,  *//szerokosc dolnych wiekszych platkow w cm, float albo double*
  "petal_length_cm": 1.4, *//dlugosc mniejszych gornych platkow w cm, float albo double*
  "petal_width_cm": 0.2   *//szerokosc mniejszych gornych platkow w cm, float albo double*
}

wyjsciowe: numer kategorii kwiatu sklasyfikowany na podstawie czterech podanych wymiarow - moze on miec wartosc od 0-2
"target_names": [
    "setosa",
    "versicolor",
    "virginica"
  ]

*0 to setosa*
*1 to versicolor*
*2 to virginica*
