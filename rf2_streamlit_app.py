import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Near-term Decarbonsiation Targets for corporations: The need for Industry-specific Pathways",
    page_icon="🎯",
    layout="wide"
)

# Title and introduction
st.title("🎯 Industry-Specific Decarbonization Pathways: Why Sectoral Approaches Fail")
st.markdown("""
**Demonstrating Research Frontier 2: The critical need for industry-specific decarbonization blueprints**

Current climate frameworks assume that IPCC sectoral pathways can guide corporate decarbonization. 
But industries span multiple sectors with complex cross-dependencies that existing guidance cannot address.

*This analysis uses real CDP corporate disclosure data and IPCC AR6 cost assessments to demonstrate 
why current sectoral approaches are fundamentally inadequate for industry realities.*
""")

# Industry data based on actual CDP research with real IPCC cost ranges
industry_data = {
    'Food, Beverage & Tobacco': {
        'scope3_total_emissions': 67,  # % of total emissions that are Scope 3
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
        'scope3_total_emissions': 99.98,  # Extreme Scope 3 dominance
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

# IPCC sectoral cost data (from AR6 WGIII Chapter 12, Table 12.3)
ipcc_cost_data = {
    'AFOLU': {
        'description': 'Agriculture, Forestry, Other Land Use',
        'cost_ranges': {
            'Forest protection': '$0-20/tCO2e',
            'Soil carbon sequestration': '$20-50/tCO2e',
            'Agricultural CH4/N2O reduction': '$20-50/tCO2e',
            'Restoration': '$50-100/tCO2e'
        },
        'total_potential': '11.4 GtCO2-eq by 2030'
    },
    'Industry': {
        'description': 'Manufacturing, Processing, Materials',
        'cost_ranges': {
            'Energy efficiency': '$0-20/tCO2e',
            'Material efficiency': '$20-50/tCO2e',
            'Fuel switching': '$20-100/tCO2e',
            'CCS': '$100-200/tCO2e'
        },
        'total_potential': '5.4 GtCO2-eq by 2030'
    },
    'Transport': {
        'description': 'Logistics, Distribution, Mobility',
        'cost_ranges': {
            'Fuel efficiency': '$0-20/tCO2e',
            'Electric vehicles': 'Variable costs',
            'Modal shift': '$0-50/tCO2e',
            'Biofuels': '$50-100/tCO2e'
        },
        'total_potential': '3.8 GtCO2-eq by 2030'
    },
    'Buildings': {
        'description': 'Retail, Storage, Facilities',
        'cost_ranges': {
            'Energy efficiency': '$0-20/tCO2e',
            'Building performance': '$20-100/tCO2e',
            'Onsite renewables': '$20-50/tCO2e'
        },
        'total_potential': '2.0 GtCO2-eq by 2030'
    },
    'Power': {
        'description': 'Electricity Generation',
        'cost_ranges': {
            'Wind energy': 'Mostly <$0/tCO2e',
            'Solar energy': 'Mostly <$0/tCO2e',
            'Nuclear': '$0-50/tCO2e',
            'Hydropower': '$0-50/tCO2e'
        },
        'total_potential': '11.0 GtCO2-eq by 2030'
    }
}

# Sidebar for industry selection
st.sidebar.header("🏭 Select Industry for Analysis")
selected_industry = st.sidebar.selectbox(
    "Choose an industry to explore its cross-sectoral dependencies:",
    list(industry_data.keys()),
    help="Based on CDP's analysis of corporate disclosures and SBTi guidance coverage"
)

# Main dashboard layout
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader(f"📊 Cross-Sectoral Dependencies: {selected_industry}")
    
    # Create Sankey diagram
    data = industry_data[selected_industry]
    
    # Prepare data for Sankey
    sectors = list(data['sector_dependencies'].keys())
    industry_name = [selected_industry]
    
    # Create source (IPCC sectors) and target (industry) nodes
    all_nodes = sectors + industry_name
    
    # Prepare links
    source_indices = []
    target_indices = []
    values = []
    colors = []
    hover_texts = []
    
    for i, (sector, details) in enumerate(data['sector_dependencies'].items()):
        source_indices.append(i)  # sector index
        target_indices.append(len(sectors))  # industry index
        values.append(details['percentage'])
        colors.append(details['color'])
        
        # Create hover text with detailed information
        hover_text = f"""
        <b>{sector} → {selected_industry}</b><br>
        Materiality: {details['percentage']}% of Scope 3 emissions<br>
        Scope 3 Category: {details['scope3_category']}<br>
        SBTi Guidance: {details['guidance']}<br>
        IPCC Cost Range: {details['cost_range']}<br>
        <extra></extra>
        """
        hover_texts.append(hover_text)
    
    # Create Sankey diagram
    fig_sankey = go.Figure(data=[go.Sankey(
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
            hovertemplate='%{customdata}<extra></extra>',
            customdata=hover_texts
        )
    )])
    
    fig_sankey.update_layout(
        title=f"Cross-Sectoral Dependencies (CDP 2021 Data)",
        font_size=12,
        height=400,
        annotations=[
            dict(
                text="<b>Left:</b> IPCC Sectors with Pathways<br><b>Right:</b> Industry Reality<br><b>Flows:</b> Actual CDP Materiality Data",
                showarrow=False,
                x=0.5, y=-0.1,
                xref="paper", yref="paper",
                font=dict(size=10)
            )
        ]
    )
    
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    # Guidance coverage summary
    st.markdown("### 📋 Guidance Coverage Analysis")
    
    guidance_summary = []
    for sector, details in data['sector_dependencies'].items():
        guidance_summary.append({
            'IPCC Sector': sector,
            'Materiality (% Scope 3)': f"{details['percentage']}%",
            'SBTi Guidance': details['guidance'],
            'IPCC Cost Range': details['cost_range'],
            'Status': '✅' if details['guidance'] == 'Available' else '⚠️' if 'Generic' in details['guidance'] or 'Recent' in details['guidance'] else '❌'
        })
    
    guidance_df = pd.DataFrame(guidance_summary)
    st.dataframe(guidance_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("🎯 The Guidance Inadequacy Problem")
    
    # Calculate guidance gaps
    total_coverage = sum([
        details['percentage'] for sector, details in data['sector_dependencies'].items() 
        if details['guidance'] == 'Available'
    ])
    
    gap_coverage = 100 - total_coverage
    
    # Create pie chart showing guidance gaps
    coverage_data = pd.DataFrame({
        'Category': ['Has Industry-Specific Guidance', 'Guidance Gap'],
        'Percentage': [total_coverage, gap_coverage],
        'Color': ['#4CAF50', '#F44336']
    })
    
    fig_pie = px.pie(
        coverage_data, 
        values='Percentage', 
        names='Category',
        color='Category',
        color_discrete_map={'Has Industry-Specific Guidance': '#4CAF50', 'Guidance Gap': '#F44336'},
        title=f"{selected_industry} Guidance Coverage"
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=300, showlegend=False)
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Key insights
    st.markdown(f"""
    **Key Challenge:**
    {data['key_challenge']}
    
    **Sample Size:** {data['cdp_sample_size']} companies (CDP 2021)
    
    **Main Gap:** {data['main_gap']}
    """)

# IPCC Cost Analysis Section
st.subheader("💰 IPCC AR6 Cross-Sectoral Cost Analysis")

st.markdown("""
**Source:** IPCC AR6 WGIII Chapter 12, Table 12.3 - "Overview of global net GHG emissions reduction potentials"

The challenge isn't just missing guidance—it's cost uncertainty across value chains.
""")

# Create cost comparison visualization
cost_tab1, cost_tab2 = st.tabs(["📊 Cost Ranges by Sector", "🎮 Investment Complexity Simulator"])

with cost_tab1:
    # Display IPCC cost data
    st.markdown("### IPCC AR6 Sectoral Mitigation Costs (2030)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost ranges table
        cost_summary = []
        for sector, data in ipcc_cost_data.items():
            for intervention, cost in data['cost_ranges'].items():
                cost_summary.append({
                    'IPCC Sector': sector,
                    'Intervention': intervention,
                    'Cost Range': cost,
                    'Potential': data['total_potential']
                })
        
        cost_df = pd.DataFrame(cost_summary)
        st.dataframe(cost_df, use_container_width=True, hide_index=True)
    
    with col2:
        # Sector potential visualization
        sector_potentials = [float(data['total_potential'].split()[0]) for data in ipcc_cost_data.values()]
        sector_names = list(ipcc_cost_data.keys())
        
        fig_potential = px.bar(
            x=sector_potentials,
            y=sector_names,
            orientation='h',
            title="IPCC AR6 Sectoral Mitigation Potential (2030)",
            labels={'x': 'Potential (GtCO2-eq)', 'y': 'IPCC Sector'},
            color=sector_potentials,
            color_continuous_scale='Viridis'
        )
        fig_potential.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_potential, use_container_width=True)

with cost_tab2:
    st.markdown("### Investment Complexity Demonstration")
    
    selected_data = industry_data[selected_industry]
    
    st.markdown(f"""
    **Scenario:** A {selected_industry} company with $10M decarbonization budget needs to optimize 
    across {len(selected_data['sector_dependencies'])} different sectoral pathways with varying costs and uncertainties.
    """)
    
    # Create cost uncertainty visualization
    fig_uncertainty = go.Figure()
    
    y_pos = 0
    for sector, details in selected_data['sector_dependencies'].items():
        # Extract cost range
        cost_range = details['cost_range']
        materiality = details['percentage']
        
        # Simple cost parsing (could be enhanced)
        if '$' in cost_range and '-' in cost_range:
            try:
                costs = cost_range.replace('$', '').replace('/tCO2e', '').split('-')
                min_cost = float(costs[0])
                max_cost = float(costs[1])
            except:
                min_cost, max_cost = 20, 100  # default for non-parseable ranges
        else:
            min_cost, max_cost = 20, 100
        
        # Add uncertainty bar
        fig_uncertainty.add_trace(go.Scatter(
            x=[min_cost, max_cost],
            y=[y_pos, y_pos],
            mode='lines+markers',
            name=sector,
            line=dict(width=8),
            marker=dict(size=12),
            hovertemplate=f"""
            <b>{sector}</b><br>
            Materiality: {materiality}% of Scope 3<br>
            Cost Range: {cost_range}<br>
            Guidance: {details['guidance']}<br>
            <extra></extra>
            """
        ))
        
        # Add materiality indicator
        fig_uncertainty.add_annotation(
            x=max_cost + 10,
            y=y_pos,
            text=f"{materiality}%",
            showarrow=False,
            font=dict(size=10)
        )
        
        y_pos += 1
    
    fig_uncertainty.update_layout(
        title="Cost Uncertainty vs. Emission Materiality",
        xaxis_title="Cost Range ($/tCO2e)",
        yaxis_title="Sectoral Dependencies",
        yaxis=dict(tickvals=list(range(len(selected_data['sector_dependencies']))), 
                   ticktext=list(selected_data['sector_dependencies'].keys())),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_uncertainty, use_container_width=True)
    
    st.markdown("""
    **The Investment Dilemma:**
    - Target lowest-cost options? → Miss material emission sources
    - Target highest-materiality? → Face extreme cost uncertainty  
    - Current guidance provides no framework for optimization
    """)

# Key insights and conclusions
st.subheader("🔑 Why Current Approaches Fail")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.markdown("""
    ### 🎯 Materiality Mismatch
    
    Industries span multiple IPCC sectors with vastly different:
    - **Cost ranges** ($0-200/tCO2e variation)
    - **Guidance availability** (✅❌⚠️ mix)
    - **Technical readiness** (decades to years)
    """)

with insight_col2:
    st.markdown("""
    ### 📊 Cross-Sectoral Complexity
    
    Current sectoral pathways assume:
    - **Single-sector focus** 
    - **Uniform cost assumptions**
    - **Independent optimization**
    
    Reality: **Complex interdependencies**
    """)

with insight_col3:
    st.markdown("""
    ### 🚀 The RF2 Solution
    
    **Industry-Specific Blueprints** that integrate:
    - ✅ Cross-sectoral materiality mapping
    - ✅ Dynamic cost modeling  
    - ✅ Technology readiness assessment
    - ✅ Investment optimization frameworks
    """)

# Scientific evidence section
st.subheader("📚 Scientific Evidence Base")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Key Research Supporting This Analysis:**
    
    1. **CDP Technical Note (2022)**: "Relevance of Scope 3 Categories by Sector"
       - Real materiality data from 1,000+ companies
       - Industry-specific emission hotspot identification
    
    2. **IPCC AR6 WGIII Chapter 12 (2022)**: "Cross-sectoral Perspectives"  
       - Authoritative sectoral cost assessments
       - Technology readiness evaluations
    
    3. **SBTi Scope 3 Review (2023)**: "Catalyzing Value Chain Decarbonization"
       - 85% of companies cite methodology gaps
       - Industry-specific guidance limitations
    """)

with col2:
    st.markdown("""
    **Data Sources:**
    
    - **Industry Dependencies**: CDP NZDPU database (2021)
    - **Cost Ranges**: IPCC AR6 WGIII Table 12.3
    - **Guidance Coverage**: SBTi methodology database
    - **Sample Sizes**: 162-376 companies per sector
    
    **Key Findings:**
    - >32 GtCO2-eq mitigation potential by 2030
    - 50%+ potential available at <$20/tCO2e
    - But optimization requires industry-specific frameworks
    """)

# Call to action
st.subheader("🎯 The Research Frontier 2 Case")

st.markdown("""
### This Analysis Demonstrates:

1. **Problem Scale**: Even industries with some guidance (like F&B with FLAG) face 60%+ emission sources without pathways
2. **Cost Complexity**: $0-200/tCO2e ranges across value chains create optimization impossibility  
3. **Investment Paralysis**: Companies lack frameworks to balance cost-effectiveness with materiality
4. **Scientific Gap**: Current sectoral approaches weren't designed for industry-specific complexities

### The Solution: Industry-Specific Decarbonization Blueprints

**RF2 research framework** translates IPCC sectoral pathways into actionable industry strategies through:
- **Materiality-weighted pathway integration**
- **Dynamic cost modeling with uncertainty quantification**  
- **Technology readiness-adjusted timelines**
- **Cross-sectoral optimization algorithms**

**Next Steps**: This complexity isn't a limitation—it's the research opportunity that RF2 addresses.
Systematic development of industry-specific blueprints can transform corporate climate action from 
fragmented compliance to strategic decarbonization aligned with planetary boundaries.
""")

# Footer with citations
st.markdown("---")
st.markdown("""
**Methodology Note**: This simulator demonstrates the problem complexity that necessitates RF2 research. 
It is based on the perspective research artcile titled "Operationalizing corporate climate action through five research frontiers" 
submitted to Nature Sustainability and uses real corporate disclosure data to highlight 
the urgent need for industry-specific decarbonization blueprints.

**Citation**: CDP (2022). Technical Note: Relevance of Scope 3 Categories by Sector. 
IPCC (2022). Climate Change 2022: Mitigation of Climate Change, Chapter 12: Cross-sectoral Perspectives.
""")
