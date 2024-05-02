import pandas as pd
import matplotlib as plt

def graph_dataframe(df) -> None:
	row_sum = [] #This block sums up all the columns for labeling purposes

	for row in df.index:
		row_sum.append(round(df.loc[row].sum()))

	color_scheme = plt.colormaps.get_cmap('tab20')
	fig = df.plot(kind='bar', stacked=True, title='Stacked_Bar',colormap = color_scheme)
	fig.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=7)
	plt.pyplot.savefig('Stacked_bar.png', dpi=300)

	for x, y in enumerate(row_sum): #Add text verticaly to the row
		fig.annotate(y, (x, y+0.1),fontsize=7,fontweight='bold',rotation = 'vertical',color ='red')
	plt.pyplot.show()