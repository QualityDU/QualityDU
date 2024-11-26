
# Instrukcja uruchamiania aplikacji Flask

## Krok 1: Tworzenie środowiska wirtualnego

1. **Stwórz środowisko wirtualne:**
   
   Przejdź do katalogu z projektem i utwórz środowisko wirtualne:
   ```bash
   python -m venv venv
   ```

2. **Aktywuj środowisko wirtualne:**

   - Na **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

   - Na **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```

## Krok 2: Instalacja wymaganych zależności

1. **Zainstaluj wymagane pakiety z pliku `requirements.txt`:**
   
   Zainstaluj wszystkie zależności:
   ```bash
   pip install -r requirements.txt
   ```
   
## Krok 3: Konfiguracja zmiennych środowiskowych

W katalogu głównym aplikacji utwórz plik .env i dodaj do niego następujące zmienne środowiskowe:

```
  FLASK_APP=app.py
  FLASK_ENV=development
  SECRET_KEY=supersecretkey
  DATABASE_URL=your_database_url
```

## Krok 4: Uruchamianie aplikacji Flask

1. **Uruchom aplikację Flask:**
   
   Aby uruchomić aplikację, użyj poniższego polecenia:
   ```bash
   flask run --debug
   ```
   lub
   ```bash
   python app.py
   ```
   Aplikacja powinna teraz działać lokalnie na domyślnym porcie (`http://127.0.0.1:5000/`).

## Krok 6: Migracje bazy danych

1. **Tworzenie migracji:**

   Aby utworzyć nowe migracje na podstawie zmian w modelach bazy danych, użyj poniższego polecenia:
   ```bash
   flask db migrate -m "Opis migracji"
   ```

2. **Wykonanie migracji:**

   Aby zastosować migracje do bazy danych, użyj:
   ```bash
   flask db upgrade
   ```
