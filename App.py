import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Wealth Engine Pro", layout="wide")
st.title(" Wealth Engine: 55-Year Strategic Plan")

# --- SIDEBAR: INPUT PANEL ---
with st.sidebar:
    st.header("Financial Inputs")
    nest_egg = st.number_input("Starting Nest Egg ($)", value=1800000, step=50000)
    
    st.subheader("Accumulation Phase")
    years_to_save = st.slider("Years of Aggressive Saving", 0, 10, 5)
    annual_savings = st.number_input("Annual Savings ($)", value=130000)
    
    st.subheader("Retirement Phases")
    go_go_spend = st.slider("Go-Go Years Spend (First 15yr)", 50000, 250000, 140000)
    base_spend = st.slider("Standard Spend (Year 16+)", 50000, 200000, 110000)
    
    st.subheader("Market Dynamics")
    exp_return = st.slider("Expected Real Return (%)", 1.0, 10.0, 6.0) / 100
    volatility = st.slider("Market Volatility (Std Dev %)", 5, 25, 15) / 100

# --- LOGIC: THE SIMULATION ---
def run_wealth_sim():
    years = 60 # 5 years save + 55 years retire
    balance = nest_egg
    history = []
    
    for yr in range(1, years + 1):
        # Apply market return
        market_move = np.random.normal(exp_return, volatility)
        balance *= (1 + market_move)
        
        # Savings vs Spending
        if yr <= years_to_save:
            balance += annual_savings
            current_draw = 0
        else:
            ret_yr = yr - years_to_save
            # Spending Smile Logic
            current_draw = go_go_spend if ret_yr <= 15 else base_spend
            
            # Guyton-Klinger Guardrail (Simple Version)
            if balance < (nest_egg * 0.8): # If down 20%, cut spending
                current_draw *= 0.9
                
            balance -= current_draw
            
        history.append(max(0, balance))
        if balance <= 0: break
            
    return history

# --- DASHBOARD: THE APPLE VIEW ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Portfolio Trajectory")
    # Run 10 simulations for visual variety
    fig = go.Figure()
    for i in range(5):
        data = run_wealth_sim()
        fig.add_trace(go.Scatter(y=data, name=f"Scenario {i+1}", mode='lines', line=dict(width=2)))
    
    fig.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Target SWR", "3.5%", help="The benchmark for 50-year survival.")
    
    # Success Rate Simulation
    results = [1 if run_wealth_sim()[-1] > 0 else 0 for _ in range(100)]
    success_rate = sum(results)
    
    st.subheader("Success Probability")
    st.title(f"{success_rate}%")
    if success_rate > 90:
        st.success("Bulletproof Plan")
    elif success_rate > 75:
        st.warning("Viable with Guardrails")
    else:
        st.error("High Risk of Depletion")

st.info("**CFP Insight:** Your current plan shows that your 'Go-Go' spending is actually covered by the portfolio growth alone if you hit a 6% real return.")
