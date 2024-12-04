# Skin Cancer Detection

## API-Dokumentation

Diese API ermöglicht es, Hautläsionen auf Hautkrebs zu analysieren und eine Klassifizierung als "benign" (gutartig) oder "malignant" (bösartig) basierend auf dem vortrainierten Modell VGG16, das für die Hautkrebs-Erkennung trainiert wurde, durchzuführen.

### Endpunkt: `/analyze-skin-lesion`

#### Beschreibung

Der Endpunkt akzeptiert ein Bild einer Hautläsion im POST-Format und gibt eine Vorhersage darüber, ob die Hautläsion gutartig oder bösartig ist. Zusätzlich wird das korrespondierende Konfidenzniveau des Modells zurückgegeben.

#### HTTP-Methode

- `POST`

#### Anfrageparameter

- **`skin-lesion-image`**: Ein Bild einer Hautläsion im JPEG- oder PNG-Format.

##### Beispielanfrage (lokal):

```bash
curl -X POST -F "skin-lesion-image=@/path/to/skin_lesion.jpg" http://localhost:5000/analyze-skin-lesion
```

#### Antwort

Die API gibt eine JSON-Antwort zurück, die die Vorhersage sowie das Konfidenzniveau enthält. Die Vorhersage kann entweder "benign" oder "malignant" sein, je nachdem, wie das Modell die Hautläsion klassifiziert. Der Konfidenzwert gibt die Sicherheit des Modells bei der Klassifizierung an.

**Wichtig**: Da das zugrundeliegende Modell eine binäre Klassifikation mit einer _sigmoid-Aktivierungsfunktion_ verwendet, ist der Konfidenzwert wie folgt zu interpretieren:

- Je näher der Konfidenzwert an 0 liegt, desto sicherer ist das Modell, dass die Hautläsion `benign` ist

- Je näher der Konfidenzwert an 1 liegt, desto sicherer ist das Modell, dass die Hautläsion `malignant` ist

##### Erfolgreiche Antwort:

```json
{
  "prediction": "benign",
  "confidence": 0.85
}
```

- **`prediction`**: Die Klassifizierung des Bildes ("benign" oder "malignant").
- **`confidence`**: Der Konfidenzwert (zwischen 0 und 1), der die Wahrscheinlichkeit angibt, mit der das Modell diese Klassifizierung vorgenommen hat. Ein höherer Wert bedeutet mehr Vertrauen in die Vorhersage.

##### Fehlerantwort:

Wenn das Bild nicht bereitgestellt wird oder ein Fehler auftritt:

```json
{
  "error": "Keine Hautläsion bereitgestellt."
}
```

#### Verzeichnisstruktur

- **`/temp`**: Ein temporäres Verzeichnis auf dem Server, in dem das hochgeladene Bild zwischengespeichert wird, um die Analyse durchzuführen. Dieses Verzeichnis wird nach der Analyse gelöscht.

#### Funktionsweise

1. **Datei hochladen**: Der Benutzer sendet das Bild der Hautläsion an den Endpunkt `/analyze-skin-lesion`.
2. **Zwischenspeicherung der Datei**: Das Bild wird vorübergehend auf dem Server im `/temp`-Verzeichnis gespeichert.
3. **Bildvorbereitung**:
   - Das Bild wird auf die benötigte Größe (224x224 Pixel) skaliert
   - Konvertierung in NumPy-Array der Form (height, width, channels) als geeignetes Format für das CNN
   - Das Array wird an Index 0 um eine zusätzliche Dimension `Batch-Dimension` erweitert
   - Normalisierung des Bildes durch Division eines jeden Pixels durch 255
4. **Vorhersage**: Das vortrainierte Modell VGG16, das für die Hautkrebs-Erkennung trainiert wurde, wird verwendet, um das Bild zu analysieren und eine Vorhersage zu treffen.
5. **Ergebnisse**: Die API gibt die Vorhersage ("benign" oder "malignant") und den Konfidenzwert zurück.
6. **Temporäres Verzeichnis entfernen**: Das temporäre Verzeichnis, das das Bild enthält, wird nach der Analyse gelöscht.

### Endpunkt: `/upload-skin-lesion`

#### Beschreibung

Der Endpunkt akzeptiert ein Bild einer Hautläsion im POST-Format, speichert es im Uploads-Verzeichnis unter der Benutzer-ID und speichert den Bildpfad in der Datenbank.

#### HTTP-Methode

- `POST`

#### Anfrageparameter

- **`skin-lesion-image`**: Ein Bild einer Hautläsion im JPEG- oder PNG-Format.

##### Beispielanfrage (lokal):

```bash
curl -X POST -F "skin-lesion-image=@/path/to/skin_lesion.jpg" http://localhost:5000/analyze-skin-lesion
```

#### Antwort

