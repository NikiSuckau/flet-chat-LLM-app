---
title: VerticalDivider
sidebar_label: VerticalDivider
---

A thin vertical line, with padding on either side.

In the material design language, this represents a divider.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/verticaldivider)


```python reference
https://github.com/flet-dev/examples/blob/example-polishing/python/controls/layout/vertical-divider/divider-vert.py
```


<img src="/img/docs/controls/vertical-divider/vertical-divider.png" className="screenshot-40" />

## Properties

### `color`

The [color](/docs/reference/colors) to use when painting the line.

### `leading_indent`

The amount of empty space to the leading edge of the divider.

Defaults to `0.0`.

### `thickness`

The thickness of the line drawn within the divider. A divider with a thickness of `0.0` is always drawn as a line with a
width of exactly one device pixel.

Defaults to `0.0`.

### `trailing_indent`

The amount of empty space to the trailing edge of the divider.

Defaults to `0.0`.

### `width`

The divider's width. The divider itself is always drawn as a vertical line that is centered within the width specified
by this value. I

Defaults to `16.0`.
