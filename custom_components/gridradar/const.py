"""Konstanten für die Gridradar-Integration."""

DOMAIN = "gridradar"
DEFAULT_SCAN_INTERVAL = 60  # Sekunden

API_BASE_URL = "https://api.gridradar.net"

# Verfügbare Metriken
METRICS = {
    "frequency_ucte_median_1s": {
        "key": "frequency-ucte-median-1s",
        "name": "Netzfrequenz UCTE (Median)",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
        "free_tier": True,
    },
    "net_time": {
        "key": "net-time",
        "name": "Netzzeit-Abweichung",
        "unit": "s",
        "icon": "mdi:clock-alert-outline",
        "device_class": None,
        "state_class": "measurement",
        "free_tier": True,
    },
    "frequency_ucte_median_100ms": {
        "key": "frequency-ucte-median-100ms",
        "name": "Netzfrequenz UCTE (Median 100ms)",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
        "free_tier": False,
    },
    "frequency_ucte_min_1s": {
        "key": "frequency-ucte-min-1s",
        "name": "Netzfrequenz UCTE (Min)",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
        "free_tier": False,
    },
    "frequency_ucte_max_1s": {
        "key": "frequency-ucte-max-1s",
        "name": "Netzfrequenz UCTE (Max)",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
        "free_tier": False,
    },
    "afrr_activated_15m": {
        "key": "afrr-activated-15m",
        "name": "aFRR aktiviert (15 Min)",
        "unit": "MW",
        "icon": "mdi:lightning-bolt",
        "device_class": "power",
        "state_class": "measurement",
        "free_tier": False,
    },
}

CONF_API_TOKEN = "api_token"
CONF_METRICS = "metrics"
CONF_SCAN_INTERVAL = "scan_interval"