Die API gibt eine JSON-Antwort zurück, die den Erfolg des Uploads bestätigt.

##### Erfolgreiche Antwort:

```json
{
  "message": "Das Bild wurde erfolgreich gespeichert.",
  "confidence": 0.85
}
```

- **`message`**: Eine Bestätigung, dass das Bild erfolgreich gespeichert wurde.

##### Fehlerantwort:

Wenn das Bild nicht bereitgestellt wird oder ein Fehler auftritt:

```json
{
  "error": "Keine Hautläsion bereitgestellt."
}
```

#### Verzeichnisstruktur

- **`/uploads/<user_id>/`**: Ein Verzeichnis auf dem Server, in dem das hochgeladene Bild unter dem Benutzerverzeichnis gespeichert wird. **`<user_id>`** ist ein Platzhalter für die ID des Benutzers, der das Bild hochgeladen hat.

#### Funktionsweise

1. **Datei hochladen**: Der Benutzer sendet das Bild der Hautläsion an den Endpunkt `/upload-skin-lesion`.
2. **Überprüfung der Datei**: Die Anfrage wird dahingehend überprüft, ob ein Bild bereitgestellt wurde.
3. **Erstellung des Upload-Verzeichnisses**: Ein Verzeichnispfad wird basierend auf der Benutzer-ID erstellt (z.B.: \*\*`/uploads/1/` für den Benutzer mit der ID 1).
4. **Speichern der Datei**: Das Bild wird sicher im entsprechenden Benutzerverzeichnis gespeichert.
5. **Speichern des Pfads in der Datenbank**: Der Pfad des gespeicherten Bilds wird in der Datenbank mit der Benutzer-ID verknüpft.
6. **Ergebnisse**: Die API gibt eine JSON-Antwort zurück, die den Erfolg des Uploads bestätigt.

### Endpunkt: `/get-all-analyses`

#### Beschreibung

Der Endpunkt gibt alle Analysen zu einer Benutzer-ID zurück.

#### HTTP-Methode

- `GET`

#### Anfrageparameter

- **`user_id`**: Die ID des Benutzers, für den die Analysen abgerufen werden sollen.

##### Beispielanfrage (lokal):

```bash
curl -X GET "http://localhost:5000/get-all-analyses?user_id=1"
```

#### Antwort

Die API gibt eine JSON-Antwort zurück, die eine Liste von Analysen enthält, die für den angegebenen Benutzer durchgeführt wurden. Jede Analyse enthält die Analyse-ID, das Ergebnis, den Konfidenzwert, die Benutzer-ID und die Bild-ID.

##### Erfolgreiche Antwort:

```json
[
  {
    "analysis_id": 1,
    "result": "benign",
    "confidence_score": 0.85,
    "user_id": 1,
    "image_id": 10
  },
  {
    "analysis_id": 2,
    "result": "malignant",
    "confidence_score": 0.91,
    "user_id": 1,
    "image_id": 11
  }
]
```

- **`analysis_id`**: Die eindeutige ID der Analyse.
- **`result`**: Das Ergebnis der Analyse ("benign" oder "malignant").
- **`confidence_score`**: Der Konfidenzwert (zwischen 0 und 1), der die Sicherheit des Modells bei der Klassifizierung angibt.
- **`user_id`**: Die ID des Benutzers, der die Analyse angefordert hat.
- **`image_id`**: Die ID des analyisierten Bilds.

##### Fehlerantwort:

Wenn die Benutzer-ID nicht bereitgestellt wird:

```json
{
  "error": "Keine Benutzer-ID bereitgestellt."
}
```

Wenn keine Analysen für die angegebene Benutzer-ID gefunden werden:

```json
{
  "error": "Es wurden keine Analysen für diesen Benutzer gefunden."
}
```

#### Funktionsweise

1. **Anfrage mit Benutzer-ID**: Der Benutzer sendet eine GET-Anfrage an den Endpunkt `/get-all-analyses` mit der Benutzer ID als Parameter.
2. **Überprüfung des Parameters**: Die Anfrage wird dahingehend überprüft, ob eine Benutzer-ID bereitgestellt wurde.
3. **Abruf der Analysen**: Es wird in der Datenbanktabelle `analyses` nach allen Analysen gesucht, die mit der angegebenen Benutzer-ID verknüpft sind.
4. **Ergebnisse**: Die API gibt eine JSON-Antwort zurück, die eine Liste von allen Analysen gefundenen Analysen enthält. Wenn keine Analysen gefunden werden, wird eine Fehlermeldung zurückgegeben.

### Endpunkt: `/register`

#### Beschreibung

