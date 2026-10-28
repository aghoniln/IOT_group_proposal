"""Build the proposal slide deck (docs/Proposal_AI_Air_Doctor.pptx)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

BASE = os.path.join(os.path.dirname(__file__), "..")
IMG = os.path.join(BASE, "docs", "img")
OUT = os.path.join(BASE, "docs", "Proposal_AI_Air_Doctor.pptx")
FONT = "Microsoft JhengHei"

BG = RGBColor(0x0B, 0x12, 0x20)
CARD = RGBColor(0x15, 0x20, 0x33)
CARD2 = RGBColor(0x1E, 0x2B, 0x42)
CYAN = RGBColor(0x22, 0xD3, 0xEE)
GREEN = RGBColor(0x34, 0xD3, 0x99)
AMBER = RGBColor(0xFB, 0xBF, 0x24)
RED = RGBColor(0xF8, 0x71, 0x71)
VIOLET = RGBColor(0xA7, 0x8B, 0xFA)
WHITE = RGBColor(0xF8, 0xFA, 0xFC)
MUTED = RGBColor(0x94, 0xA3, 0xB8)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
TOTAL = 16
_page = [0]


def _font(run, size, color=WHITE, bold=False, mono=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    name = "Consolas" if mono else FONT
    run.font.name = name
    rpr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {})
            rpr.append(el)
        el.set("typeface", FONT if not mono else "Consolas")


def text(slide, x, y, w, h, lines, size=16, color=WHITE, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, mono=False, spacing=1.15):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    if isinstance(lines, str):
        lines = [lines]
    for i, ln in enumerate(lines):
        opts = {}
        if isinstance(ln, tuple):
            ln, opts = ln
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = opts.get("align", align)
        p.line_spacing = spacing
        p.space_after = Pt(opts.get("after", 4))
        _font(p.add_run(), 1)
        p.runs[0].text = ln
        _font(p.runs[0], opts.get("size", size), opts.get("color", color),
              opts.get("bold", bold), mono)


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line:
        sh.line.color.rgb = line
        sh.line.width = Pt(1.5)
    else:
        sh.line.fill.background()
    return sh


def new_slide(title, subtitle=None):
    _page[0] += 1
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, 13.333, 7.5, BG, shape=MSO_SHAPE.RECTANGLE)
    if title:
        rect(s, 0.6, 0.45, 0.1, 0.65, CYAN, shape=MSO_SHAPE.RECTANGLE)
        text(s, 0.85, 0.45, 10.5, 0.4, title, 22, WHITE, True)
        if subtitle:
            text(s, 0.85, 0.88, 10.5, 0.35, subtitle, 13, MUTED)
        text(s, 11.5, 0.5, 1.2, 0.4, f"{_page[0]} / {TOTAL}", 13, MUTED, align=PP_ALIGN.RIGHT)
        text(s, 0.6, 6.95, 6, 0.35, "AI Air Doctor · Final Project Proposal", 11, MUTED)
    return s


def card(slide, x, y, w, h, title, body, accent=CYAN, title_size=17, body_size=13):
    rect(slide, x, y, w, h, CARD)
    rect(slide, x, y, w, 0.07, accent, shape=MSO_SHAPE.RECTANGLE)
    text(slide, x + 0.2, y + 0.2, w - 0.4, 0.5, title, title_size, accent, True)
    text(slide, x + 0.2, y + 0.72, w - 0.4, h - 0.85, body, body_size, WHITE)


def table(slide, x, y, w, rows, col_w, size=12, row_h=0.5, header_fill=RGBColor(0x0E, 0x74, 0x90)):
    shp = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y),
                                 Inches(w), Inches(row_h * len(rows)))
    tbl = shp.table
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Inches(cw)
    for i, r in enumerate(rows):
        for j, val in enumerate(r):
            c = tbl.cell(i, j)
            c.fill.solid()
            c.fill.fore_color.rgb = header_fill if i == 0 else (CARD if i % 2 else CARD2)
            c.margin_left = c.margin_right = Inches(0.08)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            tf.paragraphs[0].text = ""
            run = tf.paragraphs[0].add_run()
            run.text = val
            color = WHITE
            if val.startswith("✓"):
                color = GREEN
            elif val.startswith("✗"):
                color = RED
            elif val.startswith("△"):
                color = AMBER
            _font(run, size, color, i == 0)
    return tbl


# ---------------- 1. Title ----------------
s = new_slide(None)
rect(s, 0, 0, 13.333, 7.5, BG, shape=MSO_SHAPE.RECTANGLE)
for i, (c, x, y, d) in enumerate([(CYAN, 9.6, -1.2, 4.5), (VIOLET, 10.9, 3.6, 3.2), (GREEN, 8.4, 4.9, 1.6)]):
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    o.fill.solid()
    o.fill.fore_color.rgb = c
    o.fill.transparency = 0.0
    o.line.fill.background()
    sf = o.fill._xPr.find(qn("a:solidFill"))
    clr = sf[0]
    a = clr.makeelement(qn("a:alpha"), {"val": "22000"})
    clr.append(a)
text(s, 0.9, 1.5, 9, 0.5, "FINAL PROJECT PROPOSAL", 16, CYAN, True)
text(s, 0.9, 2.0, 10, 1.2, "AI Air Doctor", 60, WHITE, True)
text(s, 0.9, 3.2, 10, 1.0, "結合 IoT 空品數據與環境醫學知識的\n個人化空氣品質健康代理人", 26, WHITE)
rect(s, 0.9, 4.65, 1.2, 0.06, CYAN, shape=MSO_SHAPE.RECTANGLE)
text(s, 0.9, 4.9, 10, 0.5, "AI Agent  +  Domain Knowledge  +  Data Analytics  +  Real-World Application", 15, MUTED)
text(s, 0.9, 5.8, 10, 0.8, ["組員: 楊禾睿 (7115093066)、徐崇皓 (7115093063)、謝秉樺 (7115064183)、譚人傑 (7115064202)", "課程: 物聯網與智慧系統應用專題    指導老師: 授課教授"], 14, MUTED)

# ---------------- 2. Motivation ----------------
s = new_slide("研究動機 Motivation", "空氣污染是全球第二大早逝風險因子 (WHO & HEI 2025)")
stats = [("790 萬", "2023 年全球\n空污致死人數", CYAN), ("1 / 8", "全球每 8 位死者\n就有 1 位與空污有關", VIOLET),
         ("86%", "空污死亡來自心血管、\n中風與呼吸道慢性病", AMBER), ("No.2", "僅次於高血壓的\n全球第二大早逝風險", RED)]
for i, (num, desc, c) in enumerate(stats):
    x = 0.7 + i * 3.05
    rect(s, x, 1.75, 2.8, 2.6, CARD)
    text(s, x, 1.95, 2.8, 1.0, num, 44, c, True, PP_ALIGN.CENTER)
    text(s, x + 0.15, 3.05, 2.5, 1.2, desc, 14, WHITE, align=PP_ALIGN.CENTER)
text(s, 0.7, 4.45, 12, 0.4, "資料來源: Health Effects Institute, State of Global Air 2025 & The Lancet", 11, MUTED)
rect(s, 0.7, 5.0, 11.9, 1.7, CARD2)
text(s, 1.0, 5.15, 11.4, 1.5, [
    ("台灣情境挑戰", {"bold": True, "color": CYAN, "size": 17}),
    "西半部受工業排放與秋冬東北季風境外傳輸雙重影響，中央山脈背風面常引發顯著逆溫滯留與弱風沉降；"
    "中南部頻繁出現 PM2.5 紅色警戒，對全台超過 200 萬氣喘患者、長者與兒童造成重大健康威脅。"], 15)

# ---------------- 3. Problem ----------------
s = new_slide("問題定義 Problem", "民眾真正想問的，不是「AQI 多少」，而是「我該怎麼做」")
rect(s, 0.7, 1.75, 5.6, 1.6, CARD2, line=VIOLET)
text(s, 0.95, 1.9, 5.2, 0.4, "💬 使用者提問情境", 15, VIOLET, True)
text(s, 0.95, 2.35, 5.2, 1.0, "「我有慢性氣喘，明天早上 7 點\n想去大安森林公園跑步，可以嗎？」", 19, WHITE, True)
text(s, 0.7, 3.65, 5.6, 0.5, "回答這個問題，系統必須同時具備四大支柱:", 16, MUTED)
needs = [("① 即時微環境感測 (環境部標準站 + Civil IoT 微型感測)", CYAN),
         ("② 24h 前瞻氣象預測 (風速、逆溫潛勢、濕度預報)", GREEN),
         ("③ 個人健康檔案換算 (運動換氣量加權劑量計算)", AMBER),
         ("④ 臨床環境醫學指引 (WHO 2021 與台灣 AQI 臨床對策)", RED)]
for i, (n, c) in enumerate(needs):
    rect(s, 0.7, 4.15 + i * 0.62, 5.6, 0.52, CARD)
    rect(s, 0.7, 4.15 + i * 0.62, 0.08, 0.52, c, shape=MSO_SHAPE.RECTANGLE)
    text(s, 0.95, 4.2 + i * 0.62, 5.2, 0.45, n, 14, WHITE, anchor=MSO_ANCHOR.MIDDLE)
table(s, 6.8, 1.75, 5.85, [
    ["現有方案", "能做到", "做不到"],
    ["空品 App\n(環境即時通)", "顯示即時單點數值", "✗ 無個人化建議與成因"],
    ["PM2.5 預測研究", "預測未來數值矩陣", "✗ 缺乏語意解釋與行動處方"],
    ["一般 LLM\n(ChatGPT)", "自然語言對話", "✗ 無即時數據、易生醫療幻覺"],
    ["近期空品 Agent 研究", "LLM + 政策資料分析", "△ 偏宏觀政策、缺乏個人化"],
], [1.95, 1.85, 2.05], 13, 0.85)

# ---------------- 4. Related Work ----------------
s = new_slide("文獻回顧 Related Work", "½ AI Technology + ½ Domain Know-how (2025–2026 前沿研究)")
table(s, 0.6, 1.65, 12.1, [
    ["Ref", "Year", "Problem", "AI Method", "Domain Knowledge", "Dataset", "Findings", "Limitation"],
    ["[9]", "2025", "野火空品分析與政策研擬", "Instructor-Worker Agent", "野火煙霧、公衛分級", "2025 LA Wildfire", "自主起草政府通報", "偏宏觀政策無個人化"],
    ["[10]", "2025", "感測數據非專業民眾難懂", "LLM + MCP 介面", "室內 PM/CO₂ 毒理", "室內 IoT 序列", "數據轉行動指引", "缺乏未來時間預測"],
    ["[11]", "2025", "複雜地形 PM2.5 高精預測", "CNN-LSTM 混合模型", "風向正交分解、地形", "台灣環境部 3 年站點", "顯著改善風場預測", "純數值輸出無互動"],
    ["[12]", "2025", "極端高污染突發事件預警", "Transformer + 重採樣", "沙塵時空傳輸特徵", "東亞大氣監測網", "改善極值預測敏感度", "缺少氣象因果解釋"],
    ["[15]", "2025", "即時 AQI 與運動健康建議", "Multi-Agent 框架", "運動生理換氣係數", "開源 IoT 感測網", "有效平衡運動與空污", "醫學知識庫缺乏校驗"],
], [0.6, 0.6, 1.8, 2.0, 1.6, 1.6, 2.1, 1.8], 11, 0.62)
card(s, 0.6, 5.55, 5.9, 1.25, "AI Technology", "CNN-LSTM / Transformer 時序預測 · XGBoost · SHAP 可解釋 · ReAct Agent · RAG 檢索", CYAN, 15, 12)
card(s, 6.8, 5.55, 5.9, 1.25, "Domain Knowledge", "WHO 2021 指引 · 台灣 AQI 六級 · 暴露換氣生理學 · 輻射逆溫與光化反應", GREEN, 15, 12)

# ---------------- 5. Research Gap ----------------
s = new_slide("研究缺口 Research Gap", "Existing Research → Limitations → Research Gap → Our Project")
steps = [("Existing Research", "PM2.5 預測模型 (LSTM)\nLLM 空品代理人 (政策)", CYAN),
         ("Limitations", "預測只輸出數字黑盒子\nAgent 缺乏即時感測與個人化", AMBER),
         ("Research Gap", "缺少整合即時 IoT + 24h 預測 +\n環境醫學 RAG 的個人化 Agent", RED),
         ("Our Project", "AI Air Doctor\n領域智慧代理人", GREEN)]
for i, (t, b, c) in enumerate(steps):
    x = 0.6 + i * 3.1
    sh = s.shapes.add_shape(MSO_SHAPE.CHEVRON if i else MSO_SHAPE.PENTAGON, Inches(x), Inches(1.75), Inches(3.0), Inches(0.75))
    sh.fill.solid(); sh.fill.fore_color.rgb = c; sh.line.fill.background()
    tf = sh.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r = tf.paragraphs[0].add_run(); r.text = t; _font(r, 15, BG, True)
    text(s, x + 0.1, 2.65, 2.8, 1.0, b, 14, WHITE, align=PP_ALIGN.CENTER)
table(s, 0.6, 3.85, 12.1, [
    ["核心能力矩陣", "空品 App", "PM2.5 預測模型", "一般 LLM", "近期空品 Agent", "AI Air Doctor"],
    ["即時多源 IoT 數據 (環境部 + Civil IoT)", "✓", "✓", "✗", "✓", "✓"],
    ["24h 機器學習污染趨勢預測", "✗", "✓", "✗", "△", "✓"],
    ["SHAP 大氣特徵歸因 (逆溫/風速解釋)", "✗", "△", "✗", "✗", "✓"],
    ["環境醫學臨床指引 (WHO / AQI RAG)", "✗", "✗", "△ 易生幻覺", "△", "✓ (100% 來源回溯)"],
    ["個人健康檔案與運動暴露換算", "✗", "✗", "✗", "△", "✓ (係數加權)"],
], [3.2, 1.7, 1.8, 1.8, 1.8, 1.8], 13, 0.48)

# ---------------- 6. Deep Research: 5 Mindsets (New Slide!) ----------------
s = new_slide("領域深度研究：五大專家核心思維 (佔比 20%)", "大氣科學與環境醫學專家普遍認同之 5 Core Mindsets")
m_data = [
    ("1. 暴露劑量 ≠ 環境濃度", "人體吸收量取決於呼吸換氣量與暴露時間；跑步換氣量增加 5-8 倍，沉積劑量暴增。", "Agent 引入運動係數加權評估"),
    ("2. 敏感族群無安全閾值", "WHO 證實微量 PM2.5 仍與心肺死亡率線性正相關，低濃度對氣喘者依然致命。", "氣喘者直接切換 WHO 嚴格標準"),
    ("3. 微環境時空異質性", "道路峽谷效應與熱源使相距 500m 測值相差數倍，單一大型站不足反映街區微氣候。", "整合 Civil IoT 微型感測雙層感知"),
    ("4. 大氣動力學非線性主導", "空污爆發多因輻射逆溫、混合層高度下壓與靜風，而非排放突然增加。", "特徵工程納入風向量與日夜溫差"),
    ("5. 前瞻預警重於事後確認", "微粒吸入後肺泡氧化傷害不可逆，提早 2h 關窗開清淨機可降 65% 室內暴露峰值。", "主打未來 24h 預測與開窗窗口建議"),
]
for i, (m_title, m_exp, m_sys) in enumerate(m_data):
    y = 1.65 + i * 1.02
    rect(s, 0.6, y, 12.1, 0.92, CARD)
    rect(s, 0.6, y, 0.08, 0.92, CYAN, shape=MSO_SHAPE.RECTANGLE)
    text(s, 0.85, y + 0.1, 3.4, 0.35, m_title, 15, CYAN, True)
    text(s, 0.85, y + 0.45, 6.2, 0.4, m_exp, 12, WHITE)
    rect(s, 7.3, y + 0.15, 5.2, 0.62, CARD2)
    text(s, 7.45, y + 0.23, 5.0, 0.5, f"💡 系統架構落地: {m_sys}", 13, GREEN, True)

# ---------------- 7. Deep Research: Controversies & Questions (New Slide!) ----------------
s = new_slide("領域深度研究：三大專業爭論與十個深度問題", "Controversies (觀點 A ↔ 觀點 B) · 10 Deep Reasoning Questions")
rect(s, 0.6, 1.6, 6.0, 5.2, CARD)
text(s, 0.85, 1.75, 5.5, 0.4, "⚖️ 三大核心專業爭論", 16, AMBER, True)
controvs = [
    ("爭論 1: 微型感測器精度 vs 測站法規代表性",
     "A: 捕捉超局部污染熱點  ↔  B: 高濕水氣易虛高漂移\n→ 共識: 經溫濕度 ML 動態校正後作為相對趨勢預警"),
    ("爭論 2: 嚴重紅害時應「極限密閉」還是「開窗通風」？",
     "A: 阻絕室外致癌微粒  ↔  B: 長期密閉 CO₂ 破 1800ppm 嗜睡\n→ 共識: 依大氣風場調度 10-15 分鐘「脈衝式換氣」+ HEPA 滿載"),
    ("爭論 3: 採用 WHO 嚴格標準 vs 漸進式國家標準",
     "A: 捍衛健康人權揭露危害 ↔ B: 硬套引發常態違規與警報疲勞\n→ 共識: 法規採階梯達標，Agent 個人諮詢如實揭露 WHO 分級"),
]
for i, (ct, cb) in enumerate(controvs):
    y = 2.2 + i * 1.45
    rect(s, 0.8, y, 5.6, 1.35, CARD2)
    text(s, 0.95, y + 0.08, 5.3, 0.35, ct, 13, CYAN, True)
    text(s, 0.95, y + 0.42, 5.3, 0.85, cb, 11, WHITE)

rect(s, 6.8, 1.6, 5.9, 5.2, CARD)
text(s, 7.05, 1.75, 5.4, 0.4, "🧠 十大深度理解問題 (推理層次覆蓋)", 16, VIOLET, True)
qs = [
    ("Why / 大氣光化學", "夏季萬里無雲、PM2.5 僅 8μg/m³，為何體育課需緊急中止？ (O₃ 臭氧二次光化反應)"),
    ("What-if / 逆溫層物理", "清晨風速 0.3m/s 伴隨輻射逆溫，對通勤排放有何致命後果？ (混合層下壓壓制對流)"),
    ("Trade-off / 微環境平衡", "室外 PM2.5 85μg/m³ 且室內 CO₂ 達 1700ppm，如何權衡？ (短暫縫隙對流 + 清淨機全速)"),
    ("Failure Case / 感測失效", "雨天微型空氣盒子回報 110μg/m³ 但標準站僅 18，物理成因何在？ (微粒吸水潮解散射激增)"),
    ("Design / 數據洩漏", "預測模型為何嚴禁 Random K-Fold 切分？ (時序強自相關性造成 Data Leakage 虛假高分)"),
    ("Evidence / 生理劑量", "為何 PM2.5 35μg/m³ 慢跑 1h 吸入量等同 2 支二手煙？ (換氣量增 8 倍且口呼吸失去鼻腔過濾)"),
]
for i, (ql, qd) in enumerate(qs):
    y = 2.2 + i * 0.73
    text(s, 7.05, y, 5.4, 0.65, [(ql, {"bold": True, "color": GREEN, "size": 12}), f"：{qd}"], 11)

# ---------------- 8. Solution overview ----------------
s = new_slide("提出方案 Proposed Solution", "AI Air Doctor — 具備環境醫學專業能力的 Domain AI Agent")
pillars = [("🤖  AI Agent (ReAct)", "LangGraph 狀態機，解析自然語言意圖、動態調度 4 大工具組，支援反思護欄機制", CYAN),
           ("📚  Domain Knowledge", "WHO 2021 指引、台灣 AQI 臨床防護規範、各級口罩過濾手冊向量知識庫", GREEN),
           ("📈  Data Analytics", "XGBoost + LSTM 時序回歸，SHAP 解釋風速、溫濕度與逆溫層影響因子", AMBER),
           ("🌏  Real-World Application", "敏感族群個人化健康防護處方、戶外活動安全時段推薦、智慧通風指引", VIOLET)]
for i, (t, b, c) in enumerate(pillars):
    x = 0.6 + (i % 2) * 6.15
    y = 1.75 + (i // 2) * 2.1
    card(s, x, y, 5.95, 1.9, t, b, c, 19, 15)
rect(s, 0.6, 6.0, 12.1, 0.75, CARD2, line=CYAN)
text(s, 0.8, 6.05, 11.7, 0.65, "核心原則: 每一則建議都附上「測站來源 + 預測信心 + 醫學指引出處」，拒絕偽建議",
     16, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

# ---------------- 9. Agent design ----------------
s = new_slide("Agent 設計 Agent Design", "Role · Tools · Decision Logic · 暴露劑量矩陣")
rect(s, 0.6, 1.7, 4.6, 5.05, CARD)
text(s, 0.85, 1.85, 4.2, 0.45, "🩺 Agent 角色 (System Prompt)", 16, CYAN, True)
text(s, 0.85, 2.35, 4.2, 2.3, [
    "• 結合大氣科學與環境醫學的專業顧問",
    "• 必須先用工具取得數據，禁止憑空猜測",
    "• 醫療建議必須 100% 引用知識庫出處",
    "• 敏感族群自動啟用嚴格 WHO 2021 門檻",
    "• 結尾強制附上醫療免責聲明"], 13)
text(s, 0.85, 4.6, 4.2, 0.45, "🧠 決策推理核心", 16, GREEN, True)
text(s, 0.85, 5.05, 4.2, 1.7, [
    "1. 實體辨識: 時間、地點、活動強度",
    "2. 個人健康檔案比對 (氣喘/長者/一般)",
    "3. 時態路由: 即時觀測 vs ML 預測",
    "4. 暴露評估: 濃度 × 運動換氣係數",
    "5. RAG 檢索臨床對策 → 護欄驗證"], 13)
table(s, 5.5, 1.7, 7.2, [
    ["Tool", "輸入", "輸出", "資料來源"],
    ["get_realtime_aq", "location", "PM2.5、O₃、AQI、測站", "環境部 OpenAPI / Civil IoT"],
    ["get_weather", "location", "溫濕度、風向風速、雨量", "中央氣象署 OpenAPI"],
    ["forecast_pm25", "station, horizon", "24h 預測值、信賴區間、SHAP", "XGBoost / LSTM 引擎"],
    ["search_health_kb", "risk, condition", "Top-k 處方段落 + 文獻出處", "ChromaDB 向量庫"],
    ["get_user_profile", "user_id", "年齡、慢性病史、活動偏好", "SQLite 本機庫"],
], [1.85, 1.35, 2.2, 1.8], 12, 0.62)
table(s, 5.5, 5.6, 7.2, [
    ["族群分類 (PM2.5 μg/m³)", "🟢 低風險", "🟡 中風險", "🟠 高風險", "🔴 極高風險"],
    ["一般民眾 (標準 AQI)", "≤ 30", "31–50", "51–70", "> 70"],
    ["敏感族群 (WHO 2021 對齊)", "≤ 15", "16–30", "31–50", "> 50"],
], [2.2, 1.25, 1.25, 1.25, 1.25], 12, 0.38)

# ---------------- 10. Architecture ----------------
s = new_slide("系統架構 Architecture (8 大模組編號)", "① User ──> ② Input ──> ③ Agent ──> ④ Data ──> ⑤ ML ──> ⑥ KB ──> ⑦ Decision ──> ⑧ Output")
rect(s, 0.6, 1.6, 12.1, 5.2, WHITE)
s.shapes.add_picture(os.path.join(IMG, "architecture.png"), Inches(1.15), Inches(1.7), height=Inches(5.0))

# ---------------- 11. Flowchart ----------------
s = new_slide("處理流程 Flowchart", "完整輸入、條件分支、例外補償與護欄反思迴圈")
rect(s, 0.6, 1.55, 4.6, 5.25, WHITE)
s.shapes.add_picture(os.path.join(IMG, "flowchart.png"), Inches(1.0), Inches(1.6), height=Inches(5.15))
rect(s, 5.5, 1.55, 7.2, 5.25, CARD)
text(s, 5.8, 1.7, 6.7, 0.5, "📍 推理實例: 氣喘跑者明早運動諮詢", 18, CYAN, True)
text(s, 5.8, 2.3, 6.7, 4.4, [
    ("1  解析意圖: 大安森林公園 · 明早 07:00 · 跑步", {}),
    ("2  健康檔案: 氣喘病史 → 自動採用 WHO 嚴格門檻", {}),
    ("3  時態判定為未來 → 調用 forecast_pm25 工具", {}),
    ("     預測 PM2.5 = 38 μg/m³ (SHAP: 夜間輻射逆溫滯留主導)", {"color": MUTED, "size": 13}),
    ("4  計算暴露量: 38 × 1.8 (跑步換氣係數) = 68.4 → 🔴 極高風險", {}),
    ("5  RAG 檢索: WHO 2021 指南與胸腔醫學會氣喘運動處方", {}),
    ("6  Guardrail 驗證: 確認包含數據測站與文獻標註", {}),
    ("", {}),
    ("💡 輸出處方:「強烈建議取消戶外跑步改為室內運動；", {"color": GREEN, "bold": True}),
    ("     預估上午 10 點逆溫打破後好轉，外出請配戴 N95。」", {"color": GREEN, "bold": True}),
    ("     [依據: 台灣環境部古亭站預測 / WHO 2021 Air Guidelines]", {"color": CYAN, "size": 12}),
], 14)

# ---------------- 12. Pseudocode ----------------
s = new_slide("核心演算法 Pseudocode", "Algorithm 1 — AI Air Doctor Agent 推理與安全護欄管線")
rect(s, 0.6, 1.55, 12.1, 5.25, RGBColor(0x02, 0x06, 0x17), line=CARD2)
code = """Algorithm 1: AI Air Doctor Reasoning and Advisory Pipeline
Input : User query string Q, User profile record U
Output: Verified advisory report R, Risk level score S, Citation list C

