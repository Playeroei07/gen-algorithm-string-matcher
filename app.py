import streamlit as st
import pandas as pd
import time

# Import core GA functions from genetic_algorithm.py
from genetic_algorithm import run_ga_experiment

# Set up page configurations
st.set_page_config(
    page_title="Genetic Algorithm Grid Search Visualizer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for a dark-mode dashboard look and interactive buttons
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stButton>button {
        width: 100%;
        background-color: #4f46e5;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 0;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Main Title and Description
st.title("🧬 Genetic Algorithm Grid Search Visualizer")
st.write("Find the optimal hyperparameter configurations (Population Size & Mutation Rate) to match the target word using dynamic visualizations.")

# ==========================================
# SIDEBAR - GRID SEARCH CONFIGURATIONS
# ==========================================
st.sidebar.header("⚙️ Grid Search Parameters")

# Target word input
target_word = st.sidebar.text_input("Target Word (Letters Only):", value="PRABOWO").upper()

# Mutation Rate search options
mut_rate_options = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
selected_mut_rates = st.sidebar.multiselect(
    "Mutation Rates to Test:",
    options=mut_rate_options,
    default=[0.1, 0.2, 0.3]
)

# Population Size search options
pop_sizes_options = list(range(50, 1050, 50))
selected_pop_sizes = st.sidebar.multiselect(
    "Population Sizes to Test:",
    options=pop_sizes_options,
    default=[50, 100, 200, 300, 400, 500]
)

# Crossover Probability & Max Generations sliders
crossover_prob = st.sidebar.slider("Crossover Probability:", 0.1, 1.0, 0.9, step=0.05)
max_gens = st.sidebar.slider("Max Generations Limit:", 50, 1000, 500, step=50)

# Input Validation
run_allowed = True
if not target_word.isalpha():
    st.sidebar.error("⚠️ Target word must only contain letters (A-Z) with no spaces, numbers, or symbols!")
    run_allowed = False

if len(selected_mut_rates) == 0 or len(selected_pop_sizes) == 0:
    st.sidebar.warning("⚠️ Select at least one Mutation Rate and one Population Size to test!")
    run_allowed = False

# Execution button
start_search = st.sidebar.button("Run 🚀")

# ==========================================
# MAIN PAGE - EXECUTION FLOW & RESULTS
# ==========================================
if start_search and run_allowed:
    target_num = [ord(c) - 64 for c in target_word]
    total_experiments = len(selected_pop_sizes) * len(selected_mut_rates)
    
    st.subheader(f"Running Experiment Matrix for Target: `{target_word}`")
    st.write(f"Total Scenarios to Run: **{total_experiments} Combinations**")
    
    # Progress trackers
    progress_bar = st.progress(0.0)
    status_placeholder = st.empty()
    
    experiment_results = []
    
    # Execution Loop
    current_run = 0
    for pop in selected_pop_sizes:
        for mut in selected_mut_rates:
            current_run += 1
            # Update live run information
            status_placeholder.info(
                f"Running Experiment {current_run}/{total_experiments} | "
                f"Pop Size: **{pop}** | Mutation Rate: **{mut}**"
            )
            progress_bar.progress(current_run / total_experiments)
            
            # Execute Genetic Algorithm run
            generations_needed, word_log = run_ga_experiment(
                pop_size=pop,
                mut_rate=mut,
                target_num=target_num,
                crossover_probability=crossover_prob,
                max_generations=max_gens
            )
            
            # Record results
            experiment_results.append({
                'Population Size': pop,
                'Mutation Rate': mut,
                'Generations': generations_needed,
                'history': word_log
            })
            
            # Brief sleep for UI responsiveness
            time.sleep(0.01)
            
    # Clean up status widgets
    status_placeholder.empty()
    progress_bar.empty()
    st.success("🎉 **Grid Search Complete!** All parameter combinations have been successfully tested.")
    
    # Find the winning scenario (fewest generations)
    best_result = min(experiment_results, key=lambda x: x['Generations'])
    
    # ------------------------------------------
    # DISPLAY WINNING SCENARIO METRICS
    # ------------------------------------------
    st.write("## 🏆 Best Parameter Scenario")
    col1, col2, col3 = st.columns(3)
    col1.metric("Best Population Size", f"{best_result['Population Size']}")
    col2.metric("Best Mutation Rate", f"{best_result['Mutation Rate']}")
    col3.metric("Min Generations", f"{best_result['Generations']} gen")
    
    # ------------------------------------------
    # VISUAL COMPARISON CHARTS
    # ------------------------------------------
    st.write("## 📈 Parameter Performance Analysis")
    df = pd.DataFrame(experiment_results)
    
    # Pivot results: Index=Population Size, Columns=Mutation Rate, Values=Generations
    df_pivot = df.pivot(index='Population Size', columns='Mutation Rate', values='Generations')
    
    # Display the comparison chart
    st.write("### Evolution Speed Comparison (Lower is Better)")
    
    # We use Altair here instead of st.line_chart to customize the tooltip names
    import altair as alt
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Population Size:Q', title='Population Size'),
        y=alt.Y('Generations:Q', title='Generations Needed'),
        color=alt.Color('Mutation Rate:N', title='Mutation Rate'),
        tooltip=[
            alt.Tooltip('Population Size:Q', title='Population Size'),
            alt.Tooltip('Mutation Rate:N', title='Mutation Rate'),
            alt.Tooltip('Generations:Q', title='Generations Needed')
        ]
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    # Data Table Expander
    with st.expander("View Complete Experiment Results Table", expanded=False):
        st.dataframe(
            df[['Population Size', 'Mutation Rate', 'Generations']].sort_values(by='Generations'),
            use_container_width=True
        )
        
    # ------------------------------------------
    # BEST RUN EVOLUTION LOGS
    # ------------------------------------------
    st.write("## 📜 Evolution Process of the Best Scenario")
    best_out_title = f"Best Run Log (Pop: {best_result['Population Size']}, Mut: {best_result['Mutation Rate']})"
    with st.expander(best_out_title, expanded=True):
        log_text = "\n".join(best_result['history'])
        st.code(log_text, language="text")
else:
    # Landing page state
    st.info("👈 Set the target word and search space in the sidebar, then click **Run Grid Search** to begin the visual analysis.")
