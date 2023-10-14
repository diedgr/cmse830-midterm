import streamlit as st
import pandas as pd
import plotly.express as px

csv_file_path = 'V-Dem-CPD-Party-V2.csv'
data = pd.read_csv(csv_file_path)

# Add a title to the app
st.title("Exploring the Positions and Ideologies of Political Parties")
st.caption("Source: V-Party Dataset")
st.write("This visualization presents time-series data of the ideological positions of major political parties from 178 countries. The data is sourced from the V-Party dataset, which includes assessments of party organization and identity as reflected by experts in political science.")

# Dictionary mapping variable names to user-friendly labels
label_map = {
    "v2paanteli": "Anti-elitism",
    "v2papeople": "People-centrism",
    "v2paopresp": "Political opponents",
    "v2paplur": "Political pluralism",
    "v2paminor": "Minority rights",
    "v2paviol": "Rejection of political violence",
    "v2paimmig": "Immigration",
    "v2palgbt": "LGBT social equality",
    "v2paculsup": "Cultural superiority",
    "v2parelig": "Religious principles",
    "v2pagender": "Gender equality",
    "v2pawomlab": "Working women"
}

# Function to format the select box display
def format_func(key):
    return label_map[key]

# Sidebar for user input
st.sidebar.header("Select Options")
country_name = st.sidebar.selectbox("Select Country", data['country_name'].unique())
identity_score = st.sidebar.selectbox(
    "Select Party Position",
    options=list(label_map.keys()),
    format_func=format_func
)

filtered_data = data[data['country_name'] == country_name]

# Create a line graph with Plotly
party_options = filtered_data['v2paenname'].unique()
party_colors = {party: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, party in enumerate(party_options)}
fig = px.line(filtered_data, x='year', y=identity_score, color='v2paenname', color_discrete_map=party_colors, labels={'year': 'Year', identity_score: label_map[identity_score]})
if identity_score == 'v2pariglef':
    fig.update_yaxes(title=label_map[identity_score])
else:
    fig.update_yaxes(title=label_map[identity_score])

fig.update_layout(title=f'Scores for Parties in {country_name}')

# Remove the legend from the graph
fig.update_traces(showlegend=False)

# Display the line graph
st.plotly_chart(fig)

# Edit the trace box
fig.update_traces(
    hoverinfo='text',
    hovertext=[f'Party Name: {name}' for name in filtered_data['v2paenname']]
)

# Set up the layout for the legend and additional information
col1, col2 = st.columns([3, 3])

# Display the legend in col1
with col1:
    st.subheader("Legend")
    for party, color in party_colors.items():
        st.write(f"<div style='display: flex; align-items: center;'><div style='background-color: {color}; width: 20px; height: 10px; margin-right: 5px;'></div> {party}</div>", unsafe_allow_html=True)

# Dictionary mapping variable names to corresponding questions
question_map = {
    "v2paanteli": "How important is anti-elite rhetoric for this party?",
    "v2papeople": "Do leaders of this party glorify the ordinary people and identify themselves as part of them?",
    "v2paopresp": "Prior to this election, have leaders of this party used severe personal attacks or tactics of demonization against their opponents?",
    "v2paplur": "Prior to this election, to what extent was the leadership of this political party clearly committed to free and fair elections with multiple parties, freedom of speech, media, assembly and association?",
    "v2paminor": "According to the leadership of this party, how often should the will of the majority be implemented even if doing so would violate the rights of minorities?",
    "v2paviol": "To what extent does the leadership of this party explicitly discourage the use of violence against domestic political opponents?",
    "v2paimmig": "What is the party’s position regarding immigration into the country?",
    "v2palgbt": "What is this party’s position toward social equality for the lesbian, gay, bisexual, and transgender (LGBT) community?",
    "v2paculsup": "To what extent does the party leadership promote the cultural superiority of a specific social group or the nation as a whole?",
    "v2parelig": "To what extent does this party invoke God, religion, or sacred/religious texts to justify its positions?",
    "v2pagender": "What is the share of women in national-level leadership positions of this political party?",
    "v2pawomlab": "To what extent does this party support the equal participation of women in the labor market?"
}

