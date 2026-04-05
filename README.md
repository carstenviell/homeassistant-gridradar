# Gridradar Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Zeigt Echtzeit-Netzdaten von [gridradar.net](https://service.gridradar.net) in Home Assistant an.

## Verfügbare Sensoren

| Sensor | Einheit | Tarif |
|--------|---------|-------|
| Netzfrequenz UCTE (Median, 1s) | Hz | Free |
| Netzzeit-Abweichung | s | Free |
| Netzfrequenz UCTE (Median, 100ms) | Hz | Individual |
| Netzfrequenz UCTE (Min, 1s) | Hz | Individual |
| Netzfrequenz UCTE (Max, 1s) | Hz | Individual |
| aFRR aktiviert (15 Min) | MW | Individual |

## Installation

### Via HACS (empfohlen)

1. HACS öffnen → **Integrationen** → Drei-Punkte-Menü → **Benutzerdefinierte Repositories**
2. URL dieses Repositories eintragen, Kategorie: **Integration**
3. Integration suchen und installieren
4. Home Assistant neu starten

### Manuell

1. Den Ordner `custom_components/gridradar` in dein Home Assistant `custom_components`-Verzeichnis kopieren
2. Home Assistant neu starten

## Einrichtung

1. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
2. Nach „Gridradar" suchen
3. API-Token eingeben (kostenlos registrieren unter [service.gridradar.net](https://service.gridradar.net))
4. Gewünschte Metriken auswählen
5. Aktualisierungsintervall festlegen (Standard: 60 Sekunden)

## API-Token

Einen kostenlosen Token gibt es nach Registrierung auf [service.gridradar.net](https://service.gridradar.net).

Der **Free**-Tarif bietet Zugriff auf:
- Netzfrequenz UCTE Median (1s)
- Netzzeit-Abweichung

Für weitere Metriken (100ms-Auflösung, Min/Max, aFRR) ist ein **Individual**-Account erforderlich.
