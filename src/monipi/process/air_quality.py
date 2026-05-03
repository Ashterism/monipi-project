"""Air quality and climate interpretation helpers.

This module contains domain rules:
- what ranges are considered good / low / high
- how a raw value maps to a simple status
- how those ranges can be expressed for gauge-style chart

"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReadingThreshold:
    key: str
    label: str
    unit: str
    gauge_min: float
    gauge_max: float
    good_min: float | None
    good_max: float
    low_label: str = "Too low"
    good_label: str = "Good"
    high_label: str = "Too high"
    low_is_bad: bool = True


READING_THRESHOLDS = {
    "co2": ReadingThreshold(
        key="co2",
        label="CO₂",
        unit="ppm",
        gauge_min=0,
        gauge_max=2000,
        good_min=400,
        good_max=1000,
        low_label="Too low",
        good_label="Good",
        high_label="Too high",
        low_is_bad=False,
    ),
    "temperature": ReadingThreshold(
        key="temperature",
        label="Temperature",
        unit="°C",
        gauge_min=0,
        gauge_max=45,
        good_min=18,
        good_max=26,
        low_label="Cool",
        good_label="Comfortable",
        high_label="Warm",
        low_is_bad=False,
    ),
    "humidity": ReadingThreshold(
        key="humidity",
        label="Humidity",
        unit="%",
        gauge_min=0,
        gauge_max=100,
        good_min=30,
        good_max=60,
        low_label="Dry",
        good_label="Comfortable",
        high_label="Humid",
        low_is_bad=False,
    ),
    "pm1": ReadingThreshold(
        key="pm1",
        label="PM1",
        unit="µg/m³",
        gauge_min=0,
        gauge_max=80,
        good_min=None,
        good_max=10,
        low_label="Low",
        good_label="Good",
        high_label="Elevated",
        low_is_bad=False,
    ),
    "pm25": ReadingThreshold(
        key="pm25",
        label="PM2.5",
        unit="µg/m³",
        gauge_min=0,
        gauge_max=100,
        good_min=None,
        good_max=12,
        low_label="Low",
        good_label="Good",
        high_label="Elevated",
        low_is_bad=False,
    ),
    "pm10": ReadingThreshold(
        key="pm10",
        label="PM10",
        unit="µg/m³",
        gauge_min=0,
        gauge_max=150,
        good_min=None,
        good_max=45,
        low_label="Low",
        good_label="Good",
        high_label="Elevated",
        low_is_bad=False,
    ),
}


STATUS_COLOURS = {
    "low": "#f2b84b",
    "good": "#35d04fee",
    "high": "#e85b5b",
    "unknown": "#aeb7ad",
}

GAUGE_COLOURS = {
    "red": "#e85b5b",
    "amber": "#f2b84b",
    "green": "#35d04fee",
    "unknown": "#aeb7ad",
}


def get_threshold(reading_key: str) -> ReadingThreshold:
    """Return the threshold definition for a reading key."""
    return READING_THRESHOLDS[reading_key]


def get_reading_status(reading_key: str, value) -> dict:
    """Convert a raw reading value into a simple status dictionary."""
    threshold = get_threshold(reading_key)

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return {
            "key": reading_key,
            "value": None,
            "status": "unknown",
            "label": "Unknown",
            "colour": STATUS_COLOURS["unknown"],
        }

    if threshold.good_min is not None and numeric_value < threshold.good_min:
        status = "low"
        label = threshold.low_label
    elif numeric_value <= threshold.good_max:
        status = "good"
        label = threshold.good_label
    else:
        status = "high"
        label = threshold.high_label

    return {
        "key": reading_key,
        "value": numeric_value,
        "status": status,
        "label": label,
        "colour": STATUS_COLOURS[status],
    }


def get_gauge_bands(reading_key: str) -> list[list[float | str]]:
    """Return ECharts-style gauge bands for a reading.

    ECharts expects each band as [fraction_of_axis, colour].

    Readings with a meaningful low and high side use:
    red -> amber -> green -> amber -> red

    Readings where lower is simply better, such as particulate matter, use:
    green -> amber -> red
    """
    threshold = get_threshold(reading_key)

    gauge_range = threshold.gauge_max - threshold.gauge_min
    if gauge_range <= 0:
        return [[1, GAUGE_COLOURS["unknown"]]]

    good_max_fraction = _value_to_fraction(threshold.good_max, threshold)

    if threshold.good_min is None:
        amber_fraction = _value_to_fraction(threshold.good_max * 2, threshold)
        return [
            [good_max_fraction, GAUGE_COLOURS["green"]],
            [amber_fraction, GAUGE_COLOURS["amber"]],
            [1, GAUGE_COLOURS["red"]],
        ]

    good_min_fraction = _value_to_fraction(threshold.good_min, threshold)
    low_red_boundary = _midpoint_fraction(0, good_min_fraction)
    high_red_boundary = _midpoint_fraction(good_max_fraction, 1)

    return [
        [low_red_boundary, GAUGE_COLOURS["red"]],
        [good_min_fraction, GAUGE_COLOURS["amber"]],
        [good_max_fraction, GAUGE_COLOURS["green"]],
        [high_red_boundary, GAUGE_COLOURS["amber"]],
        [1, GAUGE_COLOURS["red"]],
    ]


# New function to return the basic gauge configuration needed by the UI layer.
def get_gauge_config(reading_key: str, value) -> dict:
    """Return the basic gauge configuration needed by the UI layer."""
    threshold = get_threshold(reading_key)
    status = get_reading_status(reading_key, value)

    return {
        "key": reading_key,
        "label": threshold.label,
        "unit": threshold.unit,
        "value": status["value"],
        "status": status["status"],
        "status_label": status["label"],
        "status_colour": status["colour"],
        "gauge_min": threshold.gauge_min,
        "gauge_max": threshold.gauge_max,
        "good_min": threshold.good_min,
        "good_max": threshold.good_max,
        "bands": get_gauge_bands(reading_key),
    }


def _value_to_fraction(value: float, threshold: ReadingThreshold) -> float:
    gauge_range = threshold.gauge_max - threshold.gauge_min
    return _clamp_fraction((value - threshold.gauge_min) / gauge_range)


def _midpoint_fraction(start: float, end: float) -> float:
    return _clamp_fraction(start + ((end - start) / 2))


def _clamp_fraction(value: float) -> float:
    return max(0, min(1, value))