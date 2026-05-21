"""
🌟 مجلس البينة V3 - نظام السبورة السوداء التفاعلية
محرك البحث القرآني مع الملاحة العائمة والحفظ الديناميكي
"""

import streamlit as st
import pandas as pd
import re
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import json

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⚙️ إعدادات Streamlit
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="مجلس البينة V3 - السبورة السوداء",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 التصميم والأنماط
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #ffffff;
        margin: 0;
        padding: 0;
    }
    
    [data-testid="stVerticalBlockBG"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        padding: 0;
    }
    
    .main-container {
        width: 100%;
        max-width: 100%;
        background: transparent;
    }
    
    .search-header {
        background: rgba(0, 20, 40, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 2px solid #00ccff;
        padding: 15px;
        margin: 0;
        position: sticky;
        top: 0;
        z-index: 100;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
    }
    
    .search-input-wrapper {
        flex: 1;
        display: flex;
        justify-content: center;
    }
    
    .icon-wrapper {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    .blackboard {
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid #1a3a4a;
        border-radius: 12px;
        padding: 20px;
        margin: 20px;
        min-height: 400px;
        max-height: 70vh;
        overflow-y: auto;
        box-shadow: inset 0 0 50px rgba(0, 204, 255, 0.05);
    }
    
    .blackboard::-webkit-scrollbar {
        width: 8px;
    }
    
    .blackboard::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    .blackboard::-webkit-scrollbar-thumb {
        background: #00ccff;
        border-radius: 10px;
    }
    
    .blackboard::-webkit-scrollbar-thumb:hover {
        background: #00ffff;
    }
    
    .result-button {
        display: block;
        width: 100%;
        background: rgba(20, 30, 50, 0.8);
        border: 1px solid #003355;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #ffffff;
        text-align: right;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 15px;
        line-height: 1.6;
        word-wrap: break-word;
    }
    
    .result-button:hover {
        background: rgba(0, 100, 150, 0.6);
        border-color: #00ccff;
        box-shadow: 0 0 15px rgba(0, 204, 255, 0.3);
        transform: translateX(-5px);
    }
    
    .result-button-text {
        color: #ffffff;
        font-weight: 500;
    }
    
    .result-button-meta {
        color: #888888;
        font-size: 12px;
        margin-top: 8px;
    }
    
    .dialog-content {
        background: rgba(10, 14, 39, 0.95);
        border: 2px solid #00ccff;
        border-radius: 12px;
        padding: 25px;
        color: #ffffff;
    }
    
    .verse-preview {
        background: rgba(0, 204, 255, 0.1);
        border-right: 4px solid #00ccff;
        padding: 18px;
        border-radius: 8px;
        font-size: 18px;
        line-height: 2;
        margin: 15px 0;
        word-wrap: break-word;
    }
    
    .context-verse {
        background: rgba(0, 0, 0, 0.4);
        border-right: 3px solid #00ccff;
        padding: 12px;
        margin: 8px 0;
        border-radius: 6px;
        font-size: 15px;
        line-height: 1.8;
    }
    
    .context-verse-center {
        background: rgba(255, 51, 102, 0.15);
        border-right: 4px solid #ff3366;
        font-weight: bold;
    }
    
    .word-button {
        display: inline-block;
        background: rgba(100, 150, 200, 0.3);
        border: 1px solid #00ccff;
        border-radius: 20px;
        padding: 6px 12px;
        margin: 5px 5px 5px 0;
        color: #00ccff;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.3s ease;
    }
    
    .word-button:hover {
        background: rgba(0, 204, 255, 0.4);
        color: #ffffff;
        box-shadow: 0 0 10px rgba(0, 204, 255, 0.5);
    }
    
    .action-buttons {
        display: flex;
        gap: 10px;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    
    .stButton>button {
        background-color: #ff3366 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #ff1744 !important;
        box-shadow: 0 0 15px rgba(255, 51, 102, 0.5) !important;
    }
    
    .popover-button {
        background: rgba(0, 204, 255, 0.1);
        border: 1px solid #00ccff;
        color: #00ccff;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .popover-button:hover {
        background: rgba(0, 204, 255, 0.2);
        box-shadow: 0 0 10px rgba(0, 204, 255, 0.3);
    }
    
    .stat-badge {
        background: rgba(76, 175, 80, 0.2);
        border-left: 4px solid #4CAF50;
        padding: 12px;
        border-radius: 6px;
        margin: 10px 0;
        font-size: 14px;
    }
    
    .empty-state {
        text-align: center;
        padding: 50px 20px;
        color: #888888;
    }
    
    .empty-state-icon {
        font-size: 48px;
        margin-bottom: 20px;
    }
    
    h1, h2, h3 {
        color: #00ccff !important;
        text-shadow: 0 0 10px rgba(0, 204, 255, 0.3);
    }
    
    /* إخفاء العناصر غير الضرورية */
    [data-testid="stSidebar"] { display: none; }
    footer { display: none; }
    
    </style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 دوال مساعدة
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def normalize_arabic(text):
    """توحيد النصوص العربية"""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"[\u064B-\u0652]", "", text)
    text = re.sub(r"[إأآٱا]", "ا", text)
    text = re.sub(r"[ىي]", "ي", text)
    text = re.sub(r"[ةه]", "ه", text)
    return text.strip()

@st.cache_data
def load_quran_data():
    """تحميل بيانات القرآن"""
    for path in ["data/data_quran.xlsx", "data_quran.xlsx", "./data/data_quran.xlsx"]:
        if os.path.exists(path):
            return pd.read_excel(path)
    return None

@st.cache_data
def load_words_data():
    """تحميل بيانات الألفاظ"""
    for path in ["data/data_words.xlsx", "data_words.xlsx", "./data/data_words.xlsx"]:
        if os.path.exists(path):
            return pd.read_excel(path)
    return None

def identify_quran_columns(df):
    """تحديد أسماء الأعمدة"""
    cols = df.columns
    surah_col = next((c for c in cols if c in ['السورة', 'surah', 'Surah']), None)
    verse_col = next((c for c in cols if c in ['رقم الآية', 'verse_number', 'Verse', 'آية', 'v رقم الآية']), None)
    text_col = next((c for c in cols if c in ['نص الآية', 'text', 'Text', 'الآية']), None)
    return surah_col, verse_col, text_col

def identify_words_columns(df):
    """تحديد أعمدة ملف الألفاظ"""
    cols = df.columns
    word_col = next((c for c in cols if c in ['اللفظ', 'word', 'Word', 'الكلمة']), None)
    surah_col = next((c for c in cols if c in ['السورة', 'surah', 'Surah']), None)
    verse_col = next((c for c in cols if c in ['رقم الآية', 'verse_number', 'Verse', 'آية', 'r رقم الآية']), None)
    text_col = next((c for c in cols if c in ['نص الآية الكاملة', 'نص الآية', 'text', 'Text']), None)
    return word_col, surah_col, verse_col, text_col

def search_unified(df_quran, df_words, query, surah_col, verse_col, text_col, word_col_w=None):
    """بحث موحد (ألفاظ + سياق معاً)"""
    query_norm = normalize_arabic(query)
    if not query_norm:
        return []
    
    results = []
    
    # البحث في الآيات
    for idx, row in df_quran.iterrows():
        text_norm = normalize_arabic(str(row[text_col]))
        if query_norm in text_norm:
            results.append({
                'type': 'context',
                'surah': row[surah_col],
                'verse': int(row[verse_col]),
                'text': row[text_col],
                'idx': idx
            })
    
    # البحث في الألفاظ إذا كانت متوفرة
    if df_words is not None and word_col_w is not None:
        word_col_w, _, surah_col_w, verse_col_w, text_col_w = identify_words_columns(df_words)
        mask = df_words[word_col_w].apply(lambda x: query_norm in normalize_arabic(str(x)))
        for idx, (_, row) in enumerate(df_words[mask].iterrows()):
            results.append({
                'type': 'word',
                'surah': row[surah_col_w] if surah_col_w else "؟",
                'verse': int(row[verse_col_w]) if verse_col_w else 0,
                'text': row[text_col_w] if text_col_w else "نص غير متوفر",
                'idx': idx
            })
    
    # إزالة التكرارات
    seen = set()
    unique_results = []
    for r in results:
        key = (r['surah'], r['verse'])
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    return unique_results

def get_context(df, surah_col, verse_col, text_col, surah, verse, before, after):
    """الحصول على السياق"""
    start = max(1, verse - before)
    end = verse + after
    
    mask = (
        (df[surah_col] == surah) &
        (df[verse_col].astype(int).between(start, end))
    )
    
    context = []
    for _, row in df[mask].sort_values(verse_col).iterrows():
        v_num = int(row[verse_col])
        context.append({
            'verse': v_num,
            'text': row[text_col],
            'is_center': (v_num == verse)
        })
    
    return context

def save_result(query, surah, verse, text, context_verses):
    """حفظ النتيجة في ملف"""
    os.makedirs('data', exist_ok=True)
    
    filepath = 'data/مجلد_النتائج.txt'
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    entry = f"""
╔════════════════════════════════════════════════════════════════════════════╗
📍 الاستعلام: {query}
🕐 التاريخ والوقت: {timestamp}
╚════════════════════════════════════════════════════════════════════════════╝

السورة: {surah} | الآية: {verse}

📄 الآية المركزية:
{text}

📖 السياق الموسع:
"""
    
    for ctx in context_verses:
        marker = "⭐ " if ctx['is_center'] else "  "
        entry += f"{marker}[{ctx['verse']}] ﴿{ctx['text']}﴾\n"
    
    entry += "\n" + "─" * 80 + "\n\n"
    
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(entry)
        return True
    except Exception as e:
        st.error(f"❌ خطأ في الحفظ: {str(e)}")
        return False

def load_saved_results():
    """تحميل النتائج المحفوظة"""
    filepath = 'data/مجلد_النتائج.txt'
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return "لا توجد نتائج محفوظة بعد"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📱 تهيئة الجلسة
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if 'verses_before' not in st.session_state:
    st.session_state.verses_before = 2

if 'verses_after' not in st.session_state:
    st.session_state.verses_after = 2

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

if 'current_results' not in st.session_state:
    st.session_state.current_results = []

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# تحميل البيانات
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
df_quran = load_quran_data()
df_words = load_words_data()

if df_quran is None:
    st.error("❌ لم يتم العثور على ملف بيانات القرآن")
    st.stop()

surah_col, verse_col, text_col = identify_quran_columns(df_quran)

if not all([surah_col, verse_col, text_col]):
    st.error("❌ لم نتمكن من تحديد أعمدة بيانات القرآن")
    st.stop()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎯 شريط البحث العلوي مع الأيقونات
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

col_search_left, col_search_center, col_search_right = st.columns([1, 3, 1])

with col_search_left:
    with st.popover("⚙️ إعدادات"):
        st.markdown("<h4 style='color: #00ccff;'>⚙️ معايير السياق</h4>", unsafe_allow_html=True)
        st.session_state.verses_before = st.number_input(
            "آيات قبل:",
            min_value=1,
            max_value=20,
            value=st.session_state.verses_before
        )
        st.session_state.verses_after = st.number_input(
            "آيات بعد:",
            min_value=1,
            max_value=20,
            value=st.session_state.verses_after
        )
        st.markdown(f"""
            <div class='stat-badge'>
            📊 الإجمالي: {st.session_state.verses_before + st.session_state.verses_after + 1} آية
            </div>
        """, unsafe_allow_html=True)

with col_search_center:
    search_query = st.text_input(
        "🔍",
        placeholder="ابحث عن لفظ أو آية أو جملة...",
        label_visibility="collapsed",
        key="search_input"
    )
    st.session_state.search_query = search_query

with col_search_right:
    with st.popover("💾 النتائج"):
        st.markdown("<h4 style='color: #00ccff;'>📁 مجلد النتائج المحفوظة</h4>", unsafe_allow_html=True)
        saved_content = load_saved_results()
        st.text_area(
            "النتائج المحفوظة:",
            value=saved_content,
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )
        if st.button("🗑️ مسح جميع النتائج"):
            filepath = 'data/مجلد_النتائج.txt'
            if os.path.exists(filepath):
                os.remove(filepath)
                st.success("✅ تم مسح النتائج")
                st.rerun()

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🖤 السبورة السوداء الرئيسية
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if search_query:
    results = search_unified(
        df_quran, 
        df_words, 
        search_query,
        surah_col,
        verse_col,
        text_col
    )
    st.session_state.current_results = results
else:
    results = []

# عرض السبورة السوداء
st.markdown('<div class="blackboard">', unsafe_allow_html=True)

if not results:
    if search_query:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <p>لم يتم العثور على نتائج لـ: <strong>{}</strong></p>
                <p style="color: #666; font-size: 12px;">حاول بحثاً آخر</p>
            </div>
        """.format(search_query), unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📖</div>
                <p>ابدأ البحث في القرآن الكريم</p>
                <p style="color: #666; font-size: 12px;">أدخل كلمة أو آية في شريط البحث أعلاه</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown(f"<div class='stat-badge'>📊 {len(results)} نتيجة</div>", unsafe_allow_html=True)
    
    # عرض النتائج كأزرار
    for idx, result in enumerate(results):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            button_text = f"{result['text'][:70]}..." if len(result['text']) > 70 else result['text']
            meta_text = f"{result['surah']} : {result['verse']}"
            
            if st.button(
                f"📖 {button_text}\n{meta_text}",
                key=f"result_{idx}",
                use_container_width=True
            ):
                # فتح Dialog عند الضغط
                @st.dialog("📄 معاينة الآية والسياق", width="large")
                def show_verse_detail():
                    # معاينة الآية
                    st.markdown(f"<h4 style='color: #ff3366;'>📍 {result['surah']} : {result['verse']}</h4>", unsafe_allow_html=True)
                    
                    st.markdown(f"<div class='verse-preview'>{result['text']}</div>", unsafe_allow_html=True)
                    
                    # زر النسخ
                    st.code(result['text'], language=None)
                    
                    # السياق الموسع
                    context_verses = get_context(
                        df_quran,
                        surah_col,
                        verse_col,
                        text_col,
                        result['surah'],
                        result['verse'],
                        st.session_state.verses_before,
                        st.session_state.verses_after
                    )
                    
                    st.markdown(f"<h4 style='color: #00ccff;'>📖 السياق ({st.session_state.verses_before} قبل + 1 + {st.session_state.verses_after} بعد)</h4>", unsafe_allow_html=True)
                    
                    for ctx in context_verses:
                        if ctx['is_center']:
                            st.markdown(f"<div class='context-verse context-verse-center'>⭐ [{ctx['verse']}] ﴿{ctx['text']}﴾</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='context-verse'>[{ctx['verse']}] ﴿{ctx['text']}﴾</div>", unsafe_allow_html=True)
                    
                    # أزرار الكلمات المتقابلة
                    st.markdown("<h4 style='color: #00ccff;'>🔤 اضغط على كلمة للبحث عنها</h4>", unsafe_allow_html=True)
                    
                    words = result['text'].split()
                    cols = st.columns(len(words))
                    
                    for word_idx, (col, word) in enumerate(zip(cols, words)):
                        with col:
                            if st.button(
                                word[:15],
                                key=f"word_{idx}_{word_idx}",
                                use_container_width=True
                            ):
                                # Dialog متداخل للكلمة
                                @st.dialog("🔍 نتائج البحث عن اللفظ", width="large")
                                def show_word_results():
                                    word_results = search_unified(
                                        df_quran,
                                        df_words,
                                        word,
                                        surah_col,
                                        verse_col,
                                        text_col
                                    )
                                    
                                    st.markdown(f"<h4 style='color: #00ccff;'>🔍 البحث عن: {word}</h4>", unsafe_allow_html=True)
                                    st.markdown(f"<div class='stat-badge'>📊 {len(word_results)} نتيجة</div>", unsafe_allow_html=True)
                                    
                                    for w_result in word_results[:10]:  # أول 10 نتائج
                                        st.markdown(f"<div class='context-verse'>[{w_result['surah']}:{w_result['verse']}] ﴿{w_result['text'][:50]}...﴾</div>", unsafe_allow_html=True)
                                    
                                    if len(word_results) > 10:
                                        st.markdown(f"<div class='stat-badge'>... و {len(word_results) - 10} نتيجة أخرى</div>", unsafe_allow_html=True)
                                
                                show_word_results()
                    
                    # أزرار الحفظ والتحويل
                    st.divider()
                    col_save, col_close = st.columns(2)
                    
                    with col_save:
                        if st.button("💾 حفظ في النتائج", use_container_width=True):
                            if save_result(
                                st.session_state.search_query,
                                result['surah'],
                                result['verse'],
                                result['text'],
                                context_verses
                            ):
                                st.success("✅ تم الحفظ بنجاح!")
                    
                    with col_close:
                        if st.button("✖️ إغلاق", use_container_width=True):
                            st.rerun()
                
                show_verse_detail()

st.markdown('</div>', unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 الإحصائيات السفلية
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.divider()

col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.markdown(f"""
        <div class='stat-badge'>
        📖 إجمالي الآيات: {len(df_quran)}
        </div>
    """, unsafe_allow_html=True)

with col_stat2:
    if df_words is not None:
        st.markdown(f"""
            <div class='stat-badge'>
            🔤 الألفاظ المسجلة: {len(df_words)}
            </div>
        """, unsafe_allow_html=True)

with col_stat3:
    st.markdown(f"""
        <div class='stat-badge'>
        ⚙️ معايير السياق: {st.session_state.verses_before} - {st.session_state.verses_after}
        </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #00ccff; font-size: 12px; margin-top: 20px;'>🌟 مجلس البينة V3 - السبورة السوداء التفاعلية 🌟</p>", unsafe_allow_html=True)
