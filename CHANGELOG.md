# Changelog

## 1.1.1 (2026-10-13)

- Live demo: click any icon to copy its `<img>` tag, npm import or inline SVG, or download the file
- README: ready-to-paste `<img>` tags for every drop and motion icon

## 1.1.0 (2026-10-13)

- Five new motions for every shape, as 35 animated SVGs in `svg/motion/`: spin, turn, wobble, squash and melt
- Each motion file uses its own ids and class names, so any number can be inlined on one page
- The demo page and README show every motion

## 1.0.1 (2026-10-12)

- Cell colour is now set through a per-shape CSS rule, so `--c` recolouring and the default colours behave the same in every browser
- `--loops` sets how many times the animation plays
- CI rejects keyframes that animate anything other than `transform` and `opacity`

## 1.0.0 (2026-10-12)

First public release.

- Seven animated SVG icons (I, O, T, S, Z, J, L) with the drop animation and blink
- `#still` / `.still` static frame
- `--c` colour and `--delay` offset custom properties
- Face hidden automatically below 20 px
- `prefers-reduced-motion` support
- ESM entry point with SVG strings, `names`, `colors`, `dataUri()` and TypeScript types
