---
title: ShakeDetector
sidebar_label: ShakeDetector
---

Detects phone shakes.

It is non-visual and should be added to `page.overlay` list.

## Examples

### Shake detector sample

```python reference
https://github.com/flet-dev/examples/blob/main/python/controls/utility/shake-detector/shake-detector-example.py
```

## Properties

### `minimum_shake_count`

Number of shakes required before shake is triggered.

Defaults to `1`.

### `shake_count_reset_time_ms`

Time, in milliseconds, before shake count resets.

Defaults to `3000`.

### `shake_slop_time_ms`

Minimum time between shakes, in milliseconds.

Defaults to `500`.

### `shake_threshold_gravity`

Shake detection threshold, in Gs.

Defaults to `2.7`.

## Events

### `on_shake`

Triggers when the shake detected.
