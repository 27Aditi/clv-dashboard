import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title = "Customer Lifetime Value Dashboard",
    page_icon = "💰",
    layout = "wide"
)

st.markdown("""
<style>
    /* Import Space Grotesk Font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Apply Space Grotesk to all elements */
    html, body, [class*="css"], * {
        font-family: 'Space Grotesk', sans-serif !important;
    } 
            
    /* Change the selected option text color */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        color: #000000 !important;
    }
    
    /* Change placeholder text color */
    [data-testid="stSelectbox"] input::placeholder {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)


st.title("💰 Customer Lifetime Value Analysis")
st.caption("Understand customer value, segments and revenue contribution")

@st.cache_data
def load_data():
    customerdf = pd.read_parquet('processed_data/customer_wise.parquet')
    segmentdf = pd.read_parquet('processed_data/segment_wise.parquet')
    segmentdf.reset_index(inplace = True)
    return customerdf, segmentdf

customerdf, segmentdf = load_data()

customerdf['Year'] = customerdf['LastPurchaseDate'].apply(lambda x : '2009-10' if x.year in [2009,2010] else '2011-12')

# NUMBER OF CUSTOMERS
ppl_2009 = customerdf.loc[customerdf['Year'] == '2009-10'].shape[0]
ppl_2011 = customerdf[customerdf['Year'] == '2011-12'].shape[0]
delta1 = ((ppl_2011 - ppl_2009) / ppl_2009) * 100
totalppl = customerdf.shape[0]

# TOTAL CLV
totalclv_2009 = customerdf[customerdf['Year'] == '2009-10']['TotalCLV'].sum()
totalclv_2011 = customerdf[customerdf['Year'] == '2011-12']['TotalCLV'].sum()
delta2 = ((totalclv_2011 - totalclv_2009) / totalclv_2009) * 100
totalclv = customerdf['TotalCLV'].sum()

# AVERAGE CLV
avgclv_2009 = totalclv_2009 / ppl_2009
avgclv_2011 = totalclv_2011 / ppl_2011
delta3 = ((avgclv_2011 - avgclv_2009) / avgclv_2009) * 100
avgclv = totalclv / totalppl 

# AVERAGE FREQUENCY
freq_2009 = customerdf[customerdf['Year'] == '2009-10']['Frequency'].mean()
freq_2011 = customerdf[customerdf['Year'] == '2011-12']['Frequency'].mean()
delta4 = ((freq_2011 - freq_2009) /freq_2009) * 100
avgfreq = customerdf['Frequency'].mean()

# AVERAGE CUSTOMER LIFETIME
avgclife_2009 = customerdf[customerdf['Year'] == '2009-10']['CustomerLifetime'].mean()
avgclife_2011 = customerdf[customerdf['Year'] == '2011-12']['CustomerLifetime'].mean()
delta5 = ((avgclife_2011 - avgclife_2009) / avgclife_2009) * 100
avgclife = customerdf['CustomerLifetime'].mean()

a, b, c, d, e = st.columns([0.9, 1, 0.9, 0.95, 0.8])

a.metric(label = 'Active Customers', 
    value = f"{totalppl}",
    delta = f"{delta1:.1f}%",
    border = True,
    height = 'stretch',
    width = 'content')
b.metric(label = 'Total CLV', 
    value = f"${totalclv/1e6:.1f}M",
    delta = f"{delta2:.1f}%",
    border = True,
    height = 'stretch',
    width = 'content')
c.metric(label = 'Average CLV', 
    value = f"${avgclv/1e3:.1f}K",
    delta = f"{delta3:.1f}%",
    border = True,
    height = 'stretch',
    width = 'content')
d.metric(label = 'Average Frequency', 
    value = f"{avgfreq:.1f}",
    delta = f"{delta4:.1f}%",
    border = True,
    height = 'stretch',
    width = 'content')
e.metric(label = 'Avg Customer Lifetime', 
    value = f"{avgclife:.1f}",
    delta = f"{delta5:.1f}%",
    border = True,
    height = 'stretch',
    width = 'content')

customerdf['Month'] = customerdf['LastPurchaseDate'].dt.to_period("M").dt.to_timestamp()

col_select, col_chart = st.columns([1, 3])

with col_select :
    st.write(" ")
    selected_segments = st.multiselect(
        "Select a Customer Group",
        ['Premium', 'Core', 'Promising', 'Emerging', 'Declining', 'Critical', 'Inactive', 'Watchlist'],
        default = ['Premium', 'Core', 'Promising', 'Emerging', 'Declining', 'Critical', 'Inactive', 'Watchlist'],
        width = 400,
        key = "segment_multiselect"
    )
    st.write(" ")
    show_avg = st.toggle("Show Average CLV", value = None, key = "toggle_clv")




filtered_df = customerdf[customerdf['Segment'].isin(selected_segments)]

if show_avg:
   line_df = (
    filtered_df.groupby(["Month", "Segment"], as_index=False)
    .agg(AverageCLV = ("TotalCLV", "mean")))
   y_col = "AverageCLV"
   titlef = "Average CLV by Customer Segment"
else:
    line_df = (
    filtered_df.groupby(["Month", "Segment"], as_index=False)
    .agg(TotalCLV = ("TotalCLV", "sum")))
    y_col = "TotalCLV"
    titlef = "Total CLV by Customer Segment"

if line_df.empty :
    st.warning('Please select at least one segment')
fig1 = px.line(
    line_df,
    x = "Month",
    y = y_col,
    color = "Segment",
    markers = True,
    title = titlef
)

with col_chart :
    st.plotly_chart(fig1)

avg_customer_lifetime = (
    filtered_df.groupby("Segment", as_index = False)
    .agg(AvgCustomerLifetime = ("CustomerLifetime", "mean"))
)
fig2 = px.bar(
    avg_customer_lifetime, 
    x = "Segment", 
    y = "AvgCustomerLifetime", 
    color = "Segment",
    title = "Average Customer Lifetime by Segment")
st.plotly_chart(fig2)

avg_freq = (
    filtered_df.groupby("Segment", as_index = False)
    .agg(AvgFrequency = ("Frequency", "mean"))
)
fig3 = px.bar(
    avg_freq, 
    x = "Segment", 
    y = "AvgFrequency", 
    color = "Segment",
    title = "Average Frequency by Segment")
st.plotly_chart(fig3)

avg_ov = (
    filtered_df.groupby("Segment", as_index = False)
    .agg(AvgOrderValue = ("AvgOrderValue", "mean"))
)
fig4 = px.bar(
    avg_ov, 
    x = "Segment", 
    y = "AvgOrderValue", 
    color = "Segment",
    title = "Average Order Value by Segment")
st.plotly_chart(fig4)

a1, b1, c1 = st.columns([0.8, 2, 0.8])

segment_options = ["Select a segment"] + list(segmentdf['Segment'].unique())
option = b1.selectbox(
    "Select any one Segment for analysis",
    options = segment_options,
    index=0,
    key="segment_selectbox"
)

filter2 = customerdf.loc[customerdf['Segment'] == option]

st.write(" ")
st.write(" ")

spacer1, first, second, third, spacer2 = st.columns([1.4, 1.45, 1.3, 1.7, 1])

avg_clifetime_option = filter2['CustomerLifetime'].mean()
avg_freq_option = filter2['Frequency'].mean()
avg_purchase_option = filter2['PurchaseRate'].mean()


first.metric(
    label = "Avg Customer Lifetime",
    value = f"{avg_clifetime_option:.2f}",
    border = True,
    height = 'stretch',
    width = 'content'
)
second.metric(
    label = "Average Frequency",
    value = f"{avg_freq_option:.2f}",
    border = True,
    height = 'stretch',
    width = 'content'
)
third.metric(
    label = "Average Purchase Rate",
    value = f"{avg_purchase_option:.2f}",
    border = True,
    height = 'stretch',
    width = 'content'
)

segment_colors = {
    "Premium": "#F4A261",          
    "Critical": "#3A86FF",     
    "Core": "#2EC4B6",    
    "Promising": "#FF9F1C", 
    "Watchlist": "#8AC926",     
    "Declining": "#90DBF4",            
    "Inactive": "#FF595E",        
    "Emerging": "#FFD166"       
}

fighist = px.histogram(
    filter2,
    x = "Recency",
    color="Segment",
    color_discrete_map=segment_colors
)

figmon = px.histogram(
    filter2,
    x = "Monetary",
    color = "Segment",
    color_discrete_map = segment_colors
)

space1, left_chart, right_chart, space2 = st.columns([1, 6, 6, 1])

with left_chart: 
    st.plotly_chart(fighist)
with right_chart: 
    st.plotly_chart(figmon)


top_customers = customerdf.sort_values('TotalCLV', ascending = False).head(5)

metrics = ['Recency', 'Frequency', 'Monetary', 'CustomerLifetime', 'TotalCLV']
max_vals = customerdf[metrics].max()
all_data = []
for _, customer in top_customers.iterrows():
    values = [customer[metric] for metric in metrics]
    values_normalized = [values[i] / max_vals[i] for i in range(len(values))]
    
    for i, metric in enumerate(metrics):
        all_data.append({
            'CustomerID': customer['Customer ID'],
            'Metric': metric,
            'Normalized Value': values_normalized[i]
        })

chart_df = pd.DataFrame(all_data)

c, d = st.columns([1, 3])

with c :
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    selection = st.radio(
    "Select a Customer ID",
    chart_df['CustomerID'].unique(),
    horizontal=False,  # Set to False for vertical
    )


plot_df = chart_df[chart_df['CustomerID'] == selection]

fig = px.line(
        plot_df,
        x='Metric',
        y='Normalized Value',
        color='CustomerID',
        markers=True,
        title="Top 5 Customer Comparison"
    )
    
fig.update_layout(
    xaxis_title="Metrics",
    yaxis_title="Value"
    )
    

with d :
    st.plotly_chart(fig)


segmentdf['%TotalCLV'] = (segmentdf['TotalCLV'] / (segmentdf['TotalCLV'].sum()))*100
figpie = px.pie(
    segmentdf,
    values = "%TotalCLV",
    names = "Segment",
    hole = 0.5,
)

l, r = st.columns([1, 1])

with l :
    st.plotly_chart(figpie)

with r :
    with st.container(border=True):
        st.markdown("### 📊 Insights")
        st.markdown("""
        1. **Three segments drive 80% of revenue** — Promising, Inactive, and Watchlist. Protect them at all costs.

        2. **Core is growing but diluting** — More customers, but each spends less. Volume up, value down.

        3. **Retention is fine, frequency isn't** — Customers stay ~200 days but rarely buy. Fix purchase frequency.

        4. **Critical customers have the highest spend** — Don't lose them. A few defections would hurt badly.

        5. **Big wins hiding in plain sight** — Inactive can reactivate. Promising can upgrade. Both need a push.
        """)


if 'show_data' not in st.session_state:
    st.session_state.show_data = False

if st.button("📊 Customer Data Preview", key = "Button1"):
    st.session_state.show_data = not st.session_state.show_data

if st.session_state.show_data:
    st.dataframe(customerdf)

if 'show_segment' not in st.session_state:
    st.session_state.show_segment = False

if st.button("📈 Segment Data Preview", key = "Button2"):
    st.session_state.show_segment = not st.session_state.show_segment

if st.session_state.show_segment:
    st.dataframe(segmentdf)
