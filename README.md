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

- `user_id`: Die ID des Benutzers, für den die Analysen abgerufen werden sollen.

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
