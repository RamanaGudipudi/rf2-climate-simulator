"""
The Need for Industry-Specific Pathways
========================================

Demonstrating Research Frontier 2: Why sectoral approaches fail for industry realities

This app uses real CDP corporate disclosure data and IPCC AR6 cost assessments to show
why current sectoral pathways cannot adequately guide industry-specific decarbonization.

Data: CDP (2021) - 900+ companies across 5 industries
Cost Ranges: IPCC AR6 WGIII Chapter 12
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Industry-Specific Pathways",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - MATCHING RF1 STYLE
# ============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #58a6ff;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #79c0ff;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #58a6ff;
        padding-bottom: 0.5rem;
    }
    
    .info-box {
        background-color: rgba(56, 139, 253, 0.1);
        border-left: 4px solid #58a6ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: rgba(187, 128, 9, 0.15);
        border-left: 4px solid #d29922;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: rgba(46, 160, 67, 0.15);
        border-left: 4px solid #3fb950;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: rgba(248, 81, 73, 0.15);
        border-left: 4px solid #f85149;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .key-finding {
        background-color: rgba(139, 92, 246, 0.1);
        border: 2px solid #a371f7;
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin: 1.5rem 0;
        font-size: 1.1rem;
    }
    
    .data-card {
        background-color: rgba(110, 118, 129, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #30363d;
        margin: 0.5rem 0;
    }
    
    .highlight {
        color: #f85149;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA: INDUSTRY DEPENDENCIES (CDP 2021)
# ============================================================================

industry_data = {
    'Food, Beverage & Tobacco': {
        'scope3_total_emissions': 67,
        'sector_dependencies': {
            'AFOLU': {'percentage': 40, 'guidance': 'Available', 'cost_range': '$0-50/tCO2e', 'scope3_category': 'C1: Purchased goods (agricultural)', 'color': '#2E7D32'},
            'Industry': {'percentage': 20, 'guidance': 'Limited', 'cost_range': '$20-100/tCO2e', 'scope3_category': 'C1: Purchased goods (packaging)', 'color': '#FF5722'},
            'Transport': {'percentage': 15, 'guidance': 'Generic only', 'cost_range': '$0-50/tCO2e', 'scope3_category': 'C4+C9: Transport', 'color': '#FF9800'},
            'Buildings': {'percentage': 10, 'guidance': 'None', 'cost_range': '$20-100/tCO2e', 'scope3_category': 'C13: Retail/storage', 'color': '#F44336'},
            'Power': {'percentage': 15, 'guidance': 'Available', 'cost_range': '$0-20/tCO2e', 'scope3_category': 'C2: Processing facilities', 'color': '#2E7D32'}
        },
        'key_challenge': 'Even with FLAG guidance, 60% of F&B emissions lack industry-specific pathways',
        'cdp_sample_size': 162,
        'main_gap': 'No methodology for packaging, retail, and processing dependencies'
    },
    'Transport OEMs': {
        'scope3_total_emissions': 84,
        'sector_dependencies': {
            'Industry': {'percentage': 11, 'guidance': 'Generic only', 'cost_range': '$20-100/tCO2e', 'scope3_category': 'C1: Manufacturing', 'color': '#FF9800'},
            'Transport': {'percentage': 86, 'guidance': 'Recent (2024)', 'cost_range': '$0-50/tCO2e', 'scope3_category': 'C11: Use phase', 'color': '#4CAF50'},
            'Power': {'percentage': 3, 'guidance': 'Available', 'cost_range': '$0-20/tCO2e', 'scope3_category': 'C2: Manufacturing facilities', 'color': '#2E7D32'}
        },
        'key_challenge': 'New Land Transport guidance covers use-phase, but manufacturing gaps remain',
        'cdp_sample_size': 48,
        'main_gap': 'No methodology linking automotive supply chain complexity to science-based targets'
    },
    'Capital Goods': {
        'scope3_total_emissions': 90,
        'sector_dependencies': {
            'Industry': {'percentage': 6, 'guidance': 'Generic only', 'cost_range': '$20-100/tCO2e', 'scope3_category': 'C1: Manufacturing', 'color': '#FF9800'},
            'Multiple_Enduse': {'percentage': 91, 'guidance': 'None', 'cost_range': '$50-200/tCO2e', 'scope3_category': 'C11: Use across all sectors', 'color': '#F44336'},
            'Power': {'percentage': 3, 'guidance': 'Available', 'cost_range': '$0-20/tCO2e', 'scope3_category': 'C2: Manufacturing', 'color': '#2E7D32'}
        },
        'key_challenge': '91% of emissions have no methodology to link equipment efficiency to sectoral pathways',
        'cdp_sample_size': 166,
        'main_gap': 'No framework for translating product improvements into science-based targets'
    },
    'Financial Services': {
        'scope3_total_emissions': 99.98,
        'sector_dependencies': {
            'All_Sectors_via_Investments': {'percentage': 99, 'guidance': 'PCAF available', 'cost_range': 'Variable by sector', 'scope3_category': 'C15: Financed emissions', 'color': '#9C27B0'},
            'Buildings': {'percentage': 1, 'guidance': 'Available', 'cost_range': '$0-50/tCO2e', 'scope3_category': 'C13: Real estate portfolio', 'color': '#2E7D32'}
        },
        'key_challenge': 'Portfolio emissions span ALL sectors but no methodology links PCAF to sectoral pathways',
        'cdp_sample_size': 377,
        'main_gap': 'Financed emissions 700x larger than direct, but sectoral investment optimization lacks science-based framework'
    },
    'Chemicals': {
        'scope3_total_emissions': 44,
        'sector_dependencies': {
            'Industry': {'percentage': 58, 'guidance': 'Limited', 'cost_range': '$20-100/tCO2e', 'scope3_category': 'C1: Raw materials', 'color': '#FF5722'},
            'Multiple_Downstream': {'percentage': 19, 'guidance': 'None', 'cost_range': '$50-200/tCO2e', 'scope3_category': 'C11: Use in other industries', 'color': '#F44336'},
            'Transport': {'percentage': 12, 'guidance': 'Generic only', 'cost_range': '$0-50/tCO2e', 'scope3_category': 'C4+C9: Transport', 'color': '#FF9800'},
            'Power': {'percentage': 8, 'guidance': 'Available', 'cost_range': '$0-20/tCO2e', 'scope3_category': 'C2: Production facilities', 'color': '#2E7D32'},
            'Buildings': {'percentage': 3, 'guidance': 'Limited', 'cost_range': '$100-200/tCO2e', 'scope3_category': 'C12: End-of-life', 'color': '#FF5722'}
        },
        'key_challenge': 'Intermediate products create unknown downstream use-phase across multiple industries',
        'cdp_sample_size': 146,
        'main_gap': 'No methodology for tracking chemical products through complex multi-industry value chains'
    }
}

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_sankey_diagram(industry_name, data):
    """Create Sankey diagram showing sectoral dependencies"""
    sectors = list(data['sector_dependencies'].keys())
    all_nodes = sectors + [industry_name]
    
    source_indices = []
    target_indices = []
    values = []
    colors = []
    hover_texts = []
    
    for i, (sector, details) in enumerate(data['sector_dependencies'].items()):
        source_indices.append(i)
        target_indices.append(len(sectors))
        values.append(details['percentage'])
        colors.append(details['color'])
        
        hover_text = f"<b>{sector} → {industry_name}</b><br>Materiality: {details['percentage']}% of Scope 3<br>Scope 3 Category: {details['scope3_category']}<br>SBTi Guidance: {details['guidance']}<br>IPCC Cost: {details['cost_range']}<extra></extra>"
        hover_texts.append(hover_text)
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color=["lightblue"] * len(sectors) + ["darkblue"]
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=[f"rgba{tuple(list(px.colors.hex_to_rgb(color)) + [0.7])}" for color in colors],
            customdata=hover_texts,
            hovertemplate='%{customdata}'
        )
    )])
    
    fig.update_layout(
        title=f"Cross-Sectoral Dependencies: {industry_name}",
        font_size=12,
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_hotspot_chart(data):
    """Create bar chart showing materiality hotspots >20%"""
    hotspots = [(sector, details['percentage']) for sector, details in data['sector_dependencies'].items() if details['percentage'] >= 20]
    
    if not hotspots:
        hotspots = sorted([(sector, details['percentage']) for sector, details in data['sector_dependencies'].items()], key=lambda x: x[1], reverse=True)[:3]
    
    sectors, percentages = zip(*hotspots)
    
    fig = go.Figure(data=[
        go.Bar(
            y=sectors,
            x=percentages,
            orientation='h',
            marker_color='#58a6ff',
            text=percentages,
            texttemplate='%{text}%',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Materiality Hotspots (>20% of Scope 3)",
        xaxis_title="% of Total Scope 3 Emissions",
        yaxis_title="",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c9d1d9')
    )
    
    return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # ========================================================================
    # SIDEBAR NAVIGATION
    # ========================================================================
    
    with st.sidebar:
        st.markdown("## 📍 Navigation")
        st.markdown("---")
        
        st.markdown("""
        <style>
        .nav-link-button {
            display: block;
            padding: 0.6rem 1rem;
            margin: 0.3rem 0;
            border-radius: 0.5rem;
            background-color: rgba(110, 118, 129, 0.1);
            color: inherit;
            text-decoration: none;
            border: 1px solid #30363d;
            text-align: center;
            transition: all 0.2s ease;
        }
        .nav-link-button:hover {
            background-color: rgba(151, 166, 195, 0.15);
            border-color: #4a9eff;
            text-decoration: none;
            color: inherit;
        }
        </style>
        
        <a href="#intro" class="nav-link-button">🏠 Introduction</a>
        <a href="#industry" class="nav-link-button">🏭 Industry Analysis</a>
        <a href="#costs" class="nav-link-button">💰 Cost Challenge</a>
        <a href="#conclusions" class="nav-link-button">💡 Conclusions</a>
        <a href="#references" class="nav-link-button">📚 References</a>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Industry selector
        st.markdown("## 🏭 Select Industry")
        selected_industry = st.selectbox(
            "Choose industry to analyze:",
            list(industry_data.keys()),
            help="Based on CDP 2021 corporate disclosure data"
        )
        
        st.markdown("---")
        
        # Quick stats
        data = industry_data[selected_industry]
        st.markdown(f"""
        <div style="font-size: 0.9rem; line-height: 1.8;">
        <b>📊 {selected_industry}</b><br>
        • Scope 3: {data['scope3_total_emissions']}%<br>
        • Sectors: {len(data['sector_dependencies'])}<br>
        • CDP Sample: {data['cdp_sample_size']} companies<br>
        <br>
        <b>📄 Paper Status</b><br>
        Under review at<br>
        <i>Nature Sustainability</i>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # MAIN HEADER
    # ========================================================================
    
    st.markdown('<h1 class="main-header">🏭 The Need for Industry-Specific Pathways</h1>', unsafe_allow_html=True)
    
    # ========================================================================
    # INTRODUCTION
    # ========================================================================
    
    st.markdown('<h2 id="intro">🏠 Introduction</h2>', unsafe_allow_html=True)
    
    st.markdown("### The Sectoral Pathway Assumption")
    
    # Metric cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Industries Analyzed", "5", help="Major industries from CDP data")
    with col2:
        avg_scope3 = np.mean([d['scope3_total_emissions'] for d in industry_data.values()])
        st.metric("Avg Scope 3", f"{avg_scope3:.0f}%", help="Average Scope 3 as % of total emissions")
    with col3:
        avg_sectors = np.mean([len(d['sector_dependencies']) for d in industry_data.values()])
        st.metric("Avg Sectors/Industry", f"{avg_sectors:.1f}", help="Average IPCC sectors per industry")
    with col4:
        total_companies = sum([d['cdp_sample_size'] for d in industry_data.values()])
        st.metric("CDP Sample", f"{total_companies}", help="Total companies analyzed")
    
    st.markdown("""
    Current climate frameworks assume **IPCC sectoral pathways** can guide corporate decarbonization. 
    But industries don't operate within single sectors—they span multiple sectors with complex 
    cross-dependencies that existing guidance cannot address.
    """)
    
    # Visual comparison
    st.markdown("### The Reality Gap")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: rgba(63, 185, 80, 0.15); padding: 1.5rem; border-radius: 0.8rem; border-left: 4px solid #3fb950;">
        <h4 style="color: #3fb950; margin-top: 0;">📚 IPCC Sectoral Pathways</h4>
        <ul style="font-size: 1.05rem; line-height: 1.8;">
        <li>Sector-specific guidance</li>
        <li>Single-sector focus</li>
        <li>Standardized cost ranges</li>
        <li><b>Designed for national inventories</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: rgba(248, 81, 73, 0.15); padding: 1.5rem; border-radius: 0.8rem; border-left: 4px solid #f85149;">
        <h4 style="color: #f85149; margin-top: 0;">🏭 Industry Reality</h4>
        <ul style="font-size: 1.05rem; line-height: 1.8;">
        <li>Multi-sectoral dependencies</li>
        <li>Complex value chains</li>
        <li>Varying cost structures</li>
        <li><b>Need industry-specific frameworks</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # The key question
    st.markdown("""
    <div class="key-finding">
    <h3 style="margin-top: 0; color: #a371f7;">🎯 The Central Question</h3>
    <p style="font-size: 1.2rem;">
    Can IPCC sectoral pathways adequately guide industry-specific corporate decarbonization?
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # INDUSTRY ANALYSIS
    # ========================================================================
    
    st.markdown('<h2 id="industry">🏭 Industry Analysis: Cross-Sectoral Dependencies</h2>', unsafe_allow_html=True)
    
    st.info(f"💡 **Analyzing**: {selected_industry} based on CDP 2021 disclosure data from {industry_data[selected_industry]['cdp_sample_size']} companies")
    
    data = industry_data[selected_industry]
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📊 Full Dependency Map", "🎯 Materiality Hotspots", "📋 Guidance Coverage"])
    
    with tab1:
        st.markdown("#### Cross-Sectoral Dependencies")
        
        with st.spinner("Generating Sankey diagram..."):
            fig_sankey = create_sankey_diagram(selected_industry, data)
            st.plotly_chart(fig_sankey, use_container_width=True)
        
        st.caption("**Left**: IPCC Sectors | **Right**: Industry Reality | **Flows**: CDP Materiality Data (%)")
        
        st.markdown("""
        <div class="info-box">
        <b>💡 What This Shows</b><br>
        Industries don't fit neatly into IPCC sectors. Each flow represents a different sectoral dependency,
        each with its own cost structure, guidance availability, and technical readiness.
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### Key Emission Hotspots")
        
        fig_hotspots = create_hotspot_chart(data)
        st.plotly_chart(fig_hotspots, use_container_width=True)
        
        st.markdown(f"""
        <div class="success-box">
        <b>✅ Key Insight</b><br>
        <b>{data['key_challenge']}</b>
        <br><br>
        These hotspots represent where industry-specific guidance is most urgently needed, but current
        sectoral pathways provide inadequate coverage.
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### SBTi Guidance Coverage Analysis")
        
        guidance_summary = []
        for sector, details in data['sector_dependencies'].items():
            guidance_summary.append({
                'IPCC Sector': sector,
                'Materiality (%)': details['percentage'],
                'SBTi Guidance': details['guidance'],
                'IPCC Cost Range': details['cost_range'],
                'Status': '✅' if details['guidance'] == 'Available' else '⚠️' if 'Generic' in details['guidance'] or 'Recent' in details['guidance'] else '❌'
            })
        
        guidance_df = pd.DataFrame(guidance_summary)
        guidance_df = guidance_df.sort_values('Materiality (%)', ascending=False)
        st.dataframe(guidance_df, use_container_width=True, hide_index=True)
        
        # Calculate coverage
        total_coverage = sum([
            details['percentage'] for sector, details in data['sector_dependencies'].items() 
            if details['guidance'] == 'Available'
        ])
        
        st.markdown(f"""
        <div class="error-box">
        <b>⚠️ Coverage Gap</b><br>
        Only <b>{total_coverage:.0f}%</b> of this industry's Scope 3 emissions have adequate guidance.<br>
        <b>{100 - total_coverage:.0f}%</b> lack industry-specific methodologies.
        <br><br>
        <b>Main Gap</b>: {data['main_gap']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # COST CHALLENGE
    # ========================================================================
    
    st.markdown('<h2 id="costs">💰 The Cost Challenge</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    Beyond guidance gaps, industries face **cost uncertainty** across their value chains. IPCC sectoral 
    cost ranges vary from **$0-200/tCO2e**, creating optimization impossibility without industry-specific frameworks.
    """)
    
    # Create cost uncertainty visualization
    st.markdown(f"### Cost Uncertainty: {selected_industry}")
    
    fig_cost = go.Figure()
    
    y_pos = 0
    for sector, details in data['sector_dependencies'].items():
        cost_range = details['cost_range']
        materiality = details['percentage']
        
        # Parse cost range
        if '$' in cost_range and '-' in cost_range:
            try:
                costs = cost_range.replace('$', '').replace('/tCO2e', '').split('-')
                min_cost = float(costs[0])
                max_cost = float(costs[1])
            except:
                min_cost, max_cost = 20, 100
        else:
            min_cost, max_cost = 20, 100
        
        # Add range bar
        fig_cost.add_trace(go.Scatter(
            x=[min_cost, max_cost],
            y=[y_pos, y_pos],
            mode='lines+markers',
            name=sector,
            line=dict(width=8),
            marker=dict(size=12),
            hovertemplate=f"<b>{sector}</b><br>Materiality: {materiality}%<br>Cost: {cost_range}<br>Guidance: {details['guidance']}<extra></extra>"
        ))
        
        # Add materiality label
        fig_cost.add_annotation(
            x=max_cost + 10,
            y=y_pos,
            text=f"{materiality}%",
            showarrow=False,
            font=dict(size=10, color='#c9d1d9')
        )
        
        y_pos += 1
    
    fig_cost.update_layout(
        title="Cost Ranges vs. Emission Materiality",
        xaxis_title="Cost Range ($/tCO2e)",
        yaxis=dict(
            tickvals=list(range(len(data['sector_dependencies']))),
            ticktext=list(data['sector_dependencies'].keys())
        ),
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c9d1d9')
    )
    
    st.plotly_chart(fig_cost, use_container_width=True)
    
    st.markdown("""
    <div class="warning-box">
    <b>💡 The Investment Dilemma</b><br><br>
    <b>Target lowest-cost options?</b> → Miss material emission sources<br>
    <b>Target highest-materiality?</b> → Face extreme cost uncertainty<br>
    <b>Current sectoral guidance?</b> → Provides no optimization framework<br>
    <br>
    <b>Result</b>: Companies cannot make informed investment decisions without industry-specific cost modeling.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # CONCLUSIONS
    # ========================================================================
    
    st.markdown('<h2 id="conclusions">💡 Conclusions: Why Industry-Specific Pathways Matter</h2>', unsafe_allow_html=True)
    
    st.markdown("### What We Found")
    
    st.markdown("""
    <div class="key-finding">
    <b>Three Fundamental Gaps in Current Sectoral Approaches:</b><br><br>
    
    <b>1. Multi-Sectoral Reality</b>: Industries span 3-5 IPCC sectors on average, but guidance assumes single-sector focus<br>
    <b>2. Guidance Inadequacy</b>: 40-90% of industry emissions lack sector-specific methodologies<br>
    <b>3. Cost Optimization Impossibility</b>: $0-200/tCO2e ranges across value chains prevent informed investment
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Why This Matters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="data-card">
        <b>🎯 For Companies</b><br><br>
        Cannot translate sectoral pathways into actionable strategies without 
        industry-specific blueprints integrating cross-sectoral dependencies.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="data-card">
        <b>📊 For Standard-Setters</b><br><br>
        Current SBTi guidance leaves 50%+ of corporate emissions without 
        credible methodologies for science-based target setting.
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="data-card">
        <b>💰 For Investors</b><br><br>
        Cannot assess credibility of corporate climate strategies without 
        industry-specific frameworks to evaluate decarbonization plans.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### The Path Forward: Research Frontier 2")
    
    st.markdown("""
    This analysis demonstrates why **industry-specific decarbonization blueprints** are essential. 
    Current sectoral approaches weren't designed for industry complexities and cannot adequately guide 
    corporate climate action.
    
    **What's Needed**:
    - **Materiality-weighted pathway integration** across multiple IPCC sectors
    - **Dynamic cost modeling** with uncertainty quantification
    - **Cross-sectoral optimization frameworks** for investment prioritization
    - **Technology readiness-adjusted timelines** for industry realities
    
    **RF2 Research Priority**: Systematic development of these industry-specific blueprints can transform 
    corporate climate action from fragmented compliance to strategic decarbonization aligned with 
    planetary boundaries.
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # REFERENCES
    # ========================================================================
    
    st.markdown('<h2 id="references">📚 References & Data Sources</h2>', unsafe_allow_html=True)
    
    with st.expander("📊 Data Sources"):
        st.markdown("""
        ### Primary Data
        
        **CDP (2022)**. *Technical Note: Relevance of Scope 3 Categories by Sector*  
        - Real materiality data from 900+ companies across 5 industries
        - Industry-specific emission hotspot identification
        - Source: CDP NZDPU database (2021 disclosure year)
        
        **IPCC AR6 WGIII Chapter 12 (2022)**. *Cross-sectoral Perspectives*  
        - Authoritative sectoral cost assessments (Table 12.3)
        - Mitigation potential by sector (2030)
        - Technology readiness evaluations
        
        **SBTi (2024)**. *Sector Guidance Database*  
        - Coverage assessment across industries
        - Methodology gap identification
        """)
    
    with st.expander("🔬 Methodology"):
        st.markdown("""
        ### Analysis Approach
        
        **Industry Selection**: Based on CDP disclosure volume and Scope 3 materiality
        
        **Sectoral Mapping**: Cross-reference CDP Scope 3 categories to IPCC sectors
        
        **Guidance Coverage**: Assessment of SBTi methodology availability by sector
        
        **Cost Ranges**: IPCC AR6 WGIII sectoral cost estimates
        
        **Sample Sizes**:
        - Food, Beverage & Tobacco: 162 companies
        - Transport OEMs: 48 companies
        - Capital Goods: 166 companies
        - Financial Services: 377 companies
        - Chemicals: 146 companies
        """)
    
    with st.expander("✍️ How to Cite"):
        st.markdown("""
        ### Paper Information
        
        **Title**: *Operationalizing corporate climate action through five research frontiers*  
        **Status**: Under review at *Nature Sustainability*  
        **Research Frontier 2**: Industry-specific decarbonization pathways
        
        ### Citation
        
        ```
        [Authors]. (2026). Operationalizing corporate climate action through 
        five research frontiers. Manuscript under review at Nature Sustainability.
        ```
        """)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #8b949e; padding: 2rem;">
    <p><b>The Need for Industry-Specific Pathways</b></p>
    <p>Part of <i>"Operationalizing corporate climate action through five research frontiers"</i></p>
    <p>Under review at <i>Nature Sustainability</i></p>
    <br>
    <p style="font-size: 0.9rem;">
    Research Frontier 2 Demonstration | Last updated: February 2026
    </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
