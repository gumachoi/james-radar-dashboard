import streamlit as st
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="JamesRadarBot 뉴스 대시보드", 
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터 폴더 경로 설정
DATA_DIR = Path("data")
ARTICLES_FILE = DATA_DIR / "articles.json"
UPDATE_FILE = DATA_DIR / "latest_update.json"

# 데이터 폴더가 없으면 생성
DATA_DIR.mkdir(exist_ok=True)

@st.cache_data(ttl=60)  # 1분마다 캐시 갱신
def load_articles_data():
    """JSON 파일에서 기사 데이터 로드"""
    try:
        if ARTICLES_FILE.exists():
            with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 파일이 없으면 샘플 데이터 반환
            return get_sample_data()
    except Exception as e:
        st.error(f"데이터 로드 중 오류: {e}")
        return get_sample_data()

@st.cache_data(ttl=60)
def load_update_info():
    """업데이트 정보 로드"""
    try:
        if UPDATE_FILE.exists():
            with open(UPDATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "last_update": datetime.now().isoformat(),
                "total_articles_today": 0,
                "status": "샘플 데이터"
            }
    except Exception as e:
        return {
            "last_update": datetime.now().isoformat(),
            "total_articles_today": 0,
            "status": f"오류: {e}"
        }

def get_sample_data():
    """샘플 데이터 반환 (n8n 연동 전 테스트용)"""
    return {
        "articles": [
            {
                "id": "20250813-001",
                "title": "유영상 SKT 대표 '고객 최우선·AI·보안 강화로 신뢰받는 통신사 구축'",
                "source": "디지털데일리",
                "date": "2025-08-13 11:25",
                "summary": "SKT 유영상 대표가 고객 최우선 정책과 AI 기술 강화, 보안 체계 구축을 통해 신뢰받는 통신사로 거듭나겠다고 밝혔습니다. 특히 생성형 AI 서비스 확대와 개인정보 보호 강화에 집중할 예정입니다.",
                "originalUrl": "https://news.google.com/rss/articles/CBMiZEFVX3lxTE9fSjJHNVBEWkVteU9SUVNBeS1oM09hYjZYODRod3RMUkt4QUdpeGVUY3ROajJmMUQ2ZGV3SE90Q0UxOXRaT3RGYUJoRjFFOGhtTHE4U3ZIYnVxVEROUTNMWUtDcG8?oc=5",
                "similarArticles": [
                    {"source": "위키리크스한국", "count": 1},
                    {"source": "글로벌이코노믹", "count": 1},
                    {"source": "네이트", "count": 3},
                    {"source": "Chosun Biz", "count": 1}
                ],
                "comments": {
                    "total": 247,
                    "positive": 45,
                    "negative": 35,
                    "neutral": 167,
                    "top_reactions": [
                        "AI 발전은 좋지만 보안이 더 중요",
                        "SKT 주가 상승 기대",
                        "구체적인 계획이 궁금"
                    ]
                },
                "aiInsight": "이번 발표는 SKT가 최근 보안 이슈 이후 신뢰 회복을 위한 종합적인 전략을 제시한 것으로 보입니다. AI 기술 강화와 보안 체계 구축을 동시에 추진하는 것은 통신사의 디지털 전환 트렌드에 부합하는 전략입니다.",
                "keywords": ["SKT", "AI", "보안", "통신사", "디지털전환"],
                "keyword_counts": [15, 12, 8, 6, 4]
            },
            {
                "id": "20250813-002", 
                "title": "'비상경영 끝'…SKT, AI 전략 전방위 드라이브",
                "source": "위키리크스한국",
                "date": "2025-08-13 08:59",
                "summary": "SKT가 비상경영 체제를 종료하고 AI 전략을 본격적으로 추진한다고 발표했습니다. 전사적 AI 도입과 새로운 수익 모델 창출에 집중할 계획입니다.",
                "originalUrl": "https://news.google.com/rss/articles/CBMib0FVX3lxTE5TYVFMSmR3TVE2YUNXaXRyMTFKZjAxSnN5WWdQVHQ2eXhmSEpDaEdCU3QyM25sOC1zZWlxRXFBaUJUSHpVdC1LN1lWOVZQVE55UmhOa3paYTE0TmpzbEd4d2xpb254SWdpamNhVGxNMA?oc=5",
                "similarArticles": [
                    {"source": "테크노아", "count": 1},
                    {"source": "민주신문", "count": 1}
                ],
                "comments": {
                    "total": 156,
                    "positive": 89,
                    "negative": 23,
                    "neutral": 44,
                    "top_reactions": [
                        "드디어 정상화되는구나",
                        "AI 투자 확대 좋은 신호",
                        "실적 개선 기대"
                    ]
                },
                "aiInsight": "비상경영 종료는 SKT의 재정 안정화가 완료되었음을 시사합니다. AI 전략 집중은 향후 성장 동력 확보를 위한 필수적 선택으로 평가됩니다.",
                "keywords": ["SKT", "비상경영", "AI전략", "수익모델"],
                "keyword_counts": [18, 10, 9, 5]
            }
        ]
    }

