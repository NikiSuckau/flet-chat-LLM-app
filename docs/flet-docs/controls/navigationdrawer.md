---
title: NavigationDrawer
sidebar_label: NavigationDrawer
---

Material Design Navigation Drawer component.

Navigation Drawer is a panel that slides in horizontally from the left or right edge of a page to show primary destinations in an app. To add NavigationDrawer to the page, use [`page.drawer`](/docs/controls/page#drawer) and [`page.end_drawer`](/docs/controls/page#end_drawer) properties. Similarly, the NavigationDrawer can be added to a [`View`](/docs/controls/view#drawer). To display the drawer, set its `open` property to `True`.

To open this control, simply call the [`page.open()`](/docs/controls/page#opencontrol) helper-method.

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/navigationdrawer)

### NavigationDrawer sliding from the left edge of a page

<img src="/img/docs/controls/navigationdrawer/navigation-drawer-start.gif" className="screenshot-60"/>

```python reference
https://github.com/flet-dev/examples/blob/main/python/controls/navigation/navigation-drawer/nav-drawer-example.py
```

### NavigationDrawer sliding from the right edge of a page

<img src="/img/docs/controls/navigationdrawer/navigation-drawer-end.gif" className="screenshot-60"/>

```python reference
https://github.com/flet-dev/examples/blob/main/python/controls/navigation/navigation-drawer/nav-drawer-end.py
```

## `NavigationDrawer` properties

### `bgcolor`

The [color](/docs/reference/colors) of the navigation drawer itself.

### `controls`

Defines the appearance of the items within the navigation drawer.

The list contains `NavigationDrawerDestination` items and/or other controls such as headlines and dividers.

### `elevation`

The elevation of the navigation drawer itself.

### `indicator_color`

The [color](/docs/reference/colors) of the selected destination indicator.

### `indicator_shape`

The shape of the selected destination indicator.

Value is of type [`OutlinedBorder`](/docs/reference/types/outlinedborder).

### `position`

The position of this drawer.

Value is of type [`NavigationDrawerPosition`](/docs/reference/types/navigationdrawerposition) and defaults
to `NavigationDrawerPosition.START`.

### `selected_index`

The index for the current selected `NavigationDrawerDestination` or null if no destination is selected.

A valid selected_index is an integer between 0 and number of destinations - `1`. For an invalid `selected_index`, for
example, `-1`, all destinations will appear unselected.

### `shadow_color`

The [color](/docs/reference/colors) used for the drop shadow to indicate `elevation`.

### `surface_tint_color`

The surface tint of the Material that holds the NavigationDrawer's contents.

### `tile_padding`

Defines the padding for `NavigationDrawerDestination` controls.

## `NavigationDrawer` events

### `on_change`

Fires when selected destination changed.

### `on_dismiss`

Fires when drawer is dismissed by clicking outside of the panel or [programmatically](/docs/controls/page#closecontrol).

## `NavigationDrawerDestination` properties

### `bgcolor`

The [color](/docs/reference/colors) of this destination.

### `icon`

The [name of the icon](/docs/reference/icons) or `Control` of the destination. 

Example with icon name:
```
icon=ft.Icons.BOOKMARK
```
Example with Control:
```
icon=ft.Icon(ft.Icons.BOOKMARK)
```

If `selected_icon` is provided, this will only be displayed when the destination is not selected.

### ~~`icon_content`~~

The icon `Control` of the destination. Typically the icon is an [`Icon`](/docs/controls/icon) control. Used instead of `icon` property.

**Deprecated in v0.25.0 and will be removed in v0.28.0. Use [`icon`](#icon)
instead.**

### `label`

The text label that appears below the icon of this `NavigationDrawerDestination`.

### `selected_icon`

The [name](/docs/reference/icons) of alternative icon or `Control` displayed when this destination is selected. 

Example with icon name:
```
selected_icon=ft.Icons.BOOKMARK
```
Example with Control:
```
selected_icon=ft.Icon(ft.Icons.BOOKMARK)
```

If this icon is not provided, the NavigationDrawer will display `icon` in either state.

### ~~`selected_icon_content`~~

An alternative icon `Control` displayed when this destination is selected.

**Deprecated in v0.25.0 and will be removed in v0.28.0. Use [`selected_icon`](#selected_icon)
instead.**
