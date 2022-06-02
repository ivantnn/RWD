import pandas as pd
import plotly.express as px
import streamlit as st
from scipy import stats
from numpy import floor ,newaxis
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

#https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title = 'Environmental Impact - JRODOS', page_icon=":bar_chart:",layout="wide")

df = pd.read_csv('Climate_info.csv')

#st.dataframe(df)
st.title(':arrow_down_small: Input Data')
st.header('Raw dataframe of Inputs')

#-----Sidebar
st.sidebar.header("Filter for the raw input dataframe here:")
day_Cloud = st.sidebar.multiselect("Select cloud conditions: ", options=df['Cloud'].unique(),default=df['Cloud'].unique())

df_selection = df.query('Cloud==@day_Cloud')

st.dataframe(df_selection)

#-----Main page

#graph = px.bar(
#    df,
#    x=df.index,
#    y='Angle',
#    title='<b>Angle of the Wind</b>',
#    color_discrete_sequence=['#008388']*len(df),
#    template='plotly_white')

#st.plotly_chart(graph)

#heatmap = px.imshow(
#    df['Class'].values[:,np.newaxis].T,
#    color_continuous_scale='RdBu_r',
#    title='<b>Cloudy?</b>',
#    labels=dict(x="Day of Month", color="The red-est, the cloud-est")
#    )

#st.plotly_chart(heatmap)
st.markdown('---')
st.header('Plots!')

#st.subheader('WindRose - Source of the winds')

#img = io.imread('Windrose.png')
#fig = px.imshow(img)
#fig.update_layout(height=1000, width=1000)
#st.plotly_chart(fig)

#st.markdown('##')
sns.set_theme(style="whitegrid")
fig,ax = plt.subplots(nrows=2,sharex=True)

#df.Speed_ms.plot.bar(ax=ax[1])
ax[0].bar(df.index, df['Rain_mm'],align='edge')
ax[0].set(title='Speed and Rain',ylabel='Speed (m/s)')
ax3 = ax[0].twinx()
ax3.plot(df.index+0.5, df['Speed_ms'],'-o',color="#742802")
#df.Rain_mm.plot.line(color="#742802",ax=ax3)
ax3.set(ylabel='Rain (mm)')
ax[0].spines['top'].set_visible(False)
ax3.spines['top'].set_visible(False)

#sns.color_palette("mako", as_cmap=True)
sns.heatmap(df['Class'].values[:,newaxis].T,ax=ax[1],yticklabels=False,cbar=False,cmap="mako_r")
ax[1].set(title='Cloudiness', xlabel='Hours (hr)')

st.subheader('Rain, Wind Speed and Cloudiness')
st.pyplot(fig)

st.markdown('---')
st.header('Overall...')
st.markdown('##')

def Emoji_weather(weather):
    if weather =='Overcast':
        emoji =  ':cloud:'*2 +':zap:'
    elif weather =='Cloudy':
        emoji =  ':cloud:'*2
    elif weather =='Some_Clouds':
        emoji = ':cloud:'
    else:
        emoji = ':sunny:'
    return emoji
df2 = pd.Series(['Overcast','Cloudy','Some_Clouds','Cloudless'])
most_weather = df2.iloc[stats.mode(df['Class'])[0]][0]
st.subheader(f"Most repeating weather: {most_weather} {Emoji_weather(most_weather)}")


st.markdown('##')
total_rain = df_selection['Rain_mm'].sum()
average_wind = df_selection['Speed_ms'].mean()
average_angle = df_selection['Angle'].mean()

l_col,m_col,r_col = st.columns(3)
with l_col:
    st.subheader('Total Rain: ')
    st.subheader(f"{total_rain:,} mm")

with m_col:
    st.subheader('Average Wind: ')
    st.subheader(f"{average_wind:,} m/s")

with r_col:
    st.subheader('Average Angle: ')
    st.subheader(f"{floor(average_angle):,} deg")

st.markdown('---')

hide_st_style="""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html = True)
