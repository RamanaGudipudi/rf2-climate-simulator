import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="RF2: Why One-Size-Fits-All Climate Targets Fail",
    page_icon="🎯",
    layout="wide"
)

# Title and introduction
st.title("🎯 Why One-Size-Fits-All Climate Targets Fail")
st.markdown("""
**Exploring Research Frontier 2: The need for industry-specific decarbonization pathways**

Current climate frameworks apply uniform reduction targets across all industries. 
But does a 4.2% annual reduction mean the same thing for a tech company versus a food manufacturer?

*This simulator demonstrates the complexity that necessitates scientific research for industry-specific blueprints.*
""")

# Industry data based on the research paper
industry_data = {
    'Food & Beverage': {
        'scope1_2': 15,
        'scope3': 85,
        'main_scope3_sources': ['Agricultural production (40%)', 'Packaging (20%)', 'Transport (15%)', 'Processing (10%)'],
        'control_level': 'Low',
        'current_guidance': 'Partial (Agriculture only)',
        'key_challenges': [
            'Multi-sectoral value chain dependencies',
            'Limited supplier control in agriculture',
            'No guidance for packaging emissions',
            'Seasonal variation in agricultural outputs'
        ],
        'abatement_cost_range': '$80-200/tCO2e',
        'color': '#2E8B57'
    },
    'Technology': {
        'scope1_2': 20,
        'scope3': 80,
        'main_scope3_sources': ['Manufacturing (50%)', 'Product use (25%)', 'Transport (15%)', 'End-of-life (10%)'],
        'control_level': 'Medium',
        'current_guidance': 'Limited',
        'key_challenges': [
            'Outsourced manufacturing in complex supply chains',
            'Rapid product lifecycle changes',
            'Consumer behavior dependency',
            'Global supply chain coordination'
        ],
        'abatement_cost_range': '$30-120/tCO2e',
        'color': '#4169E1'
    },
    'Heavy Manufacturing': {
        'scope1_2': 70,
        'scope3': 30,
        'main_scope3_sources': ['Raw materials (20%)', 'Transport (5%)', 'Energy (3%)', 'Waste (2%)'],
        'control_level': 'High',
        'current_guidance': 'Available (SDA method)',
        'key_challenges': [
            'High capital intensity of equipment',
            'Technology readiness limitations',
            'Process heat requirements',
            'Asset stranding risks'
        ],
        'abatement_cost_range': '$100-500/tCO2e',
        'color': '#DC143C'
    }
}

# Sidebar for industry selection
st.sidebar.header("🏭 Select Industry")
selected_industry = st.sidebar.selectbox(
    "Choose an industry to explore:",
    list(industry_data.keys())
)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📊 {selected_industry} Emission Profile")
    
    # Create emission breakdown chart
    data = industry_data[selected_industry]
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Scope 1 & 2', 'Scope 3'],
        values=[data['scope1_2'], data['scope3']],
        hole=0.4,
        marker_colors=[data['color'], '#lightgray']
    )])
    
    fig_pie.update_layout(
        title="Emission Sources Breakdown",
        height=300,
        showlegend=True
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Key characteristics
    st.markdown(f"""
    **Key Characteristics:**
    - **Control Level**: {data['control_level']}
    - **Current SBTi Guidance**: {data['current_guidance']}
    - **Abatement Costs**: {data['abatement_cost_range']}
    """)

with col2:
    st.subheader("🎯 The Universal Target Challenge")
    
    # Show the uniform target application
    st.markdown("""
    **Current Approach**: All industries must achieve **4.2% annual emission reduction**
    
    But what does this mean in practice?
    """)
    
    # Create a challenge visualization
    challenges = data['key_challenges']
    
    st.markdown("**Major Implementation Challenges:**")
    for i, challenge in enumerate(challenges, 1):
        st.markdown(f"{i}. {challenge}")

# Scope 3 breakdown section
st.subheader(f"🔍 {selected_industry} Scope 3 Emission Sources")

scope3_sources = data['main_scope3_sources']
# Extract percentages and labels for visualization
sources_data = []
for source in scope3_sources:
    if '(' in source and ')' in source:
        label = source.split('(')[0].strip()
        percentage = int(source.split('(')[1].split('%')[0])
        sources_data.append({'Source': label, 'Percentage': percentage})

sources_df = pd.DataFrame(sources_data)

fig_bar = px.bar(
    sources_df, 
    x='Percentage', 
    y='Source',
    orientation='h',
    color='Percentage',
    color_continuous_scale='Viridis',
    title=f"Scope 3 Emission Breakdown - {selected_industry}"
)

fig_bar.update_layout(
    height=400,
    xaxis_title="Percentage of Total Scope 3 Emissions",
    yaxis_title="Emission Source"
)

st.plotly_chart(fig_bar, use_container_width=True)

# Industry comparison section
st.subheader("⚖️ Cross-Industry Comparison")

# Create comparison data
comparison_data = []
for industry, data in industry_data.items():
    comparison_data.append({
        'Industry': industry,
        'Scope 3 %': data['scope3'],
        'Control Level': data['control_level'],
        'Current Guidance': data['current_guidance'],
        'Cost Range': data['abatement_cost_range']
    })

comparison_df = pd.DataFrame(comparison_data)

col1, col2 = st.columns([1, 1])

with col1:
    # Scope 3 comparison
    fig_comparison = px.bar(
        comparison_df,
        x='Industry',
        y='Scope 3 %',
        color='Industry',
        title="Scope 3 Emission Intensity by Industry",
        color_discrete_sequence=['#2E8B57', '#4169E1', '#DC143C']
    )
    fig_comparison.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_comparison, use_container_width=True)