# CSS 스타일링 - 전문적이고 미니멀한 디자인
st.markdown("""
<style>
    /* 전체 앱 스타일 */
    .stApp {
        background-color: #fafafa;
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background-color: #ffffff;
        border-right: 1px solid #e0e4e7;
    }
    
    /* 메인 헤더 */
    .main-header {
        background-color: #ffffff;
        border: 1px solid #e0e4e7;
        padding: 2rem 1.5rem;
        margin-bottom: 2rem;
        border-radius: 8px;
    }
    
    .main-header h1 {
        color: #1a1a1a;
        font-size: 2rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: #6b7280;
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    
    /* 기사 카드 */
    .article-card {
        background: #ffffff;
        border: 1px solid #e0e4e7;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .article-title {
        color: #1a1a1a;
        font-size: 1.25rem;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: 1rem;
    }
    
    .article-meta {
        color: #6b7280;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }
    
    /* 메트릭 카드 */
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* 인사이트 박스 */
    .insight-box {
        background: #1e293b;
        color: #f1f5f9;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .insight-box h4 {
        color: #f1f5f9;
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    
    /* 섹션 헤더 */
    .section-header {
        color: #374151;
        font-size: 1.125rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    /* 메트릭 스타일 */
    .metric-container {
        background: #ffffff;
        border: 1px solid #e0e4e7;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin: 0;
    }
    
    /* 댓글 리스트 */
    .comment-item {
        background: #f8fafc;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 3px solid #3b82f6;
        font-size: 0.875rem;
        color: #374151;
    }
    
    /* 차트 컨테이너 */
    .chart-container {
        background: #ffffff;
        border: 1px solid #e0e4e7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="main-header">
    <h1>JamesRadarBot</h1>
    <p>실시간 뉴스 모니터링 & 분석 대시보드</p>
</div>
""", unsafe_allow_html=True)

# 실시간 데이터 새로고침 버튼
if st.button("🔄 데이터 새로고침", help="최신 뉴스 데이터를 불러옵니다"):
    st.cache_data.clear()
    st.rerun()

# 데이터 로드
articles_data = load_articles_data()
update_info = load_update_info()

# URL 파라미터 처리 (텔레그램 링크에서 사용)
query_params = st.query_params
selected_article_id = query_params.get("article", None)

# 🆕 URL에서 직접 기사 정보 받기
url_title = query_params.get("title", None)
url_source = query_params.get("source", None) 
url_link = query_params.get("url", None)
url_date = query_params.get("date", None)