# Dictionary mapping variable names to corresponding coding system
coding_map = {
    "v2paanteli": [
        "0: Not at all important. The leadership of this party never makes statements against the elite.",
        "1: Not important. The leadership of this party rarely makes statements against the elite.",
        "2: Somewhat important. The leadership of this party sometimes makes statements against the elite.",
        "3: Important. The leadership of this party often makes statements against the elite.",
        "4: Very important. The leadership of this party makes statements against the elite whenever possible."
    ],
    "v2papeople": [
        "0: Never. The party leadership never glorifies and identifies with the ordinary people.",
        "1: Usually not. The party leadership generally does not glorify and identify with the ordinary people.",
        "2: About half of the time. The party leadership sometimes glorifies and identifies with the ordinary people.",
        "3: Usually. The party leadership generally glorifies and identifies with the ordinary people, which they claim to represent.",
        "4: Always. The party leadership always glorifies and identifies with the ordinary people, which they claim to represent."
    ],
    "v2paopresp": [
        "0: Always. Party leaders always used severe personal attacks or tactics of demonization against their opponents.",
        "1: Usually. Party leaders usually used severe personal attacks or tactics of demonization against their opponents.",
        "2: About half of the time. Party leaders sometimes used severe personal attacks or tactics of demonization against their opponents.",
        "3: Usually not. Party leaders usually did not use severe personal attacks or tactics of demo- nization against their opponents.",
        "4: Never. Party leaders never used severe personal attacks or tactics of demonization against their opponents."
    ],
    "v2paplur": [
        "0: Not at all committed. The party leadership was not at all committed to free and fair, multi-party elections, freedom of speech, media, assembly and association.",
        "1: Not committed. The party leadership was not committed to free and fair, multi-party elections, freedom of speech, media, assembly and association.",
        "2: Weakly committed. The party leadership was weakly committed to free and fair, multi- party elections, freedom of speech, media, assembly and association.",
        "3: Committed. The party leadership was committed to free and fair, multi-party elections, freedom of speech, media, assembly and association.",
        "4: Fully committed. The party leadership was fully committed to free and fair, multi-party elections, freedom of speech, media, assembly and association."
    ],
    "v2paminor": [
        "0: Always. The leadership of this party argues that the will of the majority should always determine policy even if such policy violates minority rights.",
        "1: Usually. The leadership of this party argues that the will of the majority should usually determine policy even if such policy violates minority rights.",
        "2: Half of the time. The leadership of this party argues that the will of the majority should about half of the time determine policy even if such policy violate minority rights.",
        "3: Usually not. The leadership of this party argues that the will of the majority should usually not determine policy if such policy violates minority rights.",
        "4: Never. The leadership of this party argues that the will of the majority should never determine policy if such policy violates minority rights."
    ],
    "v2paviol": [
        "0: Encourages. Leaders of this party often encourage the use of violence against domestic political opponents.",
        "1: Sometimes encourages. Leaders of this party sometimes encourage the use of violence against domestic political opponents and generally refrain from discouraging it.",
        "2: Discourages about half of the time. Leaders of this party occasionally discourage the use of violence against domestic political opponents, and do not encourage it.",
        "3: Generally discourages. Leaders of this party often discourage the use of violence against its domestic political opponents.",
        "4: Consistently discourages. Leaders of this party consistently reject the use of violence against its domestic political opponents."
    ],
    "v2paimmig": [
        "0: Strongly opposes. This party strongly opposes all or almost all forms of immigration into the country.",
        "1: Opposes. This party opposes most forms of immigration into the country.",
        "2: Ambiguous/No position. This party has no clear policy with regard to immigration into the country.",
        "3: Supports. This party supports most forms of immigration into the country.",
        "4: Strongly supports. This party strongly supports all or almost all forms of immigration into the country."
    ],
    "v2palgbt": [
        "0: Strongly opposes. This party is strongly opposed to LGBT social equality.",
        "1: Opposes. This party is opposed to LGBT social equality.",
        "2: Ambiguous/No position. This party has no clear policy with regard to LGBT social equality.",
        "3: Supports. This party supports LGBT social equality.",
        "4: Strongly supports. This party strongly supports LGBT social equality."
    ],
    "v2paculsup": [
        "0: Strongly promotes. The party strongly promotes the cultural superiority of a specific social group or the nation as a whole.",
        "1: Promotes. The party promotes the cultural superiority of a specific social group or the nation as a whole.",
        "2: Ambiguous. The party does not take a specific position on the cultural superiority of a specific social group or the nation as a whole.",
        "3: Opposes. The party opposes the promotion of the cultural superiority of a specific social group or the nation as a whole.",
        "4: Strongly opposes. The party strongly opposes the promotion of the cultural superiority of a specific social group or the nation as a whole."
    ],
    "v2parelig": [
        "0: Always, or almost always. The party almost always invokes God, religion, or sacred/religious texts to justify its positions.",
        "1: Often, but not always. The party often, but not always, invokes God, religion, or religious texts to justify its positions.",
        "2: About half of the time. The party about half of the time invokes God, religion, or religious texts to justify its positions.",
        "3: Rarely. The party rarely invokes God, religion, or religious texts to justify its positions.",
        "4: Never. The party never invokes God, religion, or religious texts to justify its positions."
    ],
    "v2pagender": [
        "0: None.",
        "1: Small minority (about 1-15%).",
        "2: Medium minority (about 16-25%).",
        "3: Large minority (about 26-39%).",
        "4: Balanced (about 40% or more)."
    ],
    "v2pawomlab": [
        "0: Strongly opposes. This party strongly opposes all or almost all types of measures that support the equal participation of women in the labor market.",
        "1: Opposes. This party opposes most types of measures that support the equal participation of women in the labor market.",
        "2: Ambiguous/No position. This party has no clear policy with regard to measures that support the equal participation of women in the labor market.",
        "3: Supports. This party supports most types of measures that support the equal participation of women in the labor market.",
        "4: Strongly supports. This party strongly supports all or almost all types of measures that support the equal participation of women in the labor market."
    ],
}

