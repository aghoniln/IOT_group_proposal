"""Generate architecture & flowchart diagrams (PNG) for the proposal and PPT."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = ["Microsoft JhengHei", "Microsoft YaHei", "sans-serif"]
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "img")
os.makedirs(OUT, exist_ok=True)

C_USER = "#7C3AED"
C_AGENT = "#0EA5E9"
C_TOOL = "#10B981"
C_DATA = "#F59E0B"
C_OUT = "#EF4444"
C_STEP = "#334155"


def box(ax, x, y, w, h, text, color, fs=11, tc="white", shape="round,pad=0.02,rounding_size=0.12"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=shape,
                                fc=color, ec="none", zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, zorder=3, fontweight="bold")


def arrow(ax, p1, p2, color="#64748B", text=None, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14, lw=1.6,
                                 color=color, zorder=1, connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 0.15, text, ha="center",
                fontsize=9, color=color)


def architecture():
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=200)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.5)
    ax.axis("off")

    box(ax, 1.2, 3.6, 1.9, 1.1, "使用者\nWeb / LINE Bot", C_USER)
    box(ax, 3.9, 3.6, 2.2, 1.5, "LLM Agent\n(ReAct)\n理解・規劃・推理", C_AGENT)

    tools = ["即時空品查詢", "氣象查詢", "PM2.5 24h 預測", "健康知識庫 RAG", "使用者健康檔案"]
    data = ["環境部 API\nCivil IoT 感測器", "中央氣象署 API", "XGBoost / LSTM\n+ SHAP",
            "ChromaDB\nWHO / AQI 指引", "User Profile DB"]
    ys = [5.7, 4.65, 3.6, 2.55, 1.5]
    for t, d, y in zip(tools, data, ys):
        box(ax, 7.0, y, 2.3, 0.75, "Tool: " + t, C_TOOL, fs=10)
        box(ax, 10.4, y, 2.4, 0.8, d, C_DATA, fs=9.5)
        arrow(ax, (5.0, 3.6), (5.85, y))
        arrow(ax, (8.15, y), (9.2, y))

    box(ax, 3.9, 0.7, 3.4, 0.85, "個人化建議 + 風險等級 + 依據來源", C_OUT, fs=10.5)
    arrow(ax, (2.15, 3.6), (2.8, 3.6))
    arrow(ax, (3.9, 2.85), (3.9, 1.13))
    arrow(ax, (2.2, 0.7), (1.2, 3.05), rad=-0.3)

    ax.text(6.5, 6.35, "AI Air Doctor 系統架構", ha="center", fontsize=16, fontweight="bold", color="#0F172A")
    fig.savefig(os.path.join(OUT, "architecture.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def flowchart():
    fig, ax = plt.subplots(figsize=(9, 12), dpi=200)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 12)
    ax.axis("off")
    cx = 4.5
    W, H = 4.4, 0.75

    box(ax, cx, 11.3, 3.0, 0.7, "使用者提問", C_USER, shape="round,pad=0.02,rounding_size=0.35")
    box(ax, cx, 10.2, W, H, "解析意圖:地點 / 時間 / 活動", C_STEP)
    box(ax, cx, 9.1, W, H, "讀取使用者健康檔案", C_STEP)
    box(ax, cx, 7.95, 3.6, 0.9, "查詢時間是現在\n還是未來?", C_AGENT, shape="round,pad=0.02,rounding_size=0.45")
    box(ax, 2.2, 6.6, 3.4, H, "查詢即時空品 + 氣象", C_TOOL)
    box(ax, 6.8, 6.6, 3.4, H, "執行 PM2.5 預測模型", C_TOOL)
    box(ax, cx, 5.3, W, H, "依健康檔案計算個人風險等級", C_STEP)
    box(ax, cx, 4.2, W, H, "RAG 檢索對應健康建議", C_STEP)
    box(ax, cx, 3.1, W, H, "LLM 整合推理,產生回答", C_STEP)
    box(ax, cx, 1.95, 3.6, 0.9, "是否附上來源?", C_AGENT, shape="round,pad=0.02,rounding_size=0.45")
    box(ax, cx, 0.7, 3.2, 0.7, "輸出建議 + 依據", C_OUT, shape="round,pad=0.02,rounding_size=0.35")

    arrow(ax, (cx, 10.95), (cx, 10.6))
    arrow(ax, (cx, 9.82), (cx, 9.48))
    arrow(ax, (cx, 8.72), (cx, 8.42))
    arrow(ax, (2.9, 7.7), (2.2, 6.98), text="現在")
    arrow(ax, (6.1, 7.7), (6.8, 6.98), text="未來")
    arrow(ax, (2.2, 6.22), (3.3, 5.68))
    arrow(ax, (6.8, 6.22), (5.7, 5.68))
    arrow(ax, (cx, 4.92), (cx, 4.58))
    arrow(ax, (cx, 3.82), (cx, 3.48))
    arrow(ax, (cx, 2.72), (cx, 2.42))
    arrow(ax, (cx, 1.48), (cx, 1.07))
    ax.text(cx + 0.15, 1.2, "是", fontsize=9.5, color="#64748B")
    arrow(ax, (6.3, 1.95), (6.7, 4.2), rad=0.4, color="#EF4444")
    ax.text(7.55, 3.0, "否:重新檢索", fontsize=9.5, color="#EF4444")
    fig.savefig(os.path.join(OUT, "flowchart.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    architecture()
    flowchart()
    print("diagrams saved to", os.path.abspath(OUT))