# URL에서 기사 정보가 온 경우 동적으로 생성
if url_title and url_source and url_link and selected_article_id:
    # 동적 기사 데이터 생성
    dynamic_article = {
        "id": selected_article_id,
        "title": url_title,
        "source": url_source,
        "date": url_date or datetime.now().strftime("%Y-%m-%d %H:%M"),
        "summary": f"'{url_title}' 기사에 대한 AI 분석을 진행하고 있습니다. 원문을 확인하여 자세한 내용을 확인해주세요.",
        "originalUrl": url_link,
        "similarArticles": [
            {"source": "기타 언론사", "count": 1}
        ],
        "comments": {
            "total": 150,
            "positive": 65,
            "negative": 25,
            "neutral": 60,
            "top_reactions": [
                "실시간 뉴스 분석 중입니다",
                "상세 분석은 잠시 후 업데이트됩니다",
                "원문을 확인해주세요"
            ]
        },
        "aiInsight": f"실시간으로 전달된 '{url_source}' 뉴스입니다. James 관련 키워드가 감지되어 알림이 발송되었습니다. 상세 분석은 잠시 후 업데이트됩니다.",
        "keywords": ["James", "실시간", "뉴스"],
        "keyword_counts": [5, 3, 2]
    }
    
    # 기존 데이터에 추가
    if "articles" not in articles_data:
        articles_data["articles"] = []
    
    # 동적 기사를 맨 앞에 추가
    articles_data["articles"].insert(0, dynamic_article)
    
    # 성공 메시지 표시
    st.info(f"📰 실시간 뉴스 분석: {url_title[:50]}...")
    
    # 선택된 기사를 동적 기사로 설정
    selected_article = dynamic_article

