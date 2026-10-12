<h1 align="center">Tetromino</h1>

<p align="center">
  <img src="svg/tetromino-i.svg" width="64" height="64" alt="I block">
  <img src="svg/tetromino-o.svg" width="64" height="64" alt="O block">
  <img src="svg/tetromino-t.svg" width="64" height="64" alt="T block">
  <img src="svg/tetromino-s.svg" width="64" height="64" alt="S block">
  <img src="svg/tetromino-z.svg" width="64" height="64" alt="Z block">
  <img src="svg/tetromino-j.svg" width="64" height="64" alt="J block">
  <img src="svg/tetromino-l.svg" width="64" height="64" alt="L block">
</p>

<p align="center">
  Seven tiny, friendly, animated four-block icons.<br>
  One self-contained SVG per shape · no JavaScript · no dependencies · under 1.5&nbsp;KB each.
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://www.npmjs.com/package/@lituus-io/tetromino"><img alt="npm" src="https://img.shields.io/npm/v/@lituus-io/tetromino.svg"></a>
</p>

---

## Contents

- [What's included](#whats-included)
- [Install](#install)
- [Usage](#usage)
  - [As an image](#as-an-image)
  - [Inline SVG](#inline-svg)
  - [JavaScript / TypeScript](#javascript--typescript)
  - [CSS background or `mask`](#css-background-or-mask)
- [Customising](#customising)
- [Sizes and legibility](#sizes-and-legibility)
- [Performance](#performance)
- [Accessibility](#accessibility)
- [Browser support](#browser-support)
- [Pro pack](#pro-pack)
- [Building from source](#building-from-source)
- [Contributing](#contributing)
- [License](#license)

## What's included

Tetrominoes are the seven shapes you can make by joining four equal squares edge to edge. This library draws each one as a small character with eyes, a smile and a soft highlight. It plays a gentle **drop** animation: the shape falls in, squashes on landing, settles, and blinks.

| Shape | File | Default colour |
|:-----:|------|----------------|
| <img src="svg/tetromino-i.svg" width="32" height="32" alt=""> **I** | `svg/tetromino-i.svg` | `#f43f5e` rose |
| <img src="svg/tetromino-o.svg" width="32" height="32" alt=""> **O** | `svg/tetromino-o.svg` | `#14b8a6` teal |
| <img src="svg/tetromino-t.svg" width="32" height="32" alt=""> **T** | `svg/tetromino-t.svg` | `#f59e0b` amber |
| <img src="svg/tetromino-s.svg" width="32" height="32" alt=""> **S** | `svg/tetromino-s.svg` | `#8b5cf6` violet |
| <img src="svg/tetromino-z.svg" width="32" height="32" alt=""> **Z** | `svg/tetromino-z.svg` | `#0ea5e9` sky |
| <img src="svg/tetromino-j.svg" width="32" height="32" alt=""> **J** | `svg/tetromino-j.svg` | `#84cc16` lime |
| <img src="svg/tetromino-l.svg" width="32" height="32" alt=""> **L** | `svg/tetromino-l.svg` | `#ec4899` pink |

Every file:

- is a single standalone SVG with its CSS animation embedded, so it works anywhere an image does
- draws on a 32 × 32 `viewBox` and scales cleanly from 16 px to any size
- can be recoloured with one CSS variable (`--c`)
- can be offset in time with `--delay` so a row of icons moves in a wave
- stops moving for people who have reduced motion turned on in their system settings
- has a static frame you can request with `#still`

A live demo page is in [`docs/index.html`](docs/index.html). Open it locally, or turn on GitHub Pages for the `docs/` folder.

## Install

**CDN (no install).** Link a file straight from jsDelivr. Pin a version tag in production:

```html
<img src="https://cdn.jsdelivr.net/gh/lituus-io/tetromino@v1.0.1/svg/tetromino-t.svg"
     width="32" height="32" alt="T block">
```

**npm.**

```sh
npm install @lituus-io/tetromino
```

**Download.** Copy the files you want from [`svg/`](svg/). There's nothing else to install.

## Usage

### As an image

```html
<img src="tetromino-t.svg" width="32" height="32" alt="T block">

<!-- static frame, no motion -->
<img src="tetromino-t.svg#still" width="32" height="32" alt="T block">
```

It also works in Markdown, which is how this README shows its icons:

```md
![T block](svg/tetromino-t.svg)
```

> An SVG loaded through `<img>` is sandboxed, so CSS variables on the page can't reach it. To recolour an icon, inline it (below) or edit `fill="var(--c,#…)"` in your copy of the file.

### Inline SVG

Paste the file contents into your HTML. Then page CSS can recolour it, delay it, or freeze it:

```html
<span style="--c:#0f766e; --delay:.3s">
  <!-- contents of tetromino-o.svg -->
</span>

<!-- class="still" on the <svg> element gives a static frame -->
<svg class="still" …>…</svg>
```

Each file defines its cell graphic with `id="c"`. If you inline **several different shapes on one page**, rename that id in each copy (for example `c` → `c-t` and `href="#c"` → `href="#c-t"`) so they don't pick up each other's colours. The demo page shows how this is done.

### JavaScript / TypeScript

The package exports each icon as a raw SVG string, so it needs no loader, plugin or framework.

```js
import shapes, { t, names, colors, dataUri } from '@lituus-io/tetromino';

el.innerHTML = t;                       // inline SVG markup
img.src = dataUri('l');                 // data: URI for <img> or CSS
names;                                  // ['i','o','t','s','z','j','l']
colors.s;                               // '#8b5cf6'
shapes[name];                           // look up by name
```

Types ship with the package (`type Shape = 'i' | 'o' | 't' | 's' | 'z' | 'j' | 'l'`).

To import the files directly in a bundler (Vite, webpack and others):

```js
import tUrl from '@lituus-io/tetromino/svg/tetromino-t.svg';
```

**React example**

```jsx
import { shapes } from '@lituus-io/tetromino';

export function Block({ shape = 't', size = 32, color, delay }) {
  return (
    <span
      role="img"
      aria-label={`${shape.toUpperCase()} block`}
      style={{ display: 'inline-block', width: size, height: size, '--c': color, '--delay': delay }}
      dangerouslySetInnerHTML={{ __html: shapes[shape].replace('width="32" height="32"', 'width="100%" height="100%"') }}
    />
  );
}
```

(The markup comes from this package, not from users, so `dangerouslySetInnerHTML` is safe here.)

### CSS background or `mask`

```css
.badge::before {
  content: "";
  display: inline-block;
  width: 1.25em;
  height: 1.25em;
  background: url("tetromino-z.svg") center / contain no-repeat;
}
```

## Customising

All the controls are CSS custom properties or classes. They take effect when the SVG is **inlined**:

| Control | Example | Effect |
|---------|---------|--------|
| `--c` | `--c: #0f766e` | Fill colour of the four cells. The highlight and edge shading adapt to it. |
| `--delay` | `--delay: .45s` | Starts the animation later. Stagger a row by giving each icon a slightly larger delay. |
| `--loops` | `--loops: 1` | How many times the animation plays (default `infinite`). Use `1` for a one-time entrance. |
| `#still` | `tetromino-t.svg#still` | Static frame. Works with `<img>` too. |
| `.still` | `<svg class="still">` | Static frame for inline SVG. |

A staggered row:

```html
<div class="row">
  <span style="--delay:0s">…i…</span>
  <span style="--delay:.15s">…o…</span>
  <span style="--delay:.3s">…t…</span>
</div>
```

The animation loops every 2.4 s. The drop takes up the first ~55% of each cycle and the shape rests for the rest.

## Sizes and legibility

| Rendered size | What you see |
|---------------|--------------|
| ≥ 24 px | Full character: cells, highlight, eyes, smile, blink |
| < 20 px | The face is hidden automatically, leaving just the shape and colour, which is what makes it recognisable at that size |

Set any `width`/`height`. The drawing scales from its `viewBox`.

## Performance

The icons are built to cost close to nothing, even with hundreds on one page:

- **Only `transform` and `opacity` are animated.** The browser can run these on the GPU compositor, so the animation causes no layout or repaint work and uses no main-thread JavaScript. CI rejects any keyframe that animates another property.
- **About 1.4 KB per file** before compression, and around 700 bytes gzipped. No fonts, images or scripts are pulled in.
- **No JavaScript** is needed to animate. The optional JS entry point only hands you the SVG strings.
- **Browsers skip off-screen work.** Animations inside `<img>` elements that aren't visible aren't painted.
- **Each cycle mostly rests.** The drop takes about 1.3 s of each 2.4 s loop. Set `--loops: 1` when you only need it once.

## Accessibility

- Each SVG has `role="img"` and an `aria-label` ("T block", and so on). Give `<img>` tags a meaningful `alt`, or `alt=""` if the icon is purely decorative.
- Motion stops for users who have reduced motion turned on (`prefers-reduced-motion: reduce`). You don't need to do anything.
- The animation never flashes, and each cycle ends in a long rest.

## Browser support

All current evergreen browsers (Chrome, Edge, Firefox, Safari on desktop and mobile). The icons use only standard SVG 1.1 shapes, `<use href>`, and CSS animations embedded in the SVG. Older environments that don't run SVG CSS animations show a correct static icon.

## Pro pack

This repository is the **free core**: the seven base shapes with the default drop animation, MIT-licensed, yours to use anywhere.

A paid **Pro pack** extends the same characters. It is sold separately under a commercial license and is not part of this repository:

- **Extra expressions:** more faces and moods for every shape
- **More motions:** *spin*, *turn* (quarter-turn clicks with overshoot) and *wobble* (a damped jelly rock), each selectable per icon
- **Lottie and GIF exports** for apps, slides, chat and anywhere SVG doesn't fit
- **Ready-made components** for popular frameworks

<!-- Replace with your storefront link(s) when the pack is live. -->
The Pro pack is coming soon. Watch or star this repository to get notified when it launches.

Purchases support continued development of the free core.

## Building from source

Every published file is generated by one standard-library Python script.

```sh
git clone https://github.com/lituus-io/tetromino.git
cd tetromino
python3 scripts/build.py   # writes svg/, index.js, index.d.ts, docs/index.html
npm test                   # validates SVGs, size budget and the JS entry point
```

Requirements: Python 3.8+ and Node 18+ (Node is only needed for `npm test`).

Repository layout:

```
svg/               the seven icons (generated)
index.js           ESM entry: SVG strings + helpers (generated)
index.d.ts         TypeScript types (generated)
docs/index.html    demo page (generated)
scripts/build.py   the generator, the single source of truth
scripts/check.py   validation run in CI
```

Edit `scripts/build.py`, not the generated files. CI rebuilds everything and fails if the committed output doesn't match.

## Contributing

Issues and pull requests are welcome, especially rendering bugs, accessibility improvements and size reductions. Please:

1. Change `scripts/build.py`, then run `python3 scripts/build.py` and `npm test`.
2. Commit the regenerated files with your change.
3. Keep each SVG under the 1.6 KB budget enforced by `scripts/check.py`.

New motions and expressions are part of the Pro pack, so pull requests that add them to this repository can't be accepted.

## License

Copyright © 2026 lituus-io. All rights reserved.
Author: spicyzhug@gmail.com

The code and icons in this repository are released under the [MIT License](LICENSE). The Pro pack is licensed separately.
