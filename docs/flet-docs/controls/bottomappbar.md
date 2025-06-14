---
title: BottomAppBar
sidebar_label: BottomAppBar
---

A material design bottom app bar.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/bottomappbar)

### BottomAppBar


```python reference
https://github.com/flet-dev/examples/blob/main/python/controls/navigation/bottom-app-bar/bottom-appbar.py
```


<img src="/img/docs/controls/bottom-app-bar/bottom-appbar.png" className="screenshot-40"/>

## Properties

### `bgcolor`

The fill [color](/docs/reference/colors) to use for the BottomAppBar. Default color is defined by current theme.

### `clip_behavior`

The content will be clipped (or not) according to this option.

Value is of type [`ClipBehavior`](/docs/reference/types/clipbehavior) and defaults to `ClipBehavior.NONE`.

### `content`

A child Control contained by the BottomAppBar.

### `elevation`

This property controls the size of the shadow below the BottomAppBar.

Defaults to `4`.

### `height`

The height of the BottomAppBar.

Defaults to `80.0` in material 3.

### `notch_margin`

The margin between the `FloatingActionButton` and the BottomAppBar's notch.

Can be visible only if `shape=None`.

### `padding`

Empty space to inscribe inside a container decoration (background, border). Padding is an instance
of [`Padding`](/docs/reference/types/padding) class.

Defaults to `padding.symmetric(vertical=12.0, horizontal=16.0)`.

### `shadow_color`

The [color](/docs/reference/colors) of the shadow below the BottomAppBar. 

### `shape`

The notch that is made for the floating action button.

Value is of type [`NotchShape`](/docs/reference/types/notchshape).

### `surface_tint_color`

The [color](/docs/reference/colors) used as an overlay on `bgcolor` to indicate elevation.

If this is `None`, no overlay will be applied. Otherwise this color will be composited on top of `bgcolor` with an opacity related to `elevation` and used to paint the BottomAppBar's background.

Defaults to `None`.