# 사이드바
with st.sidebar:
    st.markdown('<h2 style="color: #374151; font-weight: 600; margin-bottom: 1.5rem;">기사 목록</h2>', unsafe_allow_html=True)
    
    # 상태 표시
    last_update = datetime.fromisoformat(update_info["last_update"].replace("Z", "+00:00"))
    time_diff = datetime.now() - last_update.replace(tzinfo=None)
    
    if time_diff.total_seconds() < 300:  # 5분 이내
        status_color = "#10b981"
        status_text = "🟢 실시간"
    elif time_diff.total_seconds() < 1800:  # 30분 이내  
        status_color = "#f59e0b"
        status_text = "🟡 지연"
    else:
        status_color = "#ef4444"
        status_text = "🔴 오프라인"
    
    st.markdown(f"""
    <div style="background: #f8fafc; padding: 0.75rem; border-radius: 6px; margin-bottom: 1rem;">
        <div style="color: {status_color}; font-weight: 600; font-size: 0.875rem;">{status_text}</div>
        <div style="color: #6b7280; font-size: 0.75rem;">
            {last_update.strftime("%H:%M")} 업데이트
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 날짜 필터
    st.markdown('<div class="section-header">날짜 필터</div>', unsafe_allow_html=True)
    date_filter = st.date_input("", datetime.now().date(), label_visibility="collapsed")
    
    # 통계 요약
    total_articles = len(articles_data.get("articles", []))
    st.markdown(f"""
    <div class="metric-container">
        <p class="metric-value">{total_articles}</p>
        <p class="metric-label">오늘의 기사</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-container">
        <p class="metric-value">{update_info.get('total_articles_today', 0)}</p>
        <p class="metric-label">누적 처리</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 기사 목록
    st.markdown('<div class="section-header">최근 기사</div>', unsafe_allow_html=True)
    
    article_options = {}
    for article in articles_data.get("articles", []):
        display_text = f"{article['source']} • {article['title'][:40]}..."
        article_options[display_text] = article["id"]
    
    if not article_options:
        st.info("아직 기사가 없습니다. n8n에서 데이터를 확인해주세요.")
        st.stop()
    
    # 선택된 기사가 있으면 기본값으로 설정
    default_idx = 0
    if selected_article_id:
        for idx, (_, article_id) in enumerate(article_options.items()):
            if article_id == selected_article_id:
                default_idx = idx
                break
    
    selected_display = st.selectbox(
        "",
        list(article_options.keys()),
        index=default_idx,
        label_visibility="collapsed"
    )
    
    selected_article_id = article_options[selected_display]

# 선택된 기사 데이터 가져오기
selected_article = None
for article in articles_data.get("articles", []):
    if article["id"] == selected_article_id:
        selected_article = article
        break

if selected_article:
    # 메인 컨텐츠 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 기사 정보
        st.markdown('<div class="section-header">기사 정보</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="article-card">
            <div class="article-title">{selected_article['title']}</div>
            <div class="article-meta">출처: {selected_article['source']} • {selected_article['date']}</div>
            <div class="article-meta"><a href="{selected_article['originalUrl']}" target="_blank" style="color: #3b82f6; text-decoration: none;">원문 보기 →</a></div>
        </div>
        """, unsafe_allow_html=True)
        
        # 기사 요약
        st.markdown('<div class="section-header">AI 요약</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card">
            {selected_article['summary']}
        </div>
        """, unsafe_allow_html=True)
        
        # 주요 반응
        st.markdown('<div class="section-header">댓글 분석</div>', unsafe_allow_html=True)
        
        # 댓글 감정 분석 차트
        sentiment_data = {
            "감정": ["긍정", "부정", "중립"],
            "개수": [
                selected_article['comments']['positive'],
                selected_article['comments']['negative'], 
                selected_article['comments']['neutral']
            ]
        }
        
        fig_sentiment = px.pie(
            values=sentiment_data["개수"],
            names=sentiment_data["감정"],
            title="",
            color_discrete_map={
                "긍정": "#10b981",
                "부정": "#ef4444", 
                "중립": "#8b5cf6"
            },
            hole=0.4
        )
        fig_sentiment.update_layout(
            showlegend=True,
            height=300,
            margin=dict(t=20, b=20, l=20, r=20),
            font=dict(size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig_sentiment.update_traces(textposition='inside', textinfo='percent+label')
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_sentiment, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 주요 댓글 반응
        st.markdown("**주요 반응**")
        for reaction in selected_article['comments']['top_reactions']:
            st.markdown(f'<div class="comment-item">{reaction}</div>', unsafe_allow_html=True)
    
    with col2:
        # 보도 현황
        st.markdown('<div class="section-header">보도 현황</div>', unsafe_allow_html=True)
        
        # 총 보도 건수
        total_similar = sum([item['count'] for item in selected_article['similarArticles']])
        st.markdown(f"""
        <div class="metric-container">
            <p class="metric-value">{total_similar}</p>
            <p class="metric-label">유사 기사</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-container">
            <p class="metric-value">{selected_article['comments']['total']}</p>
            <p class="metric-label">총 댓글</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 언론사별 보도 현황
        similar_df = pd.DataFrame(selected_article['similarArticles'])
        
        fig_similar = px.bar(
            similar_df,
            x='count',
            y='source',
            orientation='h',
            title="",
            color='count',
            color_continuous_scale=['#e2e8f0', '#475569']
        )
        fig_similar.update_layout(
            height=250,
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=11)
        )
        fig_similar.update_xaxes(showgrid=False)
        fig_similar.update_yaxes(showgrid=False)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_similar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # AI 인사이트
        st.markdown('<div class="section-header">AI 인사이트</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="insight-box">
            <h4>분석 결과</h4>
            <p>{selected_article['aiInsight']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 키워드 분석
        st.markdown('<div class="section-header">주요 키워드</div>', unsafe_allow_html=True)
        
        # 키워드 데이터가 있는 경우에만 표시
        if 'keywords' in selected_article and 'keyword_counts' in selected_article:
            keywords = selected_article['keywords']
            keyword_counts = selected_article['keyword_counts']
        else:
            # 기본 키워드 (샘플)
            keywords = ["SKT", "AI", "보안", "통신사", "디지털전환"]
            keyword_counts = [15, 12, 8, 6, 4]
        
        fig_keywords = go.Figure(data=[go.Bar(
            x=keywords,
            y=keyword_counts,
            marker_color='#64748b'
        )])
        fig_keywords.update_layout(
            title="",
            height=200,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=11)
        )
        fig_keywords.update_xaxes(showgrid=False)
        fig_keywords.update_yaxes(showgrid=False)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_keywords, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9ca3af; font-size: 0.875rem; padding: 1rem 0;'>
    마지막 업데이트: {} • JamesRadarBot 24/7 모니터링
</div>
""".format(datetime.now().strftime("%Y.%m.%d %H:%M")), unsafe_allow_html=True)

# 개발자 노트 (하단에 숨김)
with st.expander("🔧 개발자 설정"):
    st.json({
        "데이터 파일": str(ARTICLES_FILE),
        "업데이트 파일": str(UPDATE_FILE),
        "현재 기사 수": len(articles_data.get("articles", [])),
        "마지막 업데이트": update_info.get("last_update"),
        "선택된 기사 ID": selected_article_id
    })