with col2:
    # Control level and guidance matrix
    st.markdown("**Industry Characteristics Matrix**")
    st.dataframe(
        comparison_df[['Industry', 'Control Level', 'Current Guidance', 'Cost Range']],
        use_container_width=True,
        hide_index=True
    )

# Cost sensitivity demonstration
st.subheader("💰 Cost Sensitivity Analysis")

st.markdown("""
**The Problem**: Abatement costs vary dramatically across industries and interventions, 
but current frameworks don't account for these economic realities.
""")

# Create cost sensitivity simulation
cost_factors = {
    'Carbon Price ($/tCO2e)': [50, 100, 150],
    'Technology Learning Rate (% cost reduction/year)': [5, 15, 25],
    'Policy Timeline (years until full implementation)': [2, 4, 6]
}

col1, col2, col3 = st.columns(3)

with col1:
    carbon_price = st.slider("Carbon Price ($/tCO2e)", 50, 150, 100, 25)

with col2:
    tech_learning = st.slider("Technology Learning Rate (%/year)", 5, 25, 15, 5)

with col3:
    policy_timeline = st.slider("Policy Timeline (years)", 2, 6, 4, 1)

# Calculate impact on feasibility (simplified model)
base_cost = 100  # Base abatement cost
policy_factor = 1 + (6 - policy_timeline) * 0.1  # Urgency increases costs
tech_factor = 1 - (tech_learning / 100) * 2  # Learning reduces costs
carbon_factor = carbon_price / 100  # Carbon price makes investments more attractive

adjusted_cost = base_cost * policy_factor * tech_factor / carbon_factor

# Color code feasibility
if adjusted_cost < 80:
    feasibility_color = "green"
    feasibility_text = "Highly Feasible"
elif adjusted_cost < 120:
    feasibility_color = "orange"
    feasibility_text = "Moderately Feasible"
else:
    feasibility_color = "red"
    feasibility_text = "Challenging"

st.markdown(f"""
**Adjusted Abatement Cost**: ${adjusted_cost:.0f}/tCO2e  
**Economic Feasibility**: <span style="color: {feasibility_color};">**{feasibility_text}**</span>

*This demonstrates how external factors create uncertainty in corporate decarbonization investments.*
""", unsafe_allow_html=True)

# Key insights and call to action
st.subheader("🔑 Key Insights")

st.markdown("""
### Why Current Approaches Fall Short:

1. **Materiality Mismatch**: Industries have vastly different emission profiles and control levels
2. **Guidance Gaps**: Most Scope 3 emissions lack industry-specific methodological support
3. **Cost Variability**: Abatement costs vary by 10x across sectors and interventions
4. **Dynamic Complexity**: External factors create massive uncertainty in investment decisions

### The Research Frontier 2 Solution:

**Industry-Specific Decarbonization Blueprints** that integrate:
- ✅ Bottom-up industry value chain mapping
- ✅ Dynamic cost modeling with uncertainty ranges  
- ✅ Technology readiness assessments
- ✅ Cross-sectoral dependency analysis
""")

# References section
st.subheader("📚 Scientific Evidence")

st.markdown("""
**Key Research Supporting This Analysis:**

1. **Reisinger et al. (2024)**: "Science-based targets miss the mark" - *Nature Communications*
2. **Bjørn et al. (2023)**: "Increased transparency needed for corporate science-based targets" - *Nature Climate Change*
3. **Buck et al. (2023)**: "Why residual emissions matter right now" - *Nature Climate Change*
4. **Yang et al. (2025)**: "Net-zero greenhouse gas mitigation potential across multi-tier supply chains" - *Communications Earth & Environment*

*This simulator is based on research from "Operationalizing corporate climate action through five research frontiers" - demonstrating the urgent need for RF2 scientific assessment.*
""")

# Footer
st.markdown("---")
st.markdown("""
**Next Steps**: This complexity isn't a bug—it's a feature of real-world decarbonization. 
We need scientific research to develop industry-specific blueprints that translate climate science into actionable corporate strategies.

*Interested in RF2 research? Connect with the research team developing these frameworks.*
""")