Der Endpunkt ermöglicht die Registrierung eines neuen Benutzers. Dieser muss ein Formular mit den erforderlichen Informationen ausfüllen und die API überprüft, ob der Benutzername und die E-Mail-Adresse verfügbar sind. Falls diese bereits existieren, wird eine Fehlermeldung zurückgegeben. Bei erfolgreicher Registrierung wird der Benutzer in der Datenbank gespeichert und eine Bestätigung wird zurückgegeben.

#### HTTP-Methode

- `POST`

#### Anfrageparameter

- **`username`** (Pflichtfeld): Der Benutzername des neuen Benutzers.
- **`email`** (Pflichtfeld): Die E-Mail-Adresse des neuen Benutzers.
- **`password`** (Pflichtfeld): Das Passwort des neuen Benutzers.
- **`first_name`** (Pflichtfeld): Der Vorname des neuen Benutzers.
- **`last_name`** (Pflichtfeld): Der Nachname des neuen Benutzers.

##### Beispielanfrage (lokal):

```bash
curl -X POST -F "username=maxmustermann" -F "email=max.mustermann@mail.de" -F "password=sicheresPasswort" -F "first_name=Max" -F "last_name=Mustermann" http://localhost:5000/register
```

#### Antwort

Die API gibt eine JSON-Antwort zurück, die eine Bestätigung der erfolgreichen Registrierung und die Details des neuen Benutzers enthält.

##### Erfolgreiche Antwort:

```json
{
  "message": "Benutzer wurde erfolgreich registriert.",
  "user_id": 1,
  "username": "maxmustermann",
  "email": "max.mustermann@mail.de",
  "first_name": "Max",
  "last_name": "Mustermann"
}
```

- **`message`**: Eine Bestätigung, dass der Benutzer erfolgreich registriert wurde.
- **`user_id`**: Die ID des neu erstellten Benutzers.
- **`username`**: Der Benutzername des registrierten Benutzers.
- **`email`**: Die E-Mail-Adresse des registrierten Benutzers.
- **`first_name`**: Der Vorname des registrierten Benutzers.
- **`last_name`**: Der Nachname des registrierten Benutzers.

##### Fehlerantwort:

Falls eine erforderliche Benutzereingabe fehlt:

```json
{
  "error": "Bitte alle erforderlichen Felder ausfüllen."
}
```

Falls bereits ein Benutzer mit dem angegebenen Benutzernamen existiert:

```json
{
  "error": "Benutzername bereits vergeben."
}
```

Falls bereits ein Benutzer mit der angegebenen E-Mail-Adresse existiert:

```json
{
  "error": "E-Mail-Adresse bereits vergeben."
}
```

#### Funktionsweise

1. **Anfrage mit Benutzer-ID**: Der Benutzer sendet eine POST-Anfrage an den Endpunkt `/register` mit den Parametern `username`, `email`, `password`, `first_name` und `last_name`.
2. **Überprüfung der Parameter**: Die Anfrage wird dahingehend überprüft, ob alle erforderlichen Benutzereingaben vorhanden sind.
3. **Existenzprüfung des Benutzernamens und der E-Mail-Adresse**: Es wird überprüft, ob bereits ein Benutzer mit dem angegebenen Benutzernamen oder der E-Mail-Adresse existiert.
4. **Passwort-Hashing**: Das Passwort wird sicher mit dem pbkdf2:sha256-Hashing-Verfahren gehasht, bevor es in der Datenbank gespeichert wird.
5. **Benutzererstellung**: Ein neuer Benutzer wird in der Datenbanktabelle `users` angelegt.
6. **Ergebnisse**: Die API gibt eine JSON-Antwort zurück, die bei einer erfolgreichen Registrierung eine Bestätigung und die Benutzerdaten enthält.

### Endpunkt: `/login`

#### Beschreibung

Der Endpunkt ermöglicht es einem registrierten Benutzer, sich in der Anwendung anzumelden. Der Benutzer muss seinen Benutzernamen oder seine E-Mail-Adresse und sein Passwort eingeben. Die API überprüft die Anmeldedaten und erstellt bei erfolgreicher Authentifizierung ein JWT (JSON Web Token), das zur Autorisierung zukünftiger Anfragen verwendet wird.

#### HTTP-Methode

- `POST`

#### Anfrageparameter

- **`username_or_email`** (Pflichtfeld): Der Benutzername oder die E-Mail-Adresse des Benutzers.
- **`password`** (Pflichtfeld): Das Passwort des Benutzers.

##### Beispielanfrage (lokal):

```bash
curl -X POST -F "username_or_email=maxmustermann" -F "password=sicheresPasswort" http://localhost:5000/login
```

#### Antwort

Die API gibt eine JSON-Antwort zurück, die eine Bestätigung der erfolgreichen Anmeldung sowie das JWT-Token und die Benutzerdaten enthält. Das JWT wird zusätzlich als HttpOnly-Cookie gesetzt.

##### Erfolgreiche Antwort:

