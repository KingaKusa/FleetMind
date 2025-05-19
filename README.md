Mój projekt FleetMind składa się głównie z Pythona, co oznacza, że rdzeń aplikacji jest oparty na tym języku (w ramach frameworka Django).
Jest w nim część frontendowa napisana w HTML- są to widoki dla użytkownika.
Pozostałe języki takie jak Shell, Nushell, PowerShell i Batchfile - służą do realizacji skryptów automatyzujących, instalacyjnych i integrujących aplikację z systemem operacyjnym.
Całość tworzy złożoną aplikację webową wykorzystującą AWS do hostingu i zarządzania.




**FleetMind**
FleetMind to zaawansowana aplikacja webowa, zaprojektowana w Pythonie przy użyciu frameworka Django. Jest hostowana w chmurze AWS, co zapewnia skalowalność i niezawodność.

Live demo: [FleetMind na AWS](https://fleetmind-env.eba-bxnzixvu.eu-central-1.elasticbeanstalk.com/)

**Technologie użyte w projekcie:**
Python – główny język backendu, obsługujący logikę aplikacji.

Django – framework zapewniający zarządzanie użytkownikami, bazą danych i API.

HTML – frontendowa warstwa aplikacji, odpowiedzialna za wizualizację interfejsu użytkownika.

Shell, Nushell, PowerShell, Batchfile – skrypty automatyzujące instalację, wdrożenia i integrację z systemem.

**Kluczowe funkcjonalności:**
System użytkowników – rejestracja, logowanie, autoryzacja i zarządzanie sesjami.

Obsługa zadań – funkcjonalność CRUD (Create, Read, Update, Delete) dla zarządzania zadaniami.

Dynamiczne widoki – szablony Django generujące responsywne strony internetowe.

Automatyczne wdrożenia – integracja z AWS Elastic Beanstalk umożliwiająca łatwe skalowanie aplikacji.

**Wykorzystanie AWS:**
FleetMind korzysta z usług AWS do hostingu i zarządzania aplikacją, w tym:

Elastic Beanstalk – automatyczne skalowanie i wdrażanie aplikacji.

S3 – przechowywanie plików użytkownika i zasobów aplikacji.

RDS (PostgreSQL) – zarządzana baza danych przechowująca informacje o zadaniach i użytkownikach.

IAM – kontrola dostępu i zarządzanie politykami bezpieczeństwa.

**Instrukcja instalacji:**

***Sklonuj repozytorium:***

git clone https://github.com/KingaKusa/FleetMind.git

***Utwórz i aktywuj wirtualne środowisko:***


python -m venv .venv

.venv\Scripts\activate


***Zainstaluj zależności:***

pip install -r requirements.txt


***Wykonaj migracje bazy danych:***

python manage.py makemigrations

python manage.py migrate


***Uruchom aplikację:***

python manage.py runserver

-----
Zabezpieczenia:
Zastosowałam Multi-Factor authentication (MFA) - w postaci aplikacji uwierzytelniającej. Dzięki temu dane zawarte w aplikacji mają dodatkową warstwę zabezpieczeń.

Baza danych:
Korzystam z PostgreSQL - to zaawansowany, otwarty system zarządzania bazami danych (DBMS). Jest to obiektowo-relacyjna baza danych, którą wybrałam ze względu na możliwość większej elastyczności i zaawansowania funkcji w stosunku do MySQL.
Do pracy w środowisku developerskim korzystam z Dockera, by testować lokalnie migracje i upewnić się, że modele pasują do rzeczywistej struktury DB na AWS. Przenoszenie (migracje na zdalnej bazie na AWS) wykonuję po pomyślnym wyniku testów lokalnych.





