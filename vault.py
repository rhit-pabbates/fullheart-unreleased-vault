"""
FULLHEART_VAULT.EXE — Compact Unreleased Music Player
Single-file Streamlit application.
Aesthetic: compact FullHeart red/maroon arcade audio player.
"""

import random
from datetime import datetime
from pathlib import Path
from textwrap import dedent
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
]

# ─────────────────────────────────────────────
# CSS — COMPACT FULLHEART PLAYER THEME
# ─────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=VT323&family=Orbitron:wght@400;700;900&family=Press+Start+2P&display=swap');

        :root {
            --black: #050203;
            --panel: #100507;
            --panel-2: #17070c;
            --maroon: #3b0d14;
            --wine: #5a0f1f;
            --blood: #7a1022;
            --crimson: #8b0000;
            --red: #ff355e;
            --red-soft: #c4455c;
            --silver: #b8b8b8;
            --muted: #7d4b55;
            --line: #3a1018;
            --glow-r: 0 0 8px #ff355e, 0 0 22px rgba(255,53,94,.35);
            --font-mono: 'Share Tech Mono', monospace;
            --font-vt: 'VT323', monospace;
            --font-orb: 'Orbitron', sans-serif;
            --font-px: 'Press Start 2P', monospace;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background:
                repeating-linear-gradient(
                    90deg,
                    rgba(255, 53, 94, 0.10) 0px,
                    rgba(255, 53, 94, 0.10) 2px,
                    transparent 2px,
                    transparent 18px
                ),
                radial-gradient(circle at 12% 30%, rgba(255, 53, 94, 0.18), transparent 18%),
                radial-gradient(circle at 88% 70%, rgba(122, 16, 34, 0.28), transparent 20%),
                #050000 !important;
            color: var(--silver) !important;
            font-family: var(--font-mono) !important;
            cursor: crosshair;
            background-size: 60px 60px, cover !important;
            animation: bgDrift 18s linear infinite;
        }

        [data-testid="stAppViewContainer"]::before {
            content: "";
            position: fixed;
            top: 0;
            bottom: 0;
            width: 220px;
            right: 0;
            pointer-events: none;
            z-index: 1;
            background:
                repeating-linear-gradient(
                    -45deg,
                    rgba(255, 53, 94, 0.18) 0px,
                    rgba(255, 53, 94, 0.18) 2px,
                    transparent 2px,
                    transparent 14px
                ),
                radial-gradient(circle, rgba(139, 0, 0, 0.28), transparent 55%);
            background-size: 80px 80px, cover;
            animation: sideScroll 6s linear infinite, sidePulse 2.5s ease-in-out infinite alternate;
        }

        [data-testid="stAppViewContainer"]::after {
            content: "";
            position: fixed;
            top: 0;
            bottom: 0;
            width: 220px;
            left: 0;
            pointer-events: none;
            z-index: 1;
            background:
                repeating-linear-gradient(
                    45deg,
                    rgba(255, 53, 94, 0.18) 0px,
                    rgba(255, 53, 94, 0.18) 2px,
                    transparent 2px,
                    transparent 14px
                ),
                radial-gradient(circle, rgba(255, 53, 94, 0.22), transparent 55%);
            background-size: 80px 80px, cover;
            animation: sideScroll 6s linear infinite, sidePulse 2.5s ease-in-out infinite alternate-reverse;
        }

        @keyframes bgDrift {
            from { background-position: 0 0, center; }
            to   { background-position: 240px 120px, center; }
        }

        @keyframes sideScroll {
            from { background-position: 0 0, center; }
            to   { background-position: 0 240px, center; }
        }

        @keyframes sidePulse {
            from {
                opacity: 0.25;
                filter: blur(0px) brightness(0.8);
            }
            to {
                opacity: 0.75;
                filter: blur(1px) brightness(1.4);
            }
        }

        .block-container {
            max-width: 780px !important;
            padding: 1.25rem 1rem 3.75rem !important;
            position: relative;
            z-index: 5;
        }

        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }

        #MainMenu, footer, header, [data-testid="stToolbar"], .stDeployButton {
            visibility: hidden !important;
            display: none !important;
        }

        .player-shell {
            background: linear-gradient(135deg, rgba(16,5,7,.96), rgba(36,8,14,.96));
            border: 1px solid var(--blood);
            border-top: 2px solid var(--red);
            box-shadow: 0 0 0 1px #000, 7px 7px 0 rgba(0,0,0,.55), 0 0 36px rgba(255,53,94,.16);
            padding: 16px;
            position: relative;
            overflow: hidden;
        }

        .player-shell::before {
            content: 'FULLHEART AUDIO VAULT';
            position: absolute;
            top: 10px;
            right: 12px;
            font-family: var(--font-px);
            font-size: 6px;
            letter-spacing: 2px;
            color: rgba(255,53,94,.18);
        }

        .top-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            border-bottom: 1px solid var(--line);
            padding-bottom: 12px;
            margin-bottom: 14px;
        }

        .vault-title {
            font-family: var(--font-px);
            color: var(--red);
            font-size: clamp(16px, 4vw, 28px);
            letter-spacing: 3px;
            text-shadow: 2px 2px 0 #3b0d14, var(--glow-r);
            line-height: 1.25;
            animation: titleGlow 2.2s ease-in-out infinite alternate !important;
        }

        @keyframes titleGlow {
            from {
                text-shadow:
                    0 0 8px rgba(255, 53, 94, 0.6),
                    0 0 18px rgba(255, 53, 94, 0.25);
            }
            to {
                text-shadow:
                    0 0 14px rgba(255, 53, 94, 0.95),
                    0 0 38px rgba(255, 53, 94, 0.55),
                    3px 3px 0 #3b0d14;
            }
        }

        .status-pill {
            font-family: var(--font-mono);
            font-size: 10px;
            letter-spacing: 2px;
            color: var(--red-soft);
            border: 1px solid var(--blood);
            background: rgba(122,16,34,.22);
            padding: 5px 8px;
            white-space: nowrap;
        }

        .sys-message {
            background: #0a0305;
            border: 1px solid var(--line);
            border-left: 3px solid var(--red);
            color: var(--red-soft);
            font-family: var(--font-mono);
            font-size: 11px;
            letter-spacing: 1px;
            padding: 8px 10px;
            margin-bottom: 14px;
            box-shadow: inset 0 0 18px rgba(255,53,94,.04);
            animation: sysPulse 2s ease-in-out infinite alternate !important;
        }

        @keyframes sysPulse {
            from {
                box-shadow: 0 0 4px rgba(255, 53, 94, 0.2);
                opacity: 0.75;
            }
            to {
                box-shadow: 0 0 18px rgba(255, 53, 94, 0.55);
                opacity: 1;
            }
        }

        .now-playing {
            background: linear-gradient(135deg, rgba(59,13,20,.42), rgba(8,2,4,.92));
            border: 1px solid var(--blood);
            border-left: 4px solid var(--red);
            padding: 14px;
            margin-bottom: 14px;
            box-shadow: inset 0 0 22px rgba(255,53,94,.05);
        }

        .now-label {
            font-family: var(--font-px);
            font-size: 7px;
            letter-spacing: 3px;
            color: var(--red);
            text-shadow: var(--glow-r);
            margin-bottom: 9px;
        }

        .track-title {
            font-family: var(--font-orb);
            font-size: 18px;
            font-weight: 900;
            color: #f2d7dc;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        .track-meta, .track-notes {
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--muted);
            line-height: 1.55;
        }

        .track-card {
            background: linear-gradient(135deg, #0b0305 0%, #15070b 100%);
            border: 1px solid var(--line);
            border-left: 3px solid var(--blood);
            padding: 12px 14px;
            margin-bottom: 10px;
            transition: all .15s ease;
        }

        .track-card:hover {
            border-left-color: var(--red);
            box-shadow: 0 0 18px rgba(255,53,94,.12), inset 0 0 18px rgba(255,53,94,.04);
            animation: cardJitter 0.18s steps(2) infinite;
        }

        @keyframes cardJitter {
            0%   { transform: translateX(2px); }
            50%  { transform: translateX(4px); }
            100% { transform: translateX(1px); }
        }

        .track-number {
            float: right;
            font-family: var(--font-px);
            font-size: 7px;
            color: rgba(255,53,94,.26);
            letter-spacing: 1px;
        }

        .mood-tag {
            display: inline-block;
            border: 1px solid currentColor;
            padding: 2px 7px;
            margin: 2px 4px 6px 0;
            font-family: var(--font-mono);
            font-size: 9px;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: rgba(255,53,94,.04);
        }

        .compact-divider {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--blood), var(--red), var(--blood), transparent);
            margin: 14px 0;
            opacity: .85;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: #080304 !important;
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
            background: rgba(59,13,20,.16) !important;
            padding: 8px !important;
        }

        .stButton > button {
            background: linear-gradient(180deg, var(--blood), var(--maroon)) !important;
            color: #ffe4e9 !important;
            border: 1px solid var(--red) !important;
            border-radius: 0 !important;
            font-family: var(--font-mono) !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
            box-shadow: 2px 2px 0 #000, 0 0 12px rgba(255,53,94,.16) !important;
        }

        .stButton > button:hover {
            background: linear-gradient(180deg, var(--red), var(--blood)) !important;
            transform: translate(-1px, -1px);
        }

        .stExpander {
            border: 1px solid var(--line) !important;
            background: rgba(10,3,5,.48) !important;
            margin-bottom: 12px;
        }

        .stSuccess {
            background: #100507 !important;
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

        .mini-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(180deg, #21070c, #090203);
            border-top: 1px solid var(--blood);
            color: var(--muted);
            font-family: var(--font-mono);
            font-size: 10px;
            letter-spacing: 2px;
            z-index: 1000;
        }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #050203; }
        ::-webkit-scrollbar-thumb { background: var(--blood); }
        ::-webkit-scrollbar-thumb:hover { background: var(--red); }
        .custom-audio-shell {
        background: linear-gradient(135deg, #140508, #090203);
        border: 1px solid var(--blood);
        border-left: 3px solid var(--red);
        padding: 10px;
        margin: -2px 0 14px 0;
        box-shadow:
            inset 0 0 18px rgba(255, 53, 94, 0.08),
            0 0 14px rgba(255, 53, 94, 0.08);
    }
    
    .audio-label {
        font-family: var(--font-px);
        font-size: 7px;
        letter-spacing: 2px;
        color: var(--red-soft);
        margin-bottom: 8px;
        text-shadow: 0 0 8px rgba(255, 53, 94, 0.45);
    }
    
    .custom-audio {
        width: 100%;
        height: 34px;
        border-radius: 0;
        outline: 1px solid var(--line);
        background: #090203;
        filter:
            invert(14%)
            sepia(78%)
            saturate(2300%)
            hue-rotate(320deg)
            brightness(88%)
            contrast(120%);
    }
    
    /* Chrome/Safari audio inner controls */
    .custom-audio::-webkit-media-controls-panel {
        background: linear-gradient(90deg, #21070c, #3b0d14);
        border-radius: 0;
    }
    
    .custom-audio::-webkit-media-controls-play-button,
    .custom-audio::-webkit-media-controls-mute-button {
        filter: invert(1);
    }
    
    .custom-audio::-webkit-media-controls-current-time-display,
    .custom-audio::-webkit-media-controls-time-remaining-display {
        color: #ffdce3;
        text-shadow: 0 0 4px rgba(255, 53, 94, 0.45);
    }
    
    .custom-audio::-webkit-media-controls-timeline {
        filter: hue-rotate(310deg) saturate(2);
        }
        .track-layout {
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    .cover-art {
        width: 72px;
        height: 72px;
        object-fit: cover;
        border: 1px solid var(--blood);
        box-shadow:
            0 0 12px rgba(255,53,94,.18),
            3px 3px 0 rgba(0,0,0,.45);
        flex-shrink: 0;
    }
    
    .track-info {
        flex: 1;
        min-width: 0;
    }
        </style>
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

def render_track_card(row: pd.Series, index: int, featured: bool = False):
    audio_path = Path(str(row.get("file", "")))
    file_ok = audio_path.exists()

    title = html.escape(str(row.get("title", "UNTITLED")))
    mood = html.escape(str(row.get("mood", "")))
    notes_raw = row.get("notes", "")
    notes = "" if pd.isna(notes_raw) else html.escape(str(notes_raw))
    uploaded_raw = row.get("uploaded_at", "")
    uploaded = "" if pd.isna(uploaded_raw) else html.escape(str(uploaded_raw))

    mood_html = mood_tag_html(mood)

    wrapper = "now-playing" if featured else "track-card"
    label = "NOW PLAYING // FEATURED RANDOM PICK" if featured else f"TRACK_{index:03d}"
    now_label = '<div class="now-label">▶ NOW PLAYING</div>' if featured else ""

    notes_html = (
        f'<div class="track-notes">{notes}</div>'
        if notes and notes.lower() != "nan"
        else ""
    )

    missing_html = (
        ""
        if file_ok
        else f'<div class="track-notes" style="color:#ff9aae;">⚠ FILE NOT FOUND: {html.escape(str(audio_path))}</div>'
    )

    cover_raw = row.get("cover", "")
    cover_path = Path(str(cover_raw).strip()) if pd.notna(cover_raw) and str(cover_raw).strip() else None
    cover_src = image_to_base64(cover_path)

    cover_html = (
        f'<img class="cover-art" src="{cover_src}" alt="cover art">'
        if cover_src
        else '<div class="cover-art" style="background:linear-gradient(135deg,#3b0d14,#090203);"></div>'
    )

    card_html = (
        f'<div class="{wrapper}">'
        f'<div class="track-number">{label}</div>'
        f'{now_label}'
        f'<div class="track-layout">'
        f'{cover_html}'
        f'<div class="track-info">'
        f'<div class="track-title">{title.upper()}</div>'
        f'<div class="track-meta">'
        f'{mood_html}'
        f'<span style="color:#7d4b55; margin-left:4px;">{uploaded}</span>'
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

def render_audio_player(audio_path: Path):
    audio_bytes = audio_path.read_bytes()
    encoded = base64.b64encode(audio_bytes).decode()

    ext = audio_path.suffix.lower().replace(".", "")
    mime = {
        "mp3": "audio/mpeg",
        "wav": "audio/wav",
        "ogg": "audio/ogg",
        "flac": "audio/flac",
        "m4a": "audio/mp4",
    }.get(ext, "audio/mpeg")

    audio_html = (
        '<div class="custom-audio-shell">'
        '<div class="audio-label">PLAYBACK_MODULE_ACTIVE</div>'
        f'<audio controls class="custom-audio">'
        f'<source src="data:{mime};base64,{encoded}" type="{mime}">'
        '</audio>'
        '</div>'
    )

    st.markdown(audio_html, unsafe_allow_html=True)

def image_to_base64(image_path: Path) -> str:
    if not image_path or str(image_path).strip() in ["", ".", "nan", "None"]:
        return ""

    if not image_path.exists() or not image_path.is_file():
        return ""

    ext = image_path.suffix.lower().replace(".", "")
    mime = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
    }.get(ext)

    if not mime:
        return ""

    encoded = base64.b64encode(image_path.read_bytes()).decode()
    return f"data:{mime};base64,{encoded}"

def compact_footer():
    st.markdown(
        f"""
        <div class="mini-footer">
            FULLHEART_VAULT.EXE // AUDIO PLAYER // {datetime.now().strftime('%H:%M')}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# MAIN APP — NO SIDEBAR, SINGLE COMPACT PLAYER
# ─────────────────────────────────────────────
def main():
    inject_css()
    compact_footer()
    df = load_tracks()

    st.markdown('<div class="player-shell">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="top-bar">
            <div>
                <div class="vault-title">FULLHEART_VAULT.EXE</div>
                <div style="font-family:'Share Tech Mono'; font-size:11px; color:#7d4b55; letter-spacing:3px; margin-top:7px;">
                    UNRELEASED // DEMOS // ARCHIVE PLAYER
                </div>
            </div>
            <div class="status-pill">{len(df):02d} TRACKS</div>
        </div>
        <div class="sys-message">SYS // {random.choice(SYSTEM_MESSAGES)}</div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.markdown(
            """
            <div class="now-playing">
                <div class="now-label">▶ EMPTY VAULT</div>
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

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()