---
title: Radio
sidebar_label: Radio
---

Radio buttons let people select a single option from two or more choices.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/radio)

### Basic RadioGroup


```python reference
https://github.com/flet-dev/examples/blob/main/python/controls/input-and-selections/radio/radiogroup-basic.py
```


<img src="/img/docs/controls/radio/basic-radio.gif" className="screenshot-30"/>

### RadioGroup with `on_change` event



```python reference
https://github.com/flet-dev/examples/blob/main/python/controls/input-and-selections/radio/radiogroup-with-event.py
```


<img src="/img/docs/controls/radio/radio-with-change-event.gif" className="screenshot-30"/>

## `RadioGroup` properties

### `content`

The content of the RadioGroup. Typically a list of `Radio` controls nested in a container control, e.g. `Column`, `Row`.

### `value`

Current value of the RadioGroup.

## `RadioGroup` events

### `on_change`

Fires when the state of the RadioGroup is changed.

## `Radio` properties

### `active_color`

The [color](/docs/reference/colors) used to fill this radio when it is selected.

### `adaptive`

If the value is `True`, an adaptive Radio is created based on whether the target platform is iOS/macOS.

On iOS and macOS, a [`CupertinoRadio`](/docs/controls/cupertinoradio) is created, which has matching functionality and presentation as `Radio`, and the graphics as expected on iOS. On other platforms, a Material Radio is created.

Defaults to `False`.

### `autofocus`

True if the control will be selected as the initial focus. If there is more than one control on a page with autofocus set, then the first one added to the page will get focus.

### `fill_color`

The [color](/docs/reference/colors) that fills the radio, in all or
specific [`ControlState`](/docs/reference/types/controlstate) states.

### `focus_color`

The color of this radio when it has the input focus.

### `hover_color`

The color of this radio when it is hovered.

### `label`

The clickable label to display on the right of a Radio.

### `label_style`

The label's style.

Value is of type [`TextStyle`](/docs/reference/types/textstyle).

### `label_position`

Value is of type [`LabelPosition`](/docs/reference/types/labelposition) and defaults to `LabelPosition.RIGHT`.

### `mouse_cursor`

The cursor for a mouse pointer entering or hovering over this control.

Value is of type [`MouseCursor`](/docs/reference/types/mousecursor).

### `overlay_color`

The overlay [color](/docs/reference/colors) of this radio in all or
specific [`ControlState`](/docs/reference/types/controlstate) states.

### `splash_radius`

The splash radius of the circular Material ink response.

### `toggleable`

Set to `True` if this radio button is allowed to be returned to an indeterminate state by selecting it again when selected.

### `value`

The value to set to containing `RadioGroup` when the radio is selected.

### `visual_density`

Defines how compact the radio's layout will be.

Value is of type [`VisualDensity`](/docs/reference/types/visualdensity).

## `Radio` events

### `on_blur`

Fires when the control has lost focus.

### `on_focus`

Fires when the control has received focus.
