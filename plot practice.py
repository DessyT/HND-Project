import plotly.plotly as py
import plotly.graph_objs as go

labels = ["oxygen","hydrogen","Carbon_Dioxide","Nitrogen"]
values = [4500,2500,1053,500]

trace = go.Pie(labels=labels,values=values)

py.iplot([trace],filename = "basic_pie_chat")
