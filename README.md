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
