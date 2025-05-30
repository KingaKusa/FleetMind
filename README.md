**FleetMind**
FleetMind to zaawansowana aplikacja webowa stworzona w Pythonie przy użyciu frameworka Django. Jej głównym celem jest zarządzanie zadaniami i użytkownikami w sposób skalowalny i wydajny. Aplikacja jest hostowana w chmurze AWS, co zapewnia wysoką niezawodność i elastyczność.

**Live demo**
FleetMind jest dostępne na AWS: [FleetMind na AWS](http://fleetmind-env.eba-bxnzixvu.eu-central-1.elasticbeanstalk.com/)

**Technologie użyte w projekcie:**
Python – główny język backendu, obsługujący logikę aplikacji.

Django – framework zapewniający zarządzanie użytkownikami, bazą danych i API.

HTML, CSS, JavaScript – frontendowa warstwa aplikacji, odpowiedzialna za wizualizację interfejsu użytkownika.

Shell, Nushell, PowerShell, Batchfile – skrypty automatyzujące instalację, wdrożenia i integrację z systemem operacyjnym.

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

**Zabezpieczenia:**
FleetMind zapewnia Multi-Factor Authentication (MFA) w postaci aplikacji uwierzytelniającej, co dodaje dodatkową warstwę ochrony danych użytkownika.

**Baza danych:**
Aplikacja wykorzystuje PostgreSQL – zaawansowany system zarządzania bazami danych (DBMS), który zapewnia większą elastyczność i funkcjonalność niż MySQL.

W środowisku developerskim używam Dockera, co umożliwia testowanie migracji lokalnie przed wdrożeniem na AWS.

Migracje bazy na AWS przeprowadzam dopiero po pomyślnych testach lokalnych, co zapewnia spójność danych i stabilność aplikacji.







