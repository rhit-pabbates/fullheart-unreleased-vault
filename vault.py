"""
FULLHEART_VAULT.EXE — Compact Unreleased Music Player
Single-file Streamlit application.
Aesthetic: compact FullHeart red/maroon arcade audio player.
"""

import random
from datetime import datetime
from pathlib import Path
import html
import base64

import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────
# CONFIG & PATHS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FULLHEART_VAULT.EXE",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={"About": "FULLHEART_VAULT.EXE — unreleased music stash"},
)

TRACK_DIR = Path("tracks")
DATA_FILE = Path("data/tracks.csv")
COVER_DIR = Path("covers")
COVER_DIR.mkdir(exist_ok=True)
TRACK_DIR.mkdir(exist_ok=True)
DATA_FILE.parent.mkdir(exist_ok=True)

SYSTEM_MESSAGES = [
    "AUDIO_KERNEL.sys // PLAYBACK READY",
    "TRACK_ARCHIVE.dll // INDEXED",
    "UPLOAD_MODE // ACTIVE",
    "UNRELEASED MATERIAL // HANDLE WITH CARE",
    "VAULT SESSION // AUTHENTICATED",
    "NOW SCANNING // ARCHIVED WAVEFORMS",
    "LOCAL STORAGE // ONLINE",
    "TIMESTAMP // " + datetime.now().strftime("%Y.%m.%d // %H:%M:%S"),
    "HEART_RATE // ELEVATED",
    "FULLHEART_SIGNAL // LOCKED",
]