```json
{
  "message": "Erfolgreich angemeldet.",
  "jwt_access_token": "JWT_ACCESS_TOKEN",
  "user_id": 1,
  "username": "maxmustermann",
  "email": "max.mustermann@mail.de",
  "first_name": "Max",
  "last_name": "Mustermann"
}
```

- **`message`**: Eine Bestätigung, dass der Benutzer erfolgreich angemeldet wurde.
- **`jwt_access_token`**: Das JWT-Token, das zur Autorisierung zukünftiger Anfragen verwendet wird.
- **`user_id`**: Die ID des angemeldeten Benutzers.
- **`username`**: Der Benutzername des angemeldeten Benutzers.
- **`email`**: Die E-Mail-Adresse des angemeldeten Benutzers.
- **`first_name`**: Der Vorname des angemeldeten Benutzers.
- **`last_name`**: Der Nachname des angemeldeten Benutzers.

##### Fehlerantwort:

Falls eine erforderliche Benutzereingabe fehlt:

```json
{
  "error": "Bitte alle erforderlichen Felder ausfüllen."
}
```

Falls der Benutzername oder die E-Mail-Adresse ungültig ist:

```json
{
  "error": "Benutzername oder E-Mail-Adresse ist ungültig."
}
```

Falls das Passwort falsch ist:

```json
{
  "error": "Falsches Passwort."
}
```

#### Funktionsweise

1. **Anfrage mit Benutzer-ID**: Der Benutzer sendet eine POST-Anfrage an den Endpunkt `/login` mit den Parametern `username_or_email` und `password`.
2. **Überprüfung der Parameter**: Die Anfrage wird dahingehend überprüft, ob alle erforderlichen Benutzereingaben vorhanden sind.
3. **Benutzersuche**: Es wird in der Datenbanktabelle `users` nach einem Benutzer mit dem angegebenen Benutzernamen oder E-Mail-Adresse gesucht.
4. **Passwortüberprüfung**: Wenn ein Benutzer gefunden wurde, wird geprüft ob das angegebene Passwort mit dem gespeichterten Passwort übereinstimmt.
5. **JWT-Erstellung**: Bei erfolgreicher Authentifizierung wird ein JWT-Token erstellt, das die Benutzer-ID als Identität enthält.
6. **Setzen des HttpOnly-Cookies**: Das JWT-Token wird als HttpOnly-Cookie gesetzt, um die Sicherheit zu erhöhen.
7. **Ergebnisse**: Die API gibt eine JSON-Antwort zurück, die bei einer erfolgreichen Anmeldung eine Bestätigung, das JWT-Token und die Benutzerdaten enthält.

### Endpunkt: `/delete-account`

#### Beschreibung

Der Endpunkt ermöglicht es einem authentifizierten Benuztzer seinen Account zu löschen. Es werden alle seine Benutzerdaten aus der Datenbank entfernt und das zugehörige JWT-Access-Token gelöscht.

#### HTTP-Methode

- `DELETE`

#### Anfrageparameter

Keine

##### Beispielanfrage (lokal):

```bash
curl -X DELETE http://localhost:5000/delete-account -H "Authorization: Bearer <jwt_access_token>"
```

#### Antwort

Die API gibt eine JSON-Antwort zurück, die eine Bestätigung enthält, wenn der Benutzer erfolgreich aus der Datenbank entfernt wurde.

##### Erfolgreiche Antwort

```json
{
  "message": "Account erfolgreich gelöscht."
}
```

- **`message`**: Eine Bestätigung, dass der Benutzer erfolgreich gelöscht wurde.

##### Fehlerantwort

Wenn der Benutzer nicht gefunden wird:

```json
{
  "error": "Es konnte kein Benutzer gefunden werden."
}
```

- **`message`**: Eine Bestätigung, dass der Benutzer erfolgreich gelöscht wurde.

#### Funktionsweise

1. **Benutzeridentifikation**: Der Benutzer sendet eine DELETE-Anfrage an den Endpunkt `/delete-account` ohne Parameter. Die Anfrage muss aber ein gültigen JWT mitsenden.
2. **Überprüfung des JWT**: Die Anfrage wird dahingehend überprüft, ob der Benutzer authentifiziert ist.
3. **Benutzersuche**: Es wird in der Datenbanktabelle `users` nach einem Benutzer mit der `user_id`, die im JWT enthalten ist, gesucht.
4. **Benutzer löschen**: Wenn ein Benutzer gefunden wurde, werden seine Daten aus der Datenbak entfernt.
5. **JWT löschen**: Das zugehörige JWT-Token wird aus den Cookies entfernt.
6. **Ergebnisse**: Die API gibt eine JSON-Antwort zurück, die bei erfolgreicher Entfernung des Benutzers eine Bestätigungsmeldung enthält.
