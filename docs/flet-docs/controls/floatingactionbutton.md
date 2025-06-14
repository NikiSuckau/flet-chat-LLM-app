---
title: FloatingActionButton
sidebar_label: FloatingActionButton
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

A material design floating action button. A floating action button is a circular icon button that hovers over content to promote a primary action in the application.
Floating action button is usually set to `page.floating_action_button`, but can also be added as a regular control at any place on a page.

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/floatingactionbutton)

### Basic FAB


```python reference
https://github.com/flet-dev/examples/blob/main/python/controls/buttons/floating-action-button/floating-action-button.py
```


<img src="/img/docs/controls/floatingactionbutton/floating-action-button-example.gif"/>

## Properties

### `autofocus`

True if the control will be selected as the initial focus. If there is more than one control on a page with autofocus set, then the first one added to the page will get focus.

### `bgcolor`

Button background [color](/docs/reference/colors).

### `clip_behavior`

The content will be clipped (or not) according to this option.

Value is of type [`ClipBehavior`](/docs/reference/types/clipbehavior) and defaults to `ClipBehavior.NONE`.

### `content`

A Control representing custom button content.

### `disabled_elevation`

The button's elevation when disabled.

Defaults to the same value as `elevation`.

### `elevation`

The button's elevation.

Defaults to `6`.

### `enable_feedback`

Whether detected gestures should provide acoustic and/or haptic feedback. On Android, for example, setting this to `True` will produce a click sound and a long-press will produce a short vibration.

Defaults to `True`.

### `focus_color`

The [color](/docs/reference/colors) to use for filling the button when the button has input focus.

### `focus_elevation`

The button's elevation when it has input focus.

Defaults to `8`.

### `foreground_color`

The default foreground [color](/docs/reference/colors) for icons and text within the button.

### `highlight_elevation`

The button's elevation when being touched.

Defaults to `12`.

### `hover_elevation`

The button's elevation when it is enabled and being hovered.

Defaults to `8`.

### `icon`

Icon shown in the button.

### `mini`

Controls the size of this button.

By default, floating action buttons are non-mini and have a height and width of `56.0` logical pixels. Mini floating
action buttons have a height and width of `40.0` logical pixels with a layout width and height of `48.0` logical pixels.

### `mouse_cursor`

The cursor to be displayed when a mouse pointer enters or is hovering over this control.

Value is of type [`MouseCursor`](/docs/reference/types/mousecursor).

### `shape`

The shape of the FAB's border.

The value is an instance of [`OutlinedBorder`](/docs/reference/types/outlinedborder) class.

### `splash_color`

The [color](/docs/reference/colors) of the ripple shown when this button is pressed/clicked.

### `text`

The text displayed on a button.

### `tooltip`

The text displayed when hovering the mouse over the button.

### `url`

The URL to open when the button is clicked. If registered, `on_click` event is fired after that.

### `url_target`

Where to open URL in the web mode.

Value is of type [`UrlTarget`](/docs/reference/types/urltarget) and defaults to `UrlTarget.BLANK`.

## Events

### `on_click`

Fires when a user clicks the button.
