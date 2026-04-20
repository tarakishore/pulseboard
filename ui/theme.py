"""
PulseBoard Design Tokens & Theme
Centralized color palette, gradients, and design constants.
"""

class Colors:
    BG_PRIMARY = "#0a0e1a"
    BG_SECONDARY = "#131a2e"
    BG_ELEVATED = "#1c2541"
    BG_SURFACE = "#1e293b"
    BG_CARD = "rgba(19, 26, 46, 0.75)"
    BG_CARD_HOVER = "rgba(28, 37, 65, 0.85)"
    INDIGO_400 = "#818cf8"
    INDIGO_500 = "#6366f1"
    INDIGO_600 = "#4f46e5"
    VIOLET_500 = "#8b5cf6"
    VIOLET_600 = "#7c3aed"
    SUCCESS = "#10b981"
    SUCCESS_LIGHT = "#34d399"
    WARNING = "#f59e0b"
    WARNING_LIGHT = "#fbbf24"
    DANGER = "#f43f5e"
    DANGER_LIGHT = "#fb7185"
    INFO = "#38bdf8"
    TEXT_PRIMARY = "#e2e8f0"
    TEXT_SECONDARY = "#94a3b8"
    TEXT_MUTED = "#64748b"
    TEXT_BRIGHT = "#f8fafc"
    BORDER_SUBTLE = "rgba(99, 102, 241, 0.15)"
    BORDER_DEFAULT = "rgba(99, 102, 241, 0.25)"

class Gradients:
    PRIMARY = "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)"
    PRIMARY_SOFT = "linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.15) 100%)"
    SUCCESS = "linear-gradient(135deg, #10b981 0%, #14b8a6 100%)"
    SUCCESS_SOFT = "linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(20,184,166,0.15) 100%)"
    DANGER = "linear-gradient(135deg, #f43f5e 0%, #f97316 100%)"
    DANGER_SOFT = "linear-gradient(135deg, rgba(244,63,94,0.15) 0%, rgba(249,115,22,0.15) 100%)"
    WARNING_SOFT = "linear-gradient(135deg, rgba(245,158,11,0.15) 0%, rgba(251,191,36,0.15) 100%)"
    HERO = "linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%)"

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", color=Colors.TEXT_PRIMARY, size=13),
    title_font=dict(size=18, color=Colors.TEXT_BRIGHT),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", font=dict(color=Colors.TEXT_SECONDARY, size=12)),
    xaxis=dict(gridcolor="rgba(99,102,241,0.08)", zerolinecolor="rgba(99,102,241,0.12)", tickfont=dict(color=Colors.TEXT_SECONDARY)),
    yaxis=dict(gridcolor="rgba(99,102,241,0.08)", zerolinecolor="rgba(99,102,241,0.12)", tickfont=dict(color=Colors.TEXT_SECONDARY)),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(bgcolor=Colors.BG_ELEVATED, bordercolor=Colors.BORDER_DEFAULT, font=dict(color=Colors.TEXT_PRIMARY, size=13)),
)

PLOTLY_COLORS = [Colors.INDIGO_500, Colors.SUCCESS, Colors.VIOLET_500, Colors.WARNING, Colors.INFO, Colors.DANGER]

def confidence_color(score: float) -> str:
    if score >= 80: return Colors.SUCCESS
    elif score >= 60: return Colors.WARNING
    else: return Colors.DANGER

def delta_color(value: float) -> str:
    if value > 0: return Colors.SUCCESS
    elif value < 0: return Colors.DANGER
    return Colors.TEXT_SECONDARY
