# Decor sources

All files are icons from Lucide (https://lucide.dev), licence ISC (see `src/LICENSE`, copied from
https://raw.githubusercontent.com/lucide-icons/lucide/main/LICENSE). Downloaded 2026-10-20 from the
project's GitHub, one file each:

`https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/<name>.svg`

Names: server, map-pin, triangle-alert, file-text, share-2, chart-no-axes-column, zap, cpu,
arrow-left-right, lock, workflow, sparkles, network, database, activity, radio, gauge, shield-check.

`src/` holds the unmodified downloads. `navy/ white/ sky/ blue/` are copies with `currentColor`
replaced by the theme colour (`make-decor.py`, plain text replace; no file is executed).
No illustrations or photos were downloaded.

## Logos on slide 8 (not decoration)
img/logos/*.png are crops of the logo figures already in the report (Figures 2.1–2.6); made by make-logos.py. The uv logo in the report image was broken, so slide 8 shows a text badge "uv" instead (no download).

## Leaf border (edge decoration, trial)
- Source: Material Symbols (google/material-design-icons, GitHub), rounded, FILL=1: eco, spa, grass, psychiatry, nest_eco_leaf
- URL pattern: https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/<name>/materialsymbolsrounded/<name>_fill1_24px.svg
- Licence: Apache License 2.0 (reuse allowed, no attribution on slides needed)
- Downloaded: 2026-10-20 into decor/src_material/ (unmodified); recoloured copies by make-decor.py (fill attribute text replace only; nothing executed)
- Used via Add-Border in lib-slides.ps1, switch -Leaf none|tint|green in build-slides.ps1 (default none)

**Status: UNUSED.** The user dropped the leaf border (2026-10-20). Files in decor/src_material/ stay but no slide uses them; build-slides.ps1 -Leaf defaults to none.

## Photos on slides 3-5 (Wikimedia Commons, fetched by fetch-photos.py, downloaded 2026-10-20, saved in decor/photos/, 1000 px thumbnails, only image bytes checked with Pillow)
| file | Commons page | author | licence | on-slide credit |
|---|---|---|---|---|
| inverter.jpg | https://commons.wikimedia.org/wiki/File:Central_inverter_cutout.jpg | SayCheeeeeese | CC0 | listed anyway |
| plc_panel.jpg | https://commons.wikimedia.org/wiki/File:Iron_ore_washing_plant_control_cabin_and_plc_control_panel_(6325230947).jpg | Peter Craven | CC BY 2.0 (https://creativecommons.org/licenses/by/2.0) | yes, slide 4 |
| line.jpg | https://commons.wikimedia.org/wiki/File:001_Car_factory_assembly_line_-_Opel_factory_in_Gliwice,_Poland.jpg | Marek Ślusarczyk (Tupungato) | CC BY 3.0 (https://creativecommons.org/licenses/by/3.0) | yes, slide 4 |
| scada.jpg | https://commons.wikimedia.org/wiki/File:US_Navy_110328-N-OJ170-009_Hideji_Kawasaki_operates_the_supervisory_control_and_data_acquisition_(SCADA)_system_to_balance_an_electrical_load_insid.jpg | U.S. Navy photo by Joe Schmitt | Public domain | no |
*_c.jpg are 9:8 centre crops (make-crops.py). Photos are cropped only; no other changes.

## Cartoon illustrations — soco-st (added 2026-10-20)
Terms: https://soco-st.com/guide (read 2026-10-20). Free for commercial/non-commercial use incl. teaching materials and documents; credit and prior contact NOT required; no image-count limit; resize/recolour/trim allowed; no redistribution, no AI training/reference, no face alteration. Downloaded (not hotlinked) as `<id>_paint.png` into `decor/soco/` by `fetch-soco.py`; metadata in `decor/soco/soco.json`. A small "ภาพการ์ตูน: soco-st" credit sits on slide 4 anyway.
Not used: shigureni (https://shigureni.com/terms — free only up to 5 images per work, 6th+ ¥1,000), irasutoya (https://www.irasutoya.com/p/terms.html — 21+ images in a commercial design need a paid arrangement; style would mix).
| id | page | use |
|---|---|---|
| 15162 | https://soco-st.com/15162 | cover |
| 27646 | https://soco-st.com/27646 | closing |
| 29412 | https://soco-st.com/29412 | divider 1 |
| 17500 | https://soco-st.com/17500 | divider 2 |
| 17567 | https://soco-st.com/17567 | divider 3 |
| 26698 | https://soco-st.com/26698 | divider 4 |
| 11324 | https://soco-st.com/11324 | divider 5 |
| 27268 | https://soco-st.com/27268 | problem col 3 |
| 27122 | https://soco-st.com/27122 | goals |
| 18010 | https://soco-st.com/18010 | basics |
| 26707 | https://soco-st.com/26707 | web UI |
| 9780 | https://soco-st.com/9780 | results |
| 27151 | https://soco-st.com/27151 | future |

## Photo: Huawei SUN2000 inverter (added 2026-10-20)
File: `Bregenz-indoor swimming pool (in construction)--PV-Inverter Huawei SUN2000-10KTL-(M2)-01ASD.jpg`, https://commons.wikimedia.org/wiki/File:Bregenz-indoor_swimming_pool_(in_construction)--PV-Inverter_Huawei_SUN2000-10KTL-(M2)-01ASD.jpg — author Asurnipal, CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0), 2025-01-24, fetched 2026-10-20 (960 px) -> `decor/photos/huawei_full.jpg`, 9:8 crop `huawei_c.jpg`. It is the SUN2000-10KTL-(M2), the same family as the report's SUN2000-5KTL profile; no licensed photo of the exact -5KTL was found. No Commons photo of the Eastron SDM630 was found (searches "Eastron SDM630", "Eastron energy meter" returned nothing). Replaces the CC0 "Central inverter cutout" on slide 4 (file kept, unused). The Opel assembly-line photo (CC BY 3.0) is no longer used.

Rule 2026-10-20: no real people on slides. `scada.jpg` / `scada_c.jpg` (a person in the frame) are no longer used; slide 3 now uses the soco-st monitors cartoon (`decor/soco/18010.png`). The remaining photos (Huawei inverter, PLC cabinet) show no person.
