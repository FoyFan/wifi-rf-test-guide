#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the 8 bilingual sub-pages for the Wi-Fi RF test guide."""

HEAD = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="style.css">
</head>
<body data-lang="zh">
<div class="wrap">
<p class="crumb"><a href="index.html">&larr; Wi-Fi RF Test Guide</a></p>
<h1>{zh_title}<span class="en-title">{en_title}</span></h1>
<p class="lede zh">{zh_lede}</p>
<p class="lede en">{en_lede}</p>
<div class="lang">
<button class="on" onclick="setLang('zh')">中文</button>
<button onclick="setLang('en')">English</button>
</div>
"""

FOOT = """</div>
<script>
function setLang(l){document.body.dataset.lang=l;
document.querySelectorAll('.lang button').forEach(b=>b.classList.toggle('on',b.textContent.toLowerCase().startsWith(l)));}
</script>
</body>
</html>
"""


def section(h2_zh, h2_en, body):
    return f'<section><h2>{h2_zh}<span class="en"> / {h2_en}</span></h2>\n{body}\n</section>\n'


def zh(s):
    return f'<span class="zh">{s}</span>'


def en(s):
    return f'<span class="en">{s}</span>'


PAGES = {}

# ---------------------------------------------------------------- 01 TX power
PAGES["01-tx-power.html"] = {
    "title": "01 Transmit power — Wi-Fi RF Test Guide",
    "zh_title": "01 发射功率 Transmit power",
    "en_title": "01 Transmit power",
    "zh_lede": "测量设备发射信号的最大强度（dBm）。功率过高会违规/干扰他人，过低则覆盖不足。",
    "en_lede": "Measure the DUT's transmit level in dBm. Too high violates regulations; too low kills coverage.",
    "sections": [
        section("测试目的", "Purpose",
            "<ul>"
            + zh("<li>验证各信道/速率/天线口的发射功率在规格范围内，且各信道间差异（功率平坦度）达标。</li>"
                 "<li>这是法规认证（FCC/CE/SRRC）的强制项，也是产线校准的核心项。</li>")
            + en("<li>Verify TX power per channel/rate/antenna is within spec, and inter-channel flatness is acceptable.</li>"
                 "<li>Mandatory for regulatory certification (FCC/CE/SRRC) and a core production-line item.</li>")
            + "</ul>"),
        section("环境搭建", "Setup",
            "<ol>"
            + zh("<li>DUT 放入屏蔽箱，RF 口通过线缆/耦合器接到综合测试仪（或频谱仪）。</li>"
                 "<li><b>校线损</b>：用网分或功率计测出线缆在各频点（2.412/2.437/2.472 GHz、5.18/5.5/5.8 GHz…）的损耗，输入测试软件补偿。</li>"
                 "<li>用芯片厂工具（wlu / art2 / MP tool）让 DUT 进入测试模式，脱离协议栈。</li>")
            + en("<li>Put the DUT in a shield box; connect its RF port to the combo tester (or spectrum analyzer) via cable/coupler.</li>"
                 "<li><b>Calibrate cable loss</b> at each working frequency and compensate in software.</li>"
                 "<li>Use the vendor tool (wlu / art2 / MP tool) to enter test mode.</li>")
            + "</ol>"),
        section("测试步骤", "Procedure",
            "<ol>"
            + zh("<li>DUT 设为连续发射（Continuous TX）或发满速率包流，固定信道/速率/带宽。</li>"
                 "<li>仪器测信道内<b>平均功率</b>（多个包取平均），检波用 RMS/Average。</li>"
                 "<li>遍历每个信道、每档速率、每根天线（如 2.4G 的 1/6/11 信道 × 11b/g/n 各速率）。</li>"
                 "<li>补偿：DUT 实际功率 = 仪器读数 + 线损。</li>")
            + en("<li>Set continuous TX or a full-rate packet stream; fix channel/rate/bandwidth.</li>"
                 "<li>Measure in-channel <b>average power</b> (average over many bursts, RMS/average detector).</li>"
                 "<li>Sweep every channel, rate and antenna (e.g. 2.4G ch 1/6/11 × 11b/g/n rates).</li>"
                 "<li>Compensate: actual DUT power = instrument reading + cable loss.</li>")
            + "</ol>"),
        section("判定标准", "Pass criteria",
            "<ul>"
            + zh("<li>功率在规格范围内：法规限值（如 FCC 2.4G ≤ +30 dBm EIRP）以内，产品规格通常定 18~23 dBm。</li>"
                 "<li>信道间功率差异通常 ≤ 1.5~2 dB，否则说明校准表有问题。</li>")
            + en("<li>Power within spec: below the regulatory limit (e.g. FCC 2.4G ≤ +30 dBm EIRP); product specs typically 18–23 dBm.</li>"
                 "<li>Inter-channel delta typically ≤ 1.5–2 dB, otherwise the calibration table is suspect.</li>")
            + "</ul>"),
        section("常见坑", "Pitfalls",
            "<ul>"
            + zh("<li>不校线损 → 功率虚高/虚低，全表失真。</li>"
                 "<li>频谱仪用峰值检波 vs 综合仪用平均检波，读数会打架——统一按标准配置。</li>")
            + en("<li>Skipping cable-loss calibration corrupts every number.</li>"
                 "<li>Peak vs average detector makes instruments disagree — follow the standard's configuration.</li>")
            + "</ul>"),
    ],
}

# ------------------------------------------------------ 02 Spectrum mask
PAGES["02-tx-spectrum-mask.html"] = {
    "title": "02 Transmit spectrum mask — Wi-Fi RF Test Guide",
    "zh_title": "02 发射频谱模板 Spectrum mask",
    "en_title": "02 Transmit spectrum mask",
    "zh_lede": "规定发射能量在信道内外的分布形状，要求带外/邻频泄漏必须低于标准模板线。",
    "en_lede": "Constrains the shape of the transmitted spectrum; out-of-channel leakage must fall below the standard mask.",
    "sections": [
        section("测试目的", "Purpose",
            "<ul>"
            + zh("<li>防止能量泄漏到相邻信道造成干扰——这是 FCC/CE 法规强制项。</li>"
                 "<li>验证占用带宽（OBW）不超标。</li>")
            + en("<li>Prevent adjacent-channel interference — mandatory under FCC/CE.</li>"
                 "<li>Also verifies occupied bandwidth (OBW).</li>")
            + "</ul>"),
        section("测试步骤", "Procedure",
            "<ol>"
            + zh("<li>DUT 发<b>真实 OFDM 调制信号</b>（不能用单载波 CW，否则结果完全无效）。</li>"
                 "<li>频谱仪调到信道中心，RBW=100 kHz（按标准），VBW ≥ 3×RBW，RMS 检波。</li>"
                 "<li>测信道中心 ±N MHz：20 MHz 信道测到 ±40 MHz；40 MHz 测到 ±60 MHz。</li>"
                 "<li>用 packet burst 触发，确保抓到完整数据包。</li>"
                 "<li>将实测包络与标准模板线叠加对比，并测 99% 占用带宽。</li>")
            + en("<li>DUT transmits <b>real OFDM modulation</b> (never CW — results would be invalid).</li>"
                 "<li>Analyzer at channel center, RBW=100 kHz per the standard, VBW ≥ 3×RBW, RMS detector.</li>"
                 "<li>Sweep ±N MHz around the channel: ±40 MHz for a 20 MHz channel, ±60 MHz for 40 MHz.</li>"
                 "<li>Trigger on the packet burst to capture complete packets.</li>"
                 "<li>Overlay the measured envelope on the mask; also measure 99% OBW.</li>")
            + "</ol>"),
        section("判定标准", "Pass criteria",
            "<ul>"
            + zh("<li>每一点带外衰减都不得高于模板线。802.11 典型值：中心 ±11 MHz 内 0 dBr；±20 MHz 处 ≤ −20 dBr；±30 MHz 处 ≤ −28 dBr（不同带宽/代际限值不同）。</li>"
                 "<li>99% 功率带宽不得超限。</li>")
            + en("<li>No point may rise above the mask. Typical 802.11 values: 0 dBr within ±11 MHz; ≤ −20 dBr at ±20 MHz; ≤ −28 dBr at ±30 MHz (varies with bandwidth/generation).</li>"
                 "<li>99% OBW must not exceed the limit.</li>")
            + "</ul>"),
        section("常见坑", "Pitfalls",
            "<ul>"
            + zh("<li>用 CW 代替调制信号 → 结果完全错误。</li>"
                 "<li>RBW 设置不符标准 → 模板对比无意义。</li>")
            + en("<li>Using CW instead of modulation invalidates the result.</li>"
                 "<li>Wrong RBW makes the mask comparison meaningless.</li>")
            + "</ul>"),
    ],
}

# ---------------------------------------------------------------- 03 EVM
PAGES["03-evm.html"] = {
    "title": "03 EVM (modulation accuracy) — Wi-Fi RF Test Guide",
    "zh_title": "03 调制精度 EVM",
    "en_title": "03 Transmit modulation accuracy (EVM)",
    "zh_lede": "衡量调制波形“准不准”——实际星座点与理想星座点的偏差，直接决定最高可用调制速率。",
    "en_lede": "How accurate the modulated waveform is — the deviation of actual constellation points from ideal. It caps the top usable MCS.",
    "sections": [
        section("测试目的", "Purpose",
            "<ul>"
            + zh("<li>EVM 太大时对端解调不出数据，直接限制最高速率（256QAM/1024QAM 对 EVM 要求更苛刻）。</li>"
                 "<li>这是最能暴露射频链路问题（相位噪声、IQ 不平衡、PA 压缩）的测试。</li>")
            + en("<li>High EVM breaks demodulation and caps the top rate; 256QAM/1024QAM demand tight EVM.</li>"
                 "<li>The most revealing test for phase noise, IQ imbalance and PA compression.</li>")
            + "</ul>"),
        section("测试步骤", "Procedure",
            "<ol>"
            + zh("<li>DUT 发<b>最高阶调制</b>的满速率包（11ax MCS11 = 1024QAM；11ac 的 256QAM）——EVM 只在最高阶调制下才暴露问题。</li>"
                 "<li>综合仪/VSA 解调，对每个 OFDM 符号的每个子载波计算：EVM(dB) = 20·log₁₀(误差矢量幅值 / 理想幅值)。</li>"
                 "<li>测 100~1000 个包取统计。</li>"
                 "<li>报告：平均 EVM、最差子载波 EVM、最差符号 EVM、EVM 随时间/子载波分布图。</li>")
            + en("<li>DUT transmits full-rate packets at the <b>highest-order modulation</b> (11ax MCS11 = 1024QAM; 256QAM for 11ac) — EVM problems only show there.</li>"
                 "<li>Demodulate with the VSA; per subcarrier and symbol compute EVM(dB) = 20·log₁₀(|error| / |ideal|).</li>"
                 "<li>Collect 100–1000 bursts for statistics.</li>"
                 "<li>Report mean EVM, worst subcarrier, worst symbol, and EVM vs time/subcarrier plots.</li>")
            + "</ol>"),
        section("判定标准", "Pass criteria",
            "<table><tr><th>调制 Modulation</th><th>EVM 限值 Limit</th></tr>"
            "<tr><td>QPSK</td><td>≤ −10 dB (35%)</td></tr>"
            "<tr><td>16QAM</td><td>≤ −16 dB (16%)</td></tr>"
            "<tr><td>64QAM</td><td>≤ −25 dB (5.6%)</td></tr>"
            "<tr><td>256QAM</td><td>≤ −30 dB (3.2%)</td></tr>"
            "<tr><td>1024QAM (11ax MCS10/11)</td><td>≤ −35 dB (1.8%)</td></tr></table>"),
        section("结果分析", "Analysis",
            "<ul>"
            + zh("<li>只有边缘子载波 EVM 差 → 频偏/相位噪声问题。</li>"
                 "<li>符号首尾 EVM 差 → IQ 不平衡或时域漂移。</li>"
                 "<li>整体 EVM 差 → PA 压缩或功率过高，先降功率再看。</li>")
            + en("<li>Only edge subcarriers bad → frequency offset / phase noise.</li>"
                 "<li>First/last symbols bad → IQ imbalance or timing drift.</li>"
                 "<li>Uniformly bad → PA compression or over-power; lower power and retry.</li>")
            + "</ul>"),
        section("常见坑", "Pitfalls",
            "<ul>"
            + zh("<li>只看平均 EVM → 边缘子载波/偶发符号劣化测不出来，实际用网会掉速率。</li>"
                 "<li>用低阶调制测 EVM → 永远 pass，但毫无信息量。</li>")
            + en("<li>Mean-only EVM hides edge-subcarrier or sporadic degradation; real networks will drop rate.</li>"
                 "<li>Testing EVM at low-order modulation always passes and tells you nothing.</li>")
            + "</ul>"),
    ],
}

# -------------------------------------------------------- 04 Freq error
PAGES["04-freq-error.html"] = {
    "title": "04 Frequency error — Wi-Fi RF Test Guide",
    "zh_title": "04 发射频率误差 Frequency error",
    "en_title": "04 Transmit frequency error",
    "zh_lede": "测载波实际频率与标称频率的偏差（ppm），主要反映晶振精度与 AFC 校准质量。",
    "en_lede": "Carrier offset from the nominal frequency in ppm; reflects crystal accuracy and AFC calibration.",
    "sections": [
        section("测试目的", "Purpose",
            "<ul>"
            + zh("<li>频偏过大时接收端可能无法锁定/解调，尤其在高阶调制和长帧下。</li>"
                 "<li>频偏主要来源是晶振（±20 ppm 级别），靠产线 AFC 校准补偿。</li>")
            + en("<li>Large offset prevents the receiver from locking/demodulating, especially at high MCS and long frames.</li>"
                 "<li>Mainly from the crystal (±20 ppm class); compensated by production AFC calibration.</li>")
            + "</ul>"),
        section("测试步骤", "Procedure",
            "<ol>"
            + zh("<li>DUT 发正常调制包（不用连续波——解调法估的是残余频偏）。</li>"
                 "<li>仪器解调后估计载波频偏，报 ppm = (频偏 / 载波频率) × 10⁶。</li>"
                 "<li>多信道都测：锁相环在不同频点表现可能不同。</li>"
                 "<li>温度敏感：严谨场景在高低温下复测。</li>")
            + en("<li>DUT sends normal modulated packets (demodulation estimates residual offset).</li>"
                 "<li>Report ppm = (offset / carrier frequency) × 10⁶.</li>"
                 "<li>Test several channels — PLL behavior varies by frequency.</li>"
                 "<li>Temperature-sensitive: re-test at temperature extremes for rigorous runs.</li>")
            + "</ol>"),
        section("判定标准", "Pass criteria",
            "<ul>"
            + zh("<li>≤ ±20 ppm（802.11 标准值）。</li>"
                 "<li>产线常用 ±10 ppm 作为校准通过判据。</li>")
            + en("<li>≤ ±20 ppm per IEEE 802.11.</li>"
                 "<li>Production lines often gate at ±10 ppm.</li>")
            + "</ul>"),
        section("超标处理", "If it fails",
            "<ul>"
            + zh("<li>产线做 AFC（自动频率校准）写入校准数据后复测。</li>"
                 "<li>若 AFC 后仍超标，查晶振规格或晶体负载电容匹配。</li>")
            + en("<li>Run AFC on the line, write calibration data, re-test.</li>"
                 "<li>If still failing, check the crystal spec and load-capacitor matching.</li>")
            + "</ul>"),
    ],
}

# ------------------------------------------------------- 05 DC leakage
PAGES["05-dc-leakage.html"] = {
    "title": "05 Center frequency leakage — Wi-Fi RF Test Guide",
    "zh_title": "05 中心频率泄漏 DC leakage",
    "en_title": "05 Transmit center frequency leakage",
    "zh_lede": "测 OFDM 直流子载波上的本振泄漏能量——相当于一个“跑不掉的干扰杂音”。",
    "en_lede": "LO leakage on the OFDM DC subcarrier — an interfering tone that cannot be filtered out.",
    "sections": [
        section("测试目的", "Purpose",
            "<ul>"
            + zh("<li>OFDM 跳过 DC 子载波传数据，中心残留能量全部是本振（LO）泄漏。</li>"
                 "<li>泄漏会压低邻近子载波的解调性能，也抬高 EVM。</li>")
            + en("<li>OFDM leaves the DC subcarrier unused, so any energy there is LO leakage.</li>"
                 "<li>It degrades neighboring subcarriers' demodulation and inflates EVM.</li>")
            + "</ul>"),
        section("测试步骤", "Procedure",
            "<ol>"
            + zh("<li>DUT 发 OFDM 调制包。</li>"
                 "<li>仪器解调后专门看<b>直流子载波（DC carrier）</b>上的功率。</li>"
                 "<li>报值：DC 子载波功率相对平均子载波功率的比值（dB）。</li>")
            + en("<li>DUT sends OFDM packets.</li>"
                 "<li>Demodulate and inspect the <b>DC subcarrier</b> power specifically.</li>"
                 "<li>Report the DC power relative to the average subcarrier power (dB).</li>")
            + "</ol>"),
        section("判定标准", "Pass criteria",
            "<ul>"
            + zh("<li>≤ −15 dB（802.11 典型要求，不同标准版本略有差异）。</li>")
            + en("<li>≤ −15 dB (typical 802.11 requirement; varies slightly by standard revision).</li>")
            + "</ul>"),
        section("超标分析", "If it fails",
            "<ul>"
            + zh("<li>IQ 调制器本振馈通过大 → 硬件问题，查调制器设计。</li>"
                 "<li>DC offset 校准没做好 → 重跑产线 DC 校准。</li>")
            + en("<li>Excessive LO feed-through → hardware issue in the IQ modulator.</li>"
                 "<li>Poor DC-offset calibration → re-run the production DC calibration.</li>")
            + "</ul>"),
    ],
}

# ---------------------------------------------------- 06 Flatness
PAGES["06-spectral-flatness.html"] = {
    "title": "06 Spectral flatness — Wi-Fi RF Test Guide",
    "zh_title": "06 频谱平坦度 Spectral flatness",
    "en_title": "06 Transmit spectral flatness",
    "zh_lede": "整个信道带宽内各子载波功率应基本一致——频谱“高低不平”会让部分子载波传的数据出错。",
    "en_lede": "Subcarrier power across the channel should be flat; ripple corrupts data on the weak subcarriers.",
    "sections": [
        section("测试目的", "Purpose",
            "<ul>"
            + zh("<li>发现滤波器滚降、频偏、信道估计等问题。</li>"
                 "<li>平坦度差 → 部分子载波 SNR 低 → 高阶调制时这些子载波必然出错。</li>")
            + en("<li>Reveals filter roll-off, frequency offset and channel-estimation issues.</li>"
                 "<li>Poor flatness → low SNR subcarriers → guaranteed errors at high MCS.</li>")
            + "</ul>"),
        section("测试步骤", "Procedure",
            "<ol>"
            + zh("<li>DUT 发满带宽调制包（80 MHz 带宽发满 234 个数据子载波）。</li>"
                 "<li>仪器解调，测每个子载波功率，画带内功率曲线。</li>"
                 "<li>与平均功率比，检查各子载波起伏是否在标准窗内。</li>")
            + en("<li>DUT transmits full-bandwidth packets (234 data subcarriers at 80 MHz).</li>"
                 "<li>Demodulate and plot per-subcarrier power.</li>"
                 "<li>Check ripple against the standard's window, relative to the mean.</li>")
            + "</ol>"),
        section("判定标准", "Pass criteria",
            "<ul>"
            + zh("<li>802.11 规定：中心 ±16 个子载波内起伏 ≤ +1/−2 dB；边缘子载波 ≤ +2/−4 dB。</li>"
                 "<li>全部子载波都必须落在窗内。</li>")
            + en("<li>IEEE 802.11: within the center ±16 subcarriers, ripple ≤ +1/−2 dB; edge subcarriers ≤ +2/−4 dB.</li>"
                 "<li>Every subcarrier must fall inside the window.</li>")
            + "</ul>"),
        section("超标分析", "If it fails",
            "<ul>"
            + zh("<li>曲线整体倾斜 → 频偏过大或滤波器滚降。</li>"
                 "<li>中间凹陷 → 时钟同步/信道估计问题。</li>"
                 "<li>局部尖峰 → 滤波器/匹配网络谐振。</li>")
            + en("<li>Overall tilt → excessive frequency offset or filter roll-off.</li>"
                 "<li>Mid-band dip → clock sync / channel-estimation issue.</li>"
                 "<li>Local spikes → filter or matching-network resonance.</li>")
            + "</ul>"),
    ],
}

# -------------------------------------------------- 07 RX sensitivity
PAGES["07-rx-sensitivity.html"] = {
    "title": "07 RX minimum input sensitivity — Wi-Fi RF Test Guide",
    "zh_title": "07 接收机最小输入灵敏度",
    "en_title": "07 Receiver minimum input sensitivity",
    "zh_lede": "在规定误包率下能正常解调的最弱信号电平——数值越低（越负）代表“耳朵越灵”、覆盖越好。",
    "en_lede": "The weakest input level the receiver can demodulate at a required PER — the lower (more negative), the better.",
    "sections": [
        section("测试目的", "Purpose",
            "<ul>"
            + zh("<li>直接决定弱信号下的覆盖能力与掉线表现。</li>"
                 "<li>这是 WFA 认证的 RX 核心项，产线常抽测。</li>")
            + en("<li>Determines coverage and disconnect behavior at weak signal.</li>"
                 "<li>Core RX item for WFA certification; often sampled on the production line.</li>")
            + "</ul>"),
        section("测试方向（重要）", "Direction (important)",
            "<p>"
            + zh("与 TX 项方向相反：<b>仪器当发射端，DUT 当接收端</b>。仪器发已知信号，DUT 报收包统计。")
            + en("Opposite direction from TX tests: <b>the instrument transmits, the DUT receives</b> and reports its receive statistics.")
            + "</p>"),
        section("测试步骤", "Procedure",
            "<ol>"
            + zh("<li>建立回环：DUT 收到包后通过测试模式回传收包计数给仪器。</li>"
                 "<li>信号源发<b>标准参考包</b>：固定速率（参考速率：如 11b 1 Mbps、11n MCS0）、固定包长（OFDM 4096 字节 / DSSS 1024 字节）、共 1000 包。</li>"
                 "<li>从较强电平开始，逐步衰减（步进 1 dB）降低 DUT 输入电平。</li>"
                 "<li>每个电平统计误包率（PER），找到 PER 恰好达到 10% 的电平点。</li>"
                 "<li>补偿：该电平 − 线损 = DUT 天线口实际输入电平 = 实测灵敏度。</li>")
            + en("<li>Establish the loop: the DUT reports its received-packet count back via test mode.</li>"
                 "<li>Send the <b>standard reference packet</b>: fixed rate (e.g. 11b 1 Mbps, 11n MCS0), fixed length (4096-byte OFDM / 1024-byte DSSS), 1000 packets.</li>"
                 "<li>Step attenuation (1 dB) to lower the DUT's input level from a strong start.</li>"
                 "<li>Count PER at each level; find the level where PER first reaches 10%.</li>"
                 "<li>Compensate: that level − cable loss = the actual level at the DUT antenna port = measured sensitivity.</li>")
            + "</ol>"),
        section("判定标准", "Pass criteria",
            "<ul>"
            + zh("<li>实测灵敏度 ≤ 标准限值（更好或相等）。例如：11n 20MHz MCS0 限值 −82 dBm；11ac MCS9 80MHz 限值 −72 dBm。</li>"
                 "<li>灵敏度裕量测试：在“限值 +3 dB”的电平下 PER 仍 ≤ 10%。</li>")
            + en("<li>Measured sensitivity ≤ the standard limit (equal or better). E.g. 11n 20 MHz MCS0 limit −82 dBm; 11ac MCS9 80 MHz limit −72 dBm.</li>"
                 "<li>Sensitivity margin test: at limit + 3 dB, PER must still be ≤ 10%.</li>")
            + "</ul>"),
        section("常见坑", "Pitfalls",
            "<ul>"
            + zh("<li>屏蔽箱不干净、线缆屏蔽不良 → 环境信号污染结果，灵敏度虚差。测之前先测噪底。</li>"
                 "<li>DUT 没关省电/没锁速率 → PER 被重传和速率切换污染。</li>")
            + en("<li>Leaky shield box or cables → ambient signals pollute the result; measure the noise floor first.</li>"
                 "<li>DUT not in fixed-rate / power-save disabled → PER polluted by retries and rate switching.</li>")
            + "</ul>"),
    ],
}

# ------------------------------------------------- 08 RX max input
PAGES["08-rx-max-input.html"] = {
    "title": "08 RX maximum input level — Wi-Fi RF Test Guide",
    "zh_title": "08 接收机最大输入电平",
    "en_title": "08 Receiver maximum input level",
    "zh_lede": "在规定误包率下仍能正常接收的最强信号电平——保证近距离强信号下接收机不饱和、不掉线。",
    "en_lede": "The strongest input level still received at the required PER — ensures the front end does not saturate at close range.",
    "sections": [
        section("测试目的", "Purpose",
            "<ul>"
            + zh("<li>信号太强会导致接收机前端（LNA/混频器）饱和、大信号压缩，解调失败——表现为“手机贴着 AP 反而掉线”。</li>"
                 "<li>主要在 DV 阶段验证；产线一般不测（需要反向灌大信号，工装不方便）。</li>")
            + en("<li>Too-strong signals saturate the LNA/mixer and break demodulation — the classic “phone next to the AP disconnects” case.</li>"
                 "<li>Verified at DV stage; production lines usually skip it (reverse high-level injection is awkward).</li>")
            + "</ul>"),
        section("测试步骤", "Procedure",
            "<ol>"
            + zh("<li>信号源发<b>强信号</b>直接灌入 DUT——不需要衰减器，必要时近距离耦合或加放大。</li>"
                 "<li>典型从 0 dBm 开始，发 1000 包统计 PER。</li>"
                 "<li>在标准规定的最大电平区间内（如 −30 dBm 到 0 dBm，具体看代际）逐点验证。</li>")
            + en("<li>Inject a <b>strong</b> signal directly into the DUT — no attenuator; close coupling or extra gain if needed.</li>"
                 "<li>Start at 0 dBm, send 1000 packets, count PER.</li>"
                 "<li>Verify every level in the standard's high-level range (e.g. −30 to 0 dBm, generation-dependent).</li>")
            + "</ol>"),
        section("判定标准", "Pass criteria",
            "<ul>"
            + zh("<li>在规定最大电平（802.11 通常要求到 0 dBm）下 PER ≤ 10%。</li>")
            + en("<li>At the specified maximum level (802.11 typically requires up to 0 dBm), PER ≤ 10%.</li>")
            + "</ul>"),
        section("超标表现", "If it fails",
            "<ul>"
            + zh("<li>接收机前端饱和/压缩 → 解调失败。改不了软件，通常是前端设计余量不足，需硬件评估。</li>")
            + en("<li>Front-end saturation/compression breaks demodulation. Not fixable in software — usually a front-end design margin issue needing hardware review.</li>")
            + "</ul>"),
    ],
}


def build():
    for fname, page in PAGES.items():
        parts = [HEAD.format(**page)]
        parts.extend(page["sections"])
        parts.append(FOOT)
        with open(fname, "w", encoding="utf-8") as f:
            f.write("".join(parts))
        print(f"wrote {fname}")


if __name__ == "__main__":
    build()
