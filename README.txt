Contains code for processing and Graphing Financial data.

While data scubbing will be different for every project, this code expects a standard input of a Pandas Dataframe with the named columns: 'Category name', 'Ammount' and 'Date'.


Operations:
~Remove certain categories of transations from the final view
~Group categories by month rather than category
~Split certain categories into smaller transations that appear Over a preiod of time.
  For instance, some companies pay things like Utilities in 3 month periods. This lump sum is unhelpful for visualizing weekly or monthly costs. This level functionality allows
  single transactions to be seen as a regular occurence. 
~Visualize data in a stacked bar graph