# ─────────────────────────────────────────────
# CSS — ENHANCED FULLHEART PLAYER THEME
# ─────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=VT323&family=Orbitron:wght@400;700;900&family=Press+Start+2P&display=swap');

        :root {
            --black:      #030102;
            --panel:      #0d0406;
            --panel-2:    #140509;
            --maroon:     #3b0d14;
            --wine:       #5a0f1f;
            --blood:      #7a1022;
            --crimson:    #8b0000;
            --red:        #ff355e;
            --red-soft:   #c4455c;
            --red-pale:   #ffd6e0;
            --silver:     #c8b8bc;
            --muted:      #7d4b55;
            --line:       #3a1018;
            --glow-r:     0 0 8px #ff355e, 0 0 22px rgba(255,53,94,.35);
            --font-mono:  'Share Tech Mono', monospace;
            --font-vt:    'VT323', monospace;
            --font-orb:   'Orbitron', sans-serif;
            --font-px:    'Press Start 2P', monospace;
        }

        /* ── BASE ── */
        html, body, [data-testid="stAppViewContainer"] {
            background: var(--black) !important;
            color: var(--silver) !important;
            font-family: var(--font-mono) !important;
            cursor: crosshair;
        }

        /* ── ANIMATED BACKGROUND GRID + RADIAL VIGNETTE ── */
        [data-testid="stAppViewContainer"]::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            background:
                /* vertical lines */
                repeating-linear-gradient(
                    90deg,
                    rgba(255, 53, 94, 0.055) 0px,
                    rgba(255, 53, 94, 0.055) 1px,
                    transparent 1px,
                    transparent 36px
                ),
                /* horizontal lines */
                repeating-linear-gradient(
                    0deg,
                    rgba(255, 53, 94, 0.03) 0px,
                    rgba(255, 53, 94, 0.03) 1px,
                    transparent 1px,
                    transparent 36px
                ),
                /* deep vignette */
                radial-gradient(ellipse at 50% 50%, transparent 30%, rgba(0,0,0,0.82) 100%),
                /* corner bleed */
                radial-gradient(ellipse at 8% 15%, rgba(255,53,94,0.14) 0%, transparent 35%),
                radial-gradient(ellipse at 92% 80%, rgba(122,16,34,0.22) 0%, transparent 32%),
                #030102;
            animation: gridDrift 28s linear infinite;
        }

        @keyframes gridDrift {
            from { background-position: 0 0, 0 0, center, 0 0, 0 0; }
            to   { background-position: 72px 72px, 72px 72px, center, 0 0, 0 0; }
        }

        /* ── CRT SCANLINES ── */
        [data-testid="stAppViewContainer"]::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 2;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 3px,
                rgba(0, 0, 0, 0.18) 3px,
                rgba(0, 0, 0, 0.18) 4px
            );
            animation: scanMove 8s linear infinite;
        }

        @keyframes scanMove {
            from { background-position: 0 0; }
            to   { background-position: 0 80px; }
        }

        /* ── FLOATING HEARTS LAYER ── */
        .hearts-bg {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 1;
            overflow: hidden;
        }

        .heart-particle {
            position: absolute;
            color: var(--red);
            font-size: 14px;
            opacity: 0;
            animation: floatHeart linear infinite;
            text-shadow: 0 0 8px rgba(255,53,94,0.6);
        }

        .heart-particle:nth-child(1)  { left:  4%; font-size:10px; animation-duration:14s; animation-delay:0s;    opacity:0; }
        .heart-particle:nth-child(2)  { left: 12%; font-size:16px; animation-duration:18s; animation-delay:2s;    opacity:0; }
        .heart-particle:nth-child(3)  { left: 21%; font-size: 8px; animation-duration:12s; animation-delay:5s;    opacity:0; }
        .heart-particle:nth-child(4)  { left: 33%; font-size:12px; animation-duration:20s; animation-delay:1s;    opacity:0; }
        .heart-particle:nth-child(5)  { left: 44%; font-size:18px; animation-duration:15s; animation-delay:7s;    opacity:0; }
        .heart-particle:nth-child(6)  { left: 55%; font-size: 9px; animation-duration:22s; animation-delay:3s;    opacity:0; }
        .heart-particle:nth-child(7)  { left: 67%; font-size:14px; animation-duration:16s; animation-delay:9s;    opacity:0; }
        .heart-particle:nth-child(8)  { left: 78%; font-size:11px; animation-duration:19s; animation-delay:4s;    opacity:0; }
        .heart-particle:nth-child(9)  { left: 87%; font-size:20px; animation-duration:13s; animation-delay:6s;    opacity:0; }
        .heart-particle:nth-child(10) { left: 95%; font-size: 7px; animation-duration:24s; animation-delay:11s;   opacity:0; }

        @keyframes floatHeart {
            0%   { transform: translateY(110vh) scale(0.8) rotate(-8deg); opacity: 0; }
            8%   { opacity: 0.18; }
            50%  { opacity: 0.12; transform: translateY(50vh) scale(1.1) rotate(6deg); }
            92%  { opacity: 0.1; }
            100% { transform: translateY(-10vh) scale(0.9) rotate(-4deg); opacity: 0; }
        }

        /* ── LAYOUT ── */
        .block-container {
            max-width: 800px !important;
            padding: 1.5rem 1.25rem 4rem !important;
            position: relative;
            z-index: 5;
        }

        [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
        #MainMenu, footer, header, [data-testid="stToolbar"], .stDeployButton {
            visibility: hidden !important;
            display: none !important;
        }

        /* ── PLAYER SHELL ── */
        .player-shell {
            border: 1px solid var(--maroon);
            border-top: 2px solid var(--blood);
            box-shadow:
                0 0 0 1px #000,
                0 0 60px rgba(255,53,94,0.14),
                0 0 120px rgba(122,16,34,0.12),
                inset 0 0 40px rgba(255,53,94,0.04);
            position: relative;
            background: linear-gradient(180deg, #0d0406 0%, #060203 100%);
        }

        /* big ghost heart behind content */
        .ghost-heart {
            position: absolute;
            font-size: 340px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: var(--red);
            opacity: 0.022;
            pointer-events: none;
            z-index: 0;
            animation: ghostBeat 2.8s ease-in-out infinite;
            line-height: 1;
        }

        @keyframes ghostBeat {
            0%, 100% { transform: translate(-50%, -50%) scale(1);   opacity: 0.022; }
            14%       { transform: translate(-50%, -50%) scale(1.06); opacity: 0.038; }
            28%       { transform: translate(-50%, -50%) scale(1);   opacity: 0.022; }
            42%       { transform: translate(-50%, -50%) scale(1.04); opacity: 0.032; }
        }

        /* ── TOP BAR ── */
        .top-bar {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 10px;
            border-bottom: 1px solid var(--line);
            padding-bottom: 14px;
            margin-bottom: 16px;
            position: relative;
            z-index: 2;
        }

        /* ── LOGO ── */
        .vault-title-wrap {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .vault-logo-line {
            display: flex;
            align-items: baseline;
            gap: 0;
            font-family: var(--font-px);
            font-size: clamp(13px, 3.4vw, 22px);
            letter-spacing: 2px;
            line-height: 1.3;
        }

        .logo-full {
            color: var(--red-pale);
            text-shadow:
                0 0 10px rgba(255,214,224,0.55),
                2px 2px 0 rgba(90,15,31,0.8);
        }

        .logo-heart {
            color: var(--red);
            text-shadow: var(--glow-r);
            animation: logoBeat 2.8s ease-in-out infinite;
        }

        .logo-suffix {
            color: var(--muted);
            font-size: 0.6em;
            letter-spacing: 3px;
            margin-left: 6px;
            align-self: center;
        }

        @keyframes logoBeat {
            0%, 100% { text-shadow: 0 0 8px rgba(255,53,94,0.6), 0 0 20px rgba(255,53,94,0.25); transform: scale(1); }
            14%       { text-shadow: 0 0 18px rgba(255,53,94,1),   0 0 42px rgba(255,53,94,0.6);  transform: scale(1.08); }
            28%       { text-shadow: 0 0 8px rgba(255,53,94,0.6), 0 0 20px rgba(255,53,94,0.25); transform: scale(1); }
            42%       { text-shadow: 0 0 14px rgba(255,53,94,0.85),0 0 32px rgba(255,53,94,0.45); transform: scale(1.04); }
        }

        .vault-subtitle {
            font-family: var(--font-mono);
            font-size: 10px;
            color: var(--muted);
            letter-spacing: 3px;
            margin-top: 8px;
        }

        /* ECG / heartbeat line under logo */
        .ecg-line {
            width: 160px;
            height: 20px;
            margin-top: 10px;
            opacity: 0.55;
        }

        /* ── STATUS PILL ── */
        .status-pill {
            font-family: var(--font-mono);
            font-size: 9px;
            letter-spacing: 2px;
            color: var(--red-soft);
            border: 1px solid var(--blood);
            background: rgba(122,16,34,.18);
            padding: 6px 10px;
            white-space: nowrap;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
        }

        .status-heart {
            font-size: 14px;
            color: var(--red);
            animation: logoBeat 2.8s ease-in-out infinite;
            line-height: 1;
        }

        /* ── SYS MESSAGE ── */
        .sys-message {
            background: #060203;
            border: 1px solid var(--line);
            border-left: 3px solid var(--red);
            color: var(--red-soft);
            font-family: var(--font-mono);
            font-size: 10px;
            letter-spacing: 1.5px;
            padding: 7px 12px;
            margin-bottom: 16px;
            position: relative;
            z-index: 2;
            overflow: hidden;
        }

        .sys-message::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(90deg, rgba(255,53,94,0.06) 0%, transparent 60%);
            animation: sysSweep 3.5s ease-in-out infinite alternate;
        }

        @keyframes sysSweep {
            from { transform: translateX(-100%); }
            to   { transform: translateX(100%); }
        }

        /* ── NOW PLAYING ── */
        .now-playing {
            background: linear-gradient(135deg, rgba(59,13,20,0.38), rgba(6,2,3,0.95));
            border: 1px solid var(--blood);
            border-left: 4px solid var(--red);
            padding: 16px;
            margin-bottom: 12px;
            position: relative;
            z-index: 2;
            overflow: hidden;
        }

        .now-playing::after {
            content: "♥";
            position: absolute;
            right: -10px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 90px;
            color: var(--red);
            opacity: 0.06;
            pointer-events: none;
            animation: ghostBeat 2.8s ease-in-out infinite;
        }

        .now-label {
            font-family: var(--font-px);
            font-size: 7px;
            letter-spacing: 3px;
            color: var(--red);
            text-shadow: var(--glow-r);
            margin-bottom: 10px;
        }

        /* ── TRACK CARD ── */
        .track-card {
            background: linear-gradient(135deg, #0b0304 0%, #120609 100%);
            border: 1px solid var(--line);
            border-left: 3px solid var(--blood);
            padding: 13px 15px;
            margin-bottom: 10px;
            position: relative;
            z-index: 2;
            overflow: hidden;
            transition: border-left-color 0.12s ease, box-shadow 0.12s ease;
        }

        .track-card::before {
            content: "♥";
            position: absolute;
            right: 10px;
            bottom: 6px;
            font-size: 52px;
            color: var(--red);
            opacity: 0.04;
            pointer-events: none;
            transition: opacity 0.15s ease;
        }

        .track-card:hover {
            border-left-color: var(--red);
            box-shadow:
                0 0 20px rgba(255,53,94,0.10),
                inset 0 0 20px rgba(255,53,94,0.04);
        }

        .track-card:hover::before {
            opacity: 0.10;
        }

        /* staggered entrance */
        .track-card { animation: cardIn 0.35s ease both; }
        @keyframes cardIn {
            from { opacity: 0; transform: translateX(-8px); }
            to   { opacity: 1; transform: translateX(0); }
        }

        /* ── TRACK TYPOGRAPHY ── */
        .track-number {
            float: right;
            font-family: var(--font-px);
            font-size: 6px;
            color: rgba(255,53,94,0.22);
            letter-spacing: 1px;
        }

        .track-title {
            font-family: var(--font-orb);
            font-size: 17px;
            font-weight: 900;
            color: #f4dde2;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 7px;
        }

        .track-meta, .track-notes {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--muted);
            line-height: 1.6;
        }

        .mood-tag {
            display: inline-block;
            border: 1px solid currentColor;
            padding: 2px 8px;
            margin: 2px 4px 6px 0;
            font-family: var(--font-mono);
            font-size: 9px;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: rgba(255,53,94,0.04);
        }

        /* ── TRACK LAYOUT ── */
        .track-layout {
            display: flex;
            gap: 13px;
            align-items: center;
        }

        .track-info { flex: 1; min-width: 0; }

        /* ── COVER ART ── */
        .cover-wrap {
            position: relative;
            width: 74px;
            height: 74px;
            flex-shrink: 0;
        }

        .cover-art {
            width: 74px;
            height: 74px;
            object-fit: cover;
            border: 1px solid var(--blood);
            display: block;
            box-shadow:
                0 0 14px rgba(255,53,94,0.20),
                3px 3px 0 rgba(0,0,0,0.5);
        }

        /* subtle corner heart badge */
        .cover-wrap::after {
            content: "♥";
            position: absolute;
            bottom: -5px;
            right: -5px;
            font-size: 13px;
            color: var(--red);
            text-shadow: 0 0 6px rgba(255,53,94,0.8);
            line-height: 1;
            animation: logoBeat 2.8s ease-in-out infinite;
        }

        .cover-placeholder {
            width: 74px;
            height: 74px;
            background: linear-gradient(135deg, #3b0d14, #090203);
            border: 1px solid var(--blood);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            color: rgba(255,53,94,0.3);
            box-shadow: 3px 3px 0 rgba(0,0,0,0.5);
            animation: ghostBeat 2.8s ease-in-out infinite;
        }

        /* ── AUDIO PLAYER ── */
        .custom-audio-shell {
            background: linear-gradient(135deg, #100406, #060203);
            border: 1px solid var(--blood);
            border-left: 3px solid var(--red);
            padding: 10px 12px;
            margin: -2px 0 12px 0;
            position: relative;
            z-index: 2;
            overflow: hidden;
        }

        .custom-audio-shell::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, rgba(255,53,94,0.04) 0%, transparent 50%);
            pointer-events: none;
        }

        .audio-label {
            font-family: var(--font-px);
            font-size: 6px;
            letter-spacing: 2px;
            color: var(--red-soft);
            margin-bottom: 7px;
            text-shadow: 0 0 8px rgba(255,53,94,0.45);
        }

        .custom-audio {
            width: 100%;
            height: 34px;
            border-radius: 0;
            outline: 1px solid var(--line);
            background: #060203;
            filter:
                invert(14%)
                sepia(78%)
                saturate(2300%)
                hue-rotate(320deg)
                brightness(90%)
                contrast(125%);
        }

        .custom-audio::-webkit-media-controls-panel {
            background: linear-gradient(90deg, #1a050a, #3b0d14);
            border-radius: 0;
        }

        .custom-audio::-webkit-media-controls-current-time-display,
        .custom-audio::-webkit-media-controls-time-remaining-display {
            color: #ffdce3;
        }

        .custom-audio::-webkit-media-controls-timeline {
            filter: hue-rotate(310deg) saturate(2.2);
        }

        /* ── DIVIDER ── */
        .compact-divider {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--blood), var(--red), var(--blood), transparent);
            margin: 16px 0;
            opacity: 0.7;
            position: relative;
            z-index: 2;
        }

        /* ── STREAMLIT OVERRIDES ── */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: #060203 !important;
            border: 1px solid var(--line) !important;
            border-radius: 0 !important;
            color: #f0cbd2 !important;
            font-family: var(--font-mono) !important;
            caret-color: var(--red) !important;
        }

        .stTextInput label, .stTextArea label, .stFileUploader label {
            font-family: var(--font-mono) !important;
            font-size: 10px !important;
            color: var(--muted) !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
        }

        [data-testid="stFileUploader"] {
            border: 1px dashed var(--blood) !important;
            background: rgba(59,13,20,0.14) !important;
            padding: 8px !important;
        }

        .stButton > button {
            background: linear-gradient(180deg, var(--blood), var(--maroon)) !important;
            color: #ffe4e9 !important;
            border: 1px solid var(--blood) !important;
            border-radius: 0 !important;
            font-family: var(--font-mono) !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
            box-shadow: 2px 2px 0 #000, 0 0 12px rgba(255,53,94,0.14) !important;
            transition: all 0.12s ease !important;
        }

        .stButton > button:hover {
            background: linear-gradient(180deg, var(--red), var(--blood)) !important;
            box-shadow: 2px 2px 0 #000, 0 0 22px rgba(255,53,94,0.35) !important;
            transform: translate(-1px, -1px) !important;
        }

        .stExpander {
            border: 1px solid var(--line) !important;
            background: rgba(8,2,4,0.55) !important;
            margin-bottom: 12px;
        }

        .stSuccess {
            background: #0d0406 !important;
            border: 1px solid var(--blood) !important;
            border-left: 3px solid var(--red) !important;
            color: #ffdce3 !important;
            border-radius: 0 !important;
        }

        .stWarning {
            background: #120806 !important;
            border: 1px solid #9b5c66 !important;
            border-left: 3px solid #ff9aae !important;
            color: #ffcad4 !important;
            border-radius: 0 !important;
        }

        /* ── FOOTER BAR ── */
        .mini-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: linear-gradient(180deg, #180609, #060203);
            border-top: 1px solid var(--blood);
            color: var(--muted);
            font-family: var(--font-mono);
            font-size: 9px;
            letter-spacing: 2px;
            z-index: 1000;
        }

        .footer-heart {
            color: var(--red);
            animation: logoBeat 2.8s ease-in-out infinite;
            font-size: 11px;
        }

        /* ── SCROLLBAR ── */
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: var(--black); }
        ::-webkit-scrollbar-thumb { background: var(--blood); }
        ::-webkit-scrollbar-thumb:hover { background: var(--red); }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # floating hearts layer
    st.markdown(
        """
        <div class="hearts-bg" aria-hidden="true">
            <span class="heart-particle">♥</span>
            <span class="heart-particle">♥</span>
            <span class="heart-particle">♥</span>
            <span class="heart-particle">♥</span>
            <span class="heart-particle">♥</span>
            <span class="heart-particle">♥</span>
            <span class="heart-particle">♥</span>
            <span class="heart-particle">♥</span>
            <span class="heart-particle">♥</span>
            <span class="heart-particle">♥</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# DATA HELPERS
# ─────────────────────────────────────────────
def load_tracks() -> pd.DataFrame:
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        for col in ["title", "mood", "notes", "file", "uploaded_at", "cover"]:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=["title", "mood", "notes", "file", "uploaded_at", "cover"])


def mood_tag_html(mood_text: str) -> str:
    color = "#c4455c"
    return f'<span class="mood-tag" style="color:{color}; border-color:{color};">{mood_text.upper()}</span>'


def image_to_base64(image_path) -> str:
    if image_path is None:
        return ""
    image_path = Path(str(image_path).strip())
    if str(image_path) in ["", ".", "nan", "None"]:
        return ""
    if not image_path.exists() or not image_path.is_file():
        return ""
    ext = image_path.suffix.lower().replace(".", "")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}.get(ext)
    if not mime:
        return ""
    encoded = base64.b64encode(image_path.read_bytes()).decode()
    return f"data:{mime};base64,{encoded}"


def render_audio_player(audio_path: Path):
    audio_bytes = audio_path.read_bytes()
    encoded = base64.b64encode(audio_bytes).decode()
    ext = audio_path.suffix.lower().replace(".", "")
    mime = {
        "mp3": "audio/mpeg", "wav": "audio/wav",
        "ogg": "audio/ogg", "flac": "audio/flac", "m4a": "audio/mp4",
    }.get(ext, "audio/mpeg")

    audio_html = (
        '<div class="custom-audio-shell">'
        '<div class="audio-label">▶ PLAYBACK_MODULE // ACTIVE</div>'
        f'<audio controls class="custom-audio">'
        f'<source src="data:{mime};base64,{encoded}" type="{mime}">'
        '</audio>'
        '</div>'
    )
    st.markdown(audio_html, unsafe_allow_html=True)


def render_track_card(row: pd.Series, index: int, featured: bool = False):
    audio_path = Path(str(row.get("file", "")))
    file_ok = audio_path.exists()

    title       = html.escape(str(row.get("title", "UNTITLED")))
    mood        = html.escape(str(row.get("mood", "")))
    notes_raw   = row.get("notes", "")
    notes       = "" if pd.isna(notes_raw) else html.escape(str(notes_raw))
    uploaded_raw = row.get("uploaded_at", "")
    uploaded    = "" if pd.isna(uploaded_raw) else html.escape(str(uploaded_raw))

    mood_html   = mood_tag_html(mood)
    wrapper     = "now-playing" if featured else "track-card"
    label       = "NOW PLAYING // FEATURED RANDOM PICK" if featured else f"TRACK_{index:03d}"
    now_label   = '<div class="now-label">♥ NOW PLAYING</div>' if featured else ""

    notes_html  = f'<div class="track-notes">{notes}</div>' if notes and notes.lower() != "nan" else ""
    missing_html = (
        ""
        if file_ok
        else f'<div class="track-notes" style="color:#ff9aae;">⚠ FILE NOT FOUND: {html.escape(str(audio_path))}</div>'
    )

    cover_raw  = row.get("cover", "")
    cover_path = Path(str(cover_raw).strip()) if pd.notna(cover_raw) and str(cover_raw).strip() else None
    cover_src  = image_to_base64(cover_path)

    if cover_src:
        cover_html = (
            '<div class="cover-wrap">'
            f'<img class="cover-art" src="{cover_src}" alt="cover art">'
            '</div>'
        )
    else:
        cover_html = '<div class="cover-wrap"><div class="cover-placeholder">♥</div></div>'

    card_html = (
        f'<div class="{wrapper}" style="animation-delay:{(index-1)*0.06:.2f}s">'
        f'<div class="track-number">{label}</div>'
        f'{now_label}'
        f'<div class="track-layout">'
        f'{cover_html}'
        f'<div class="track-info">'
        f'<div class="track-title">{title.upper()}</div>'
        f'<div class="track-meta">'
        f'{mood_html}'
        f'<span style="color:#7d4b55; margin-left:6px; font-size:10px;">{uploaded}</span>'
        f'</div>'
        f'{notes_html}'
        f'{missing_html}'
        f'</div>'
        f'</div>'
        f'</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)
    if file_ok:
        render_audio_player(audio_path)


# ─────────────────────────────────────────────
# ECG SVG
# ─────────────────────────────────────────────
ECG_SVG = """
<svg class="ecg-line" viewBox="0 0 160 20" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1.2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <polyline
    points="0,10 18,10 22,10 24,3 27,17 30,3 33,17 36,10 40,10 44,10 50,10 54,7 58,10 160,10"
    fill="none"
    stroke="#ff355e"
    stroke-width="1.2"
    filter="url(#glow)"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <animate attributeName="stroke-dasharray" values="0,300;300,0" dur="2.8s" repeatCount="indefinite"/>
    <animate attributeName="stroke-dashoffset" values="300;0" dur="2.8s" repeatCount="indefinite"/>
  </polyline>
</svg>
"""


def compact_footer():
    st.markdown(
        f"""
        <div class="mini-footer">
            FULLHEART_VAULT.EXE
            <span class="footer-heart">♥</span>
            AUDIO PLAYER
            <span class="footer-heart">♥</span>
            {datetime.now().strftime('%H:%M')}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    inject_css()
    compact_footer()
    df = load_tracks()

    st.markdown('<div class="player-shell"><div class="ghost-heart">♥</div>', unsafe_allow_html=True)

    track_count = f"{len(df):02d}"
    sys_msg = random.choice(SYSTEM_MESSAGES)
    st.markdown(
        f"""
        <div class="top-bar">
            <div class="vault-title-wrap">
                <div class="vault-logo-line">
                    <span class="logo-full">FULL</span><span class="logo-heart">HEART</span>
                    <span class="logo-suffix">_VAULT.EXE</span>
                </div>
                <div class="vault-subtitle">UNRELEASED // DEMOS // ARCHIVE PLAYER</div>
            </div>
            <div class="status-pill">
                <span class="status-heart">&#9829;</span>
                {track_count}&#160;TRACKS
            </div>
        </div>
        <div class="sys-message">SYS // {sys_msg}</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(ECG_SVG, unsafe_allow_html=True)

    if df.empty:
        st.markdown(
            """
            <div class="now-playing">
                <div class="now-label">♥ EMPTY VAULT</div>
                <div class="track-title">NO TRACKS LOADED</div>
                <div class="track-notes">Open the upload drawer below to add your first unreleased track.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        recent_tracks = df.iloc[::-1]
        for display_index, (row_index, row) in enumerate(recent_tracks.iterrows(), start=1):
            render_track_card(row, display_index)

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()