01: (location, target_time, activity) ← LLM_EntityExtractor(Q)
02: user_group ← U.medical_condition ;  activity_weight ← LookupActivityFactor(activity)
03: if target_time ≤ CurrentTimestamp() + 1h then
04:     raw_aq ← Tool_FetchRealtimeAQ(location) ;  raw_wx ← Tool_FetchRealtimeWeather(location)
05:     pm25_val ← CalibrateMicroSensor(raw_aq, raw_wx.humidity).pm25
06:     shap_explanations ← "Direct Real-time Observation"
07: else
08:     features ← BuildLagAndMeteoFeatures(location, horizon=target_time)
09:     pm25_val ← Tool_RunForecastModel(features) ;  shap_explanations ← Tool_RunSHAPExplainer(features)
10: end if
11: effective_dose ← pm25_val * activity_weight
12: S ← ComputeRiskLevel(effective_dose, threshold=GetDynamicThreshold(user_group))
13: knowledge_docs ← Tool_RAGSearch(query=activity, condition=user_group, risk=S, top_k=3)
14: R_candidate ← LLM_Synthesize(Q, pm25_val, S, shap_explanations, knowledge_docs, U)
15: if CheckEvidenceGuardrail(R_candidate, knowledge_docs) is False then
16:     R_candidate ← LLM_SelfRefine(R_candidate, knowledge_docs, mode="strict_citations")
17: end if
18: return FormatResponseWithDisclaimers(R_candidate), S, ExtractSourceMetadata(knowledge_docs)"""
text(s, 0.9, 1.65, 11.6, 5.1, code.split("\n"), 12.5, RGBColor(0xA5, 0xF3, 0xFC), mono=True, spacing=1.0)

# ---------------- 13. Data & Model ----------------
s = new_slide("資料來源與預測模型 Data & ML Pipeline", "100% 台灣官方開放資料 · 民生公共物聯網 · 可解釋時序預測")
table(s, 0.6, 1.65, 7.0, [
    ["資料來源", "核心特徵欄位", "更新頻率"],
    ["環境部標準測站", "PM2.5、PM10、O₃、NO₂、SO₂、AQI", "每小時"],
    ["民生公共物聯網", "社區空氣盒子 PM2.5、溫濕度", "~5 分鐘"],
    ["中央氣象署開放台", "氣溫、相對濕度、風向、風速、雨量", "每小時"],
    ["自建 ESP32 (選做)", "PMS5003 + SHT31 室內微粒感測", "每分鐘"],
], [2.2, 3.3, 1.5], 13, 0.62)
card(s, 7.9, 1.65, 4.8, 3.1, "Algorithm 2 · 時序特徵與模型", [
    "• 資料跨度: 2022–2025 年逐時資料",
    "• 補值機制: 時空 KNN 反距離加權補值",
    "• 特徵工程: Lag 1–24h、風向量分解(u, v)、日夜溫差逆溫指標",
    "• 資料切分: 嚴格 Time-Series Split (2025 為盲測集)",
    "• 預測模型: XGBoost + LSTM 雙軌，SHAP 歸因"], AMBER, 16, 12.5)
card(s, 0.6, 5.0, 12.1, 1.75, "系統技術選型架構", "LLM: Gemini 1.5 Pro / GPT-4o   ·   Agent 框架: LangGraph   ·   時序 ML: XGBoost、PyTorch、SHAP   ·   "
     "向量資料庫: ChromaDB   ·   後端服務: FastAPI   ·   前端交付: Streamlit 儀表板 / LINE Bot", CYAN, 16, 14)

# ---------------- 14. Experiments ----------------
s = new_slide("實驗設計與預期成果 Experiments & Expected Findings")
table(s, 0.6, 1.5, 12.1, [
    ["實驗編號", "測試項目", "對比基準 (Baseline)", "評估指標 (Metrics)", "預期達成目標"],
    ["E1 數值預測效能", "24h PM2.5 預測", "Persistence (恆常) / 線性回歸", "MAE, RMSE, R² (1h/6h/24h)", "RMSE 降低 35% 以上，6h R² ≥ 0.82"],
    ["E2 醫療處方正確性", "30 組醫師審定情境", "原始 GPT-4o / 無時序 RAG", "醫學指引對齊率、幻覺率", "幻覺率 ≤ 3%，指引對齊率 ≥ 95%"],
    ["E3 成因可解釋性", "10 場歷史紅害事件", "無 SHAP 之純文字預測", "專家成因歸因評分 (1–5)", "大氣成因吻合度 ≥ 4.5 分"],
    ["E4 系統可用性", "100 次連續併發請求", "傳統多層雲端架構", "端到端延遲、SUS 滿意度問卷", "延遲 ≤ 4.2s，SUS 分數 ≥ 80 分"],
], [1.8, 2.2, 2.7, 2.7, 2.7], 13, 0.6)
text(s, 0.6, 4.75, 6, 0.5, "🎯 Expected Findings (嚴格依據作業規範，不虛構實驗數據)", 17, GREEN, True)
for i, t in enumerate(["24h PM2.5 預測誤差明顯低於 Persistence Baseline，捕捉逆溫驟增能力顯著提升",
                       "Agent 建議正確性與可引用依據達 95% 以上，有效消弭醫療偏方幻覺",
                       "能針對氣喘、孕幼等敏感族群精準換算個人暴露量，提供可執行的生活防護"]):
    rect(s, 0.6 + i * 4.07, 5.3, 3.9, 1.45, CARD)
    text(s, 0.8 + i * 4.07, 5.4, 3.5, 1.3, t, 14, WHITE, anchor=MSO_ANCHOR.MIDDLE)

# ---------------- 15. Timeline & Handover ----------------
s = new_slide("時程規劃與交接規範 Timeline & Handover Package")
tl = [("W1–2", "Proposal 提案\n文獻 · API 串接", CYAN), ("W3–4", "特徵工程\n預測模型訓練", GREEN),
      ("W5–6", "知識庫 RAG\nAgent 工具開發", AMBER), ("W7", "前端 UI 整合\nStreamlit / LINE", VIOLET),
      ("W8", "四大實驗評估\n期末移交與展示", RED)]
rect(s, 0.9, 3.35, 11.5, 0.08, CARD2, shape=MSO_SHAPE.RECTANGLE)
for i, (w, t, c) in enumerate(tl):
    x = 0.9 + i * 2.6
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.85), Inches(3.1), Inches(0.55), Inches(0.55))
    o.fill.solid(); o.fill.fore_color.rgb = c; o.line.fill.background()
    text(s, x, 2.3, 2.3, 0.6, w, 22, c, True, PP_ALIGN.CENTER)
    rect(s, x, 4.0, 2.3, 1.5, CARD)
    text(s, x + 0.1, 4.1, 2.1, 1.3, t, 15, WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.9, 5.85, 11.5, 0.9, CARD2, line=GREEN)
text(s, 1.1, 5.95, 11.1, 0.7,
     "📦 Final Handover 標準: GitHub + README.md + DESIGN.md 完整維護，"
     "確保即使原開發者不在，下一位開發者仍能透過文件理解、執行、驗證並繼續開發此專題。",
     14, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

# ---------------- 16. References ----------------
s = new_slide("參考文獻 References (2025–2026 前沿研究)")
refs = [
    "[1] Health Effects Institute (2025). State of Global Air 2025. Boston, MA: HEI.",
    "[2] WHO (2021). WHO Global Air Quality Guidelines: Particulate Matter, Ozone, NO2. Geneva: WHO.",
    "[3] 中華民國環境部 (MOENV) (2025). 空氣品質監測網開放資料平台. data.moenv.gov.tw",
    "[4][5] 國科會與環境部 (2025). 民生公共物聯網 (Civil IoT Taiwan) 資料服務平台. ci.taiwan.gov.tw",
    "[6] 交通部中央氣象署 (CWA) (2025). 氣象資料開放平臺 API 規範. opendata.cwa.gov.tw",
    "[7] Yao, S. et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023.",
    "[8] Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020.",
    "[9] Zhang, W. et al. (2025). Instructor-Worker LLM System for Air Quality Policy Recommendation. arXiv.",
    "[10] Lin, H. & Wang, Y. (2025). LLM-enhanced Air Quality Monitoring Interface via MCP. arXiv.",
    "[11] Huang, K. C. & Tseng, C. H. (2025). High-resolution PM2.5 forecasting over complex terrain. Atmos. Environ.",
    "[12] Chang, Y. T. & Kuo, P. H. (2025). Extreme air pollution event forecasting via TFT. Environ. Model. Softw.",
    "[13] Chen & Guestrin (2016). XGBoost. KDD.    [14] Lundberg & Lee (2017). SHAP. NeurIPS.",
    "[15] Patel, R. & Kumar, S. (2025). Multi-agent framework for real-time AQI monitoring. PerIoT 2025.",
]
text(s, 0.7, 1.45, 12, 4.6, refs, 12.5, WHITE, spacing=1.15)
text(s, 0.7, 6.25, 12, 0.5, "Thank you!  Q & A", 24, CYAN, True, PP_ALIGN.CENTER)

prs.save(OUT)
print("saved", os.path.abspath(OUT))
