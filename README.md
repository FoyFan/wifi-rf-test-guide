# Wi-Fi RF Test Guide / Wi-Fi 射频八项测试指南

Bilingual (中文/English) static site detailing the 8 core Wi-Fi RF conducted tests: purpose, setup, step-by-step procedure, pass criteria and common pitfalls.

通过 GitHub Pages 访问 / View via GitHub Pages: https://foyfan.github.io/wifi-rf-test-guide/

## The 8 tests

| # | Test | 中文 |
|---|------|------|
| 01 | Transmit power | 发射功率 |
| 02 | Transmit spectrum mask | 发射频谱模板 |
| 03 | Modulation accuracy (EVM) | 调制精度 |
| 04 | Frequency error | 发射频率误差 |
| 05 | Center frequency leakage | 中心频率泄漏 |
| 06 | Spectral flatness | 频谱平坦度 |
| 07 | RX minimum input sensitivity | 接收机最小输入灵敏度 |
| 08 | RX maximum input level | 接收机最大输入电平 |

## Structure

- `index.html` — landing page with cards + language toggle
- `0*.html` — one detail page per test (purpose / setup / procedure / pass criteria / pitfalls)
- `style.css` — shared stylesheet (dark/light aware)
- `gen_pages.py` — generator script that builds the 8 detail pages

## Editing

Edit `gen_pages.py` and re-run:

```bash
python3 gen_pages.py
```

Then commit the regenerated HTML.

Limits and clause numbers cited per test follow **IEEE Std 802.11-2016** (consolidated OFDM/HT/VHT numbering, Clauses 17/20/21 — TX §17.3.9.x, RX §17.3.10.x). 802.11-2016 was superseded by 802.11-2020, itself by 802.11-2024, with identical clause numbering. Regulatory limits: FCC Part 15.247/15.407 and ETSI EN 300 328/301 893 — always defer to your customer's spec sheet.