# Additional Information display
with col2:
    st.subheader("Scoring System")
    if identity_score in label_map:
        st.write(f"Question: {question_map[identity_score]}")
        st.write("Responses:")
        for rating in coding_map[identity_score]:
            st.write(rating)

# New imports for 3D scatter plot
import plotly.graph_objects as go

# New title for the 3D scatter plot
st.subheader("3D Scatter Plot")

# Find the most recent year with data available
most_recent_year = filtered_data['year'].max()

# Filtering data based on the most recent year
filtered_data_year = filtered_data[filtered_data['year'] == most_recent_year]

# Check if data is available for the most recent year
if filtered_data_year.empty:
    st.write("No data available for the most recent year.")
else:
    # 3D Scatter plot creation
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=filtered_data_year['v2pariglef'],
        y=filtered_data_year['ep_v6_lib_cons'],
        z=filtered_data_year[identity_score],
        text=filtered_data_year['v2paenname'],  # set text to party names
        mode='markers',
        marker=dict(
            size=8,
            color=filtered_data_year[identity_score],  # set color to the identity score
            colorscale='Viridis',  # choose a colorscale
            opacity=0.8
        )
    )])

    # Layout configuration for the 3D scatter plot
    fig_3d.update_layout(scene=dict(
        xaxis_title='Economic Left-Right Scale',
        yaxis_title='Social Liberalism-Conservatism Scale',
        zaxis_title=label_map[identity_score],
        xaxis=dict(title=dict(font=dict(size=12))),
        yaxis=dict(title=dict(font=dict(size=12))),
        zaxis=dict(title=dict(font=dict(size=12))),
    ), 
    margin=dict(l=0, r=0, b=0, t=0))

    # Configuring the frame
    fig_3d.update_layout(scene_aspectmode='manual',
                        scene_aspectratio=dict(x=1, y=1, z=0.8))

    # Display the 3D scatter plot
    st.plotly_chart(fig_3d)