import streamlit as st
import requests

st.set_page_config(
    page_title="LeafScan AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none !important; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1300px !important; margin: 0 auto; }

.stApp {
    background: #0d0d0d !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f0f0f0 !important;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 20%, rgba(0,255,100,0.05) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,180,80,0.04) 0%, transparent 60%);
    pointer-events: none; z-index: 0;
}

/* ---- Kill ALL internal Streamlit backgrounds ---- */
.stApp > div, section.main > div,
[data-testid="stAppViewContainer"] > section > div,
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlock"] > div,
[data-testid="stHorizontalBlock"],
.element-container,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] > div,
div[data-testid="column"],
div[data-testid="column"] > div,
div[data-testid="column"] > div > div,
div[data-testid="column"] > div > div > div,
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* ---- Hero ---- */
.hero-wrap { text-align: center; padding: 3rem 1rem 1.5rem; position: relative; z-index: 2; }
.pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(0,255,100,0.07); border: 1px solid rgba(0,255,100,0.2);
    border-radius: 999px; padding: 5px 14px;
    font-size: 0.72rem; font-weight: 600; color: #00ff64;
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 1.2rem;
}
.pill-dot { width:6px; height:6px; border-radius:50%; background:#00ff64; box-shadow:0 0 8px #00ff64; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
.hero-title { font-size: clamp(2.5rem,5.5vw,4.5rem); font-weight:700; line-height:1.05; letter-spacing:-1.5px; color:#fff; margin-bottom:0.8rem; }
.hero-title span { color: #00ff64; }
.hero-sub { font-size:0.95rem; color:#666; max-width:400px; margin:0 auto 1.8rem; line-height:1.7; }
.hero-stats { display:inline-flex; gap:0; border:1px solid #1f1f1f; border-radius:14px; overflow:hidden; }
.stat-item { padding:0.9rem 1.8rem; text-align:center; border-right:1px solid #1f1f1f; }
.stat-item:last-child { border-right:none; }
.stat-val { font-family:'Space Mono',monospace; font-size:1.4rem; font-weight:700; color:#00ff64; display:block; }
.stat-lbl { font-size:0.62rem; color:#555; text-transform:uppercase; letter-spacing:1.5px; display:block; margin-top:2px; }

/* ---- Section labels ---- */
.sec-label {
    font-size:0.62rem; font-weight:700; color:#555;
    text-transform:uppercase; letter-spacing:2.5px;
    margin-bottom:1rem; display:flex; align-items:center; gap:10px;
}
.sec-label::after { content:''; flex:1; height:1px; background:#1f1f1f; }

/* ---- FILE UPLOADER ---- */
[data-testid="stFileUploader"] {
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploader"] > div,
[data-testid="stFileUploader"] > div > div {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stFileUploadDropzone"] {
    background: #111 !important;
    border: 1.5px dashed #2a2a2a !important;
    border-radius: 14px !important;
    transition: all 0.3s !important;
    cursor: pointer !important;
    min-height: 130px !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: #00ff64 !important;
    background: rgba(0,255,100,0.04) !important;
}
[data-testid="stFileUploadDropzone"] > div {
    background: transparent !important;
    padding: 1.5rem !important;
}
/* Text inside dropzone */
[data-testid="stFileUploadDropzone"] span,
[data-testid="stFileUploadDropzone"] p,
[data-testid="stFileUploadDropzone"] small {
    color: #555 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.85rem !important;
    background: transparent !important;
}
/* Upload icon */
[data-testid="stFileUploadDropzone"] svg {
    color: #444 !important; fill: #444 !important;
}
[data-testid="stFileUploadDropzone"]:hover svg {
    color: #00ff64 !important; fill: #00ff64 !important;
}
/* ===== BROWSE FILES BUTTON - THE MAIN FIX ===== */
[data-testid="stFileUploadDropzone"] button,
[data-testid="stFileUploadDropzone"] button:focus,
[data-testid="stFileUploadDropzone"] button:active {
    background-color: #00ff64 !important;
    background: #00ff64 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    padding: 8px 18px !important;
    cursor: pointer !important;
    min-height: unset !important;
    height: auto !important;
    width: auto !important;
    transition: all 0.2s !important;
}
[data-testid="stFileUploadDropzone"] button:hover {
    background-color: #00e558 !important;
    background: #00e558 !important;
    box-shadow: 0 0 20px rgba(0,255,100,0.4) !important;
    transform: translateY(-1px) !important;
}
/* Force button text color no matter what */
[data-testid="stFileUploadDropzone"] button *,
[data-testid="stFileUploadDropzone"] button p,
[data-testid="stFileUploadDropzone"] button span {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    background: transparent !important;
    font-weight: 700 !important;
}
/* Uploaded file chip */
[data-testid="stFileUploaderFile"] {
    background: #161616 !important;
    border: 1px solid #222 !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
    margin-top: 0.6rem !important;
}
[data-testid="stFileUploaderFile"] *,
[data-testid="stFileUploaderFileName"] {
    color: #666 !important; background: transparent !important;
    font-size: 0.8rem !important;
}
[data-testid="stFileUploaderDeleteBtn"] button,
[data-testid="stFileUploaderDeleteBtn"] button * {
    background: transparent !important;
    color: #444 !important;
    -webkit-text-fill-color: #444 !important;
    border: none !important; box-shadow: none !important;
    min-height: unset !important; width: auto !important;
    padding: 2px 6px !important;
}
[data-testid="stFileUploaderDeleteBtn"] button:hover,
[data-testid="stFileUploaderDeleteBtn"] button:hover * {
    color: #ff5555 !important;
    -webkit-text-fill-color: #ff5555 !important;
    background: transparent !important;
}

/* Image */
[data-testid="stImage"] { background: transparent !important; }
[data-testid="stImage"] img {
    border-radius: 12px !important;
    border: 1px solid #1f1f1f !important;
    width: 100% !important; margin-top: 0.8rem !important;
}

/* Analyze button */
[data-testid="stButton"] > button {
    background: #00ff64 !important;
    color: #000 !important;
    -webkit-text-fill-color: #000 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 14px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.25s !important;
    box-shadow: 0 0 30px rgba(0,255,100,0.15) !important;
    margin-top: 1rem !important;
}
[data-testid="stButton"] > button * {
    color: #000 !important;
    -webkit-text-fill-color: #000 !important;
}
[data-testid="stButton"] > button:hover {
    background: #00e558 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 40px rgba(0,255,100,0.3) !important;
}

/* Result content */
.empty-box { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:260px; gap:12px; }
.empty-icon { font-size:2.5rem; opacity:0.5; animation:bob 3s ease-in-out infinite; }
@keyframes bob { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-10px);} }
.empty-msg { font-size:0.85rem; color:#555; text-align:center; line-height:1.7; }

.disease-top { display:flex; justify-content:space-between; align-items:flex-start; padding-bottom:1rem; margin-bottom:1rem; border-bottom:1px solid #1f1f1f; }
.disease-label { font-size:0.58rem; color:#555; text-transform:uppercase; letter-spacing:2px; margin-bottom:5px; }
.disease-name { font-size:1.4rem; font-weight:700; color:#fff; line-height:1.2; }
.conf-box { text-align:center; }
.conf-num { font-family:'Space Mono',monospace; font-size:1.5rem; font-weight:700; color:#00ff64; display:block; }
.conf-lbl { font-size:0.58rem; color:#555; text-transform:uppercase; letter-spacing:1px; }

.tags { display:flex; flex-wrap:wrap; gap:7px; margin-bottom:1.1rem; }
.tag { font-size:0.72rem; font-weight:500; padding:4px 12px; border-radius:999px; border:1px solid; }
.tag-g { color:#00ff64; border-color:#00ff6433; background:#00ff6410; }
.tag-y { color:#fbbf24; border-color:#fbbf2433; background:#fbbf2410; }
.tag-o { color:#fb923c; border-color:#fb923c33; background:#fb923c10; }
.tag-r { color:#f87171; border-color:#f8717133; background:#f8717110; }

.sec-h { font-size:0.6rem; font-weight:700; color:#444; text-transform:uppercase; letter-spacing:2px; margin-bottom:7px; display:flex; align-items:center; gap:8px; }
.sec-h::after { content:''; flex:1; height:1px; background:#1a1a1a; }
.items { display:flex; flex-direction:column; gap:4px; margin-bottom:1.1rem; }
.item-r { font-size:0.83rem; color:#777; line-height:1.5; padding:7px 12px 7px 12px; border-left:2px solid #1f1f1f; border-radius:0 8px 8px 0; background:#0d0d0d; transition:all 0.2s; }
.item-r:hover { border-left-color:#00ff64; color:#aaa; }

.healthy-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:260px; gap:10px; text-align:center; }
.healthy-icon { font-size:3rem; animation:pop 0.5s cubic-bezier(0.34,1.56,0.64,1); }
@keyframes pop { from{transform:scale(0);} to{transform:scale(1);} }
.healthy-title { font-size:1.7rem; font-weight:700; color:#00ff64; }
.healthy-sub { font-size:0.85rem; color:#555; }
.ts { font-size:0.65rem; color:#333; margin-top:1rem; padding-top:0.8rem; border-top:1px solid #1a1a1a; font-family:'Space Mono',monospace; }

[data-testid="stAlert"] { background:#1a0a0a !important; border:1px solid #3a1010 !important; border-radius:10px !important; color:#f87171 !important; }
[data-testid="stSpinner"] p { color:#555 !important; }
::-webkit-scrollbar { width:4px; } ::-webkit-scrollbar-track { background:#0d0d0d; } ::-webkit-scrollbar-thumb { background:#222; border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="pill"><div class="pill-dot"></div>Groq Vision AI</div>
    <div class="hero-title">Detect leaf<br><span>diseases instantly</span></div>
    <div class="hero-sub">Upload a plant leaf photo. AI diagnoses diseases and recommends treatment in seconds.</div>
    <div class="hero-stats">
        <div class="stat-item"><span class="stat-val">50+</span><span class="stat-lbl">Diseases</span></div>
        <div class="stat-item"><span class="stat-val">95%</span><span class="stat-lbl">Accuracy</span></div>
        <div class="stat-item"><span class="stat-val">&lt;3s</span><span class="stat-lbl">Speed</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

api_url = "http://leaf-diseases-detect.vercel.app"

col1, col2 = st.columns([1, 1.5], gap="large")

# ── LEFT COLUMN ──────────────────────────────────────
with col1:
    st.markdown("<div class='sec-label'>Upload leaf image</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop image here", type=["jpg","jpeg","png"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)
        st.button("ANALYZE LEAF →", use_container_width=True, key="analyze_btn")

# ── RIGHT COLUMN ─────────────────────────────────────
with col2:
    st.markdown("<div class='sec-label'>Analysis result</div>", unsafe_allow_html=True)

    if not uploaded_file:
        st.markdown("""
        <div class='empty-box'>
            <div class='empty-icon'>🌿</div>
            <div class='empty-msg'>Upload a leaf image on the left<br>to begin AI diagnosis</div>
        </div>""", unsafe_allow_html=True)

    elif not st.session_state.get("analyze_btn"):
        st.markdown("""
        <div class='empty-box'>
            <div class='empty-icon'>🔬</div>
            <div class='empty-msg'>Press <b style='color:#00ff64;'>ANALYZE LEAF</b><br>to run the scan</div>
        </div>""", unsafe_allow_html=True)

    else:
        with st.spinner("Analyzing with AI..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{api_url}/disease-detection-file", files=files)

                if response.status_code == 200:
                    r = response.json()

                    if r.get("disease_type") == "invalid_image":
                        st.markdown("""
                        <div class='empty-box'>
                            <div class='empty-icon'>⚠️</div>
                            <div class='empty-msg' style='color:#fb923c;font-size:1rem;font-weight:600;'>Invalid Image</div>
                            <div class='empty-msg'>Please upload a clear photo of a plant leaf.</div>
                        </div>""", unsafe_allow_html=True)

                    elif r.get("disease_detected"):
                        sev = r.get("severity","").lower()
                        sev_cls = {"low":"tag-y","moderate":"tag-o","high":"tag-r"}.get(sev,"tag-y")
                        st.markdown(f"""
                        <div class='disease-top'>
                            <div>
                                <div class='disease-label'>Detected Disease</div>
                                <div class='disease-name'>🦠 {r.get('disease_name','Unknown')}</div>
                            </div>
                            <div class='conf-box'>
                                <span class='conf-num'>{r.get('confidence',0)}%</span>
                                <span class='conf-lbl'>confidence</span>
                            </div>
                        </div>
                        <div class='tags'>
                            <span class='tag tag-g'>{r.get('disease_type','N/A')}</span>
                            <span class='tag {sev_cls}'>Severity: {r.get('severity','N/A')}</span>
                        </div>""", unsafe_allow_html=True)

                        for title, key in [("Symptoms","symptoms"),("Possible Causes","possible_causes"),("Treatment Plan","treatment")]:
                            items = r.get(key, [])
                            if items:
                                st.markdown(f"<div class='sec-h'>{title}</div><div class='items'>", unsafe_allow_html=True)
                                for item in items:
                                    st.markdown(f"<div class='item-r'>{item}</div>", unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)

                        st.markdown(f"<div class='ts'>🕒 {r.get('analysis_timestamp','N/A')}</div>", unsafe_allow_html=True)

                    else:
                        st.markdown(f"""
                        <div class='healthy-wrap'>
                            <div class='healthy-icon'>✅</div>
                            <div class='healthy-title'>Healthy Leaf</div>
                            <div class='healthy-sub'>No disease detected. Your plant is thriving!</div>
                            <div class='tags' style='justify-content:center;margin-top:0.5rem;'>
                                <span class='tag tag-g'>Status: Healthy</span>
                                <span class='tag tag-g'>{r.get('confidence','N/A')}% Confidence</span>
                            </div>
                            <div class='ts'>🕒 {r.get('analysis_timestamp','N/A')}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.error(f"API Error {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
