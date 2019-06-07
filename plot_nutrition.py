import pickle
import numpy as np
import pandas as pd
import os
import bokeh
import bokeh.plotting
import bokeh.io
from preprocess import preprocess

countries_shortcut = {'India': 'IND', 'Japan': 'JPN', 'Korea': 'KOR', 'China': 'CHN', 'Thai': 'THA', 'Italy': 'ITA', 'France': 'FRC', 'Greece': 'GRC', 'Mexico': 'MEX', 'US': 'USA'}

class plot_nutrition:
    '''
    A class for nutrition plots.
    '''
    
    def __init__(self, countries=None, obesity_rate=None):
        '''
        Initialization function
        
        Parameters
        ----------
        countries: list
        - A list of countries 
        
        obesity_rate: list
        - A list of obesity rates of corresponding countries, should have the same length as countries
        '''
        
        # Nutrition attributes and health data
        self.nutritions = ['calories', 'fat', 'protein', 'cholesterol', 'sodium', 'carbohydrate']
        self.units = ['cal', 'g', 'g', 'mg', 'mg', 'g']
        self.df = self.get_nutritions(countries, obesity_rate)


    def get_nutritions(self, countries=None, obesity_rate=None):
        '''
        Get the nutrition fact pandas dataFrame from scraped data

        Parameters
        ----------
        countries: list
        - A list of country names

        obesity_rate: list
        - A list of obesity rates of the corresponding countries

        Returns
        -------
        df: pd.DataFrame
        - A dataframe contains means of nutrition facts of each country, and the health data of each country
        '''


        if countries == None:
            countries = ['India', 'Japan', 'Korea', 'China', 'Thai', 'Italy', 'France', 'Greece', 'Mexico', 'US']
        assert isinstance(countries, list)

        if obesity_rate == None:
            obesity_rate = [3.9, 4.3, 4.7, 6.2, 10, 19.9, 21.6, 24.9, 28.9, 36.2]
        assert isinstance(obesity_rate, list)
        assert len(countries) == len(obesity_rate)

        dfs = []
        for country in countries:
            with open('./data/allrecipes_' + country + '.pkl', 'rb') as f:
                dfs.append(pd.DataFrame(preprocess(pickle.load(f))))

        means = []
        for i, df in enumerate(dfs):
            means.append(df[self.nutritions].mean())

        df = pd.DataFrame(means)
        df['obesity_rate'] = obesity_rate
        df.index = countries
        df = df.sort_values(['obesity_rate'])

        return df
    
    def plot_bar_line(self, save_path='./img/bar.html'):
        '''
        Plotting nutrition lines and health data bars.

        Parameters
        ----------
        save_path: str
        - A filepath that saves the output image.

        Returns
        -------

        '''
        
        assert isinstance(save_path, str)

        tabs = []
        for nutrition, unit, color in zip(self.nutritions, self.units, bokeh.palettes.Category10[6]):
            x = np.array(self.df['obesity_rate'])
            y = np.array(self.df[nutrition])
            countries = [countries_shortcut[x] for x in list(self.df.index)]
            
            p = bokeh.plotting.figure(plot_height = 600,
                                      plot_width = 700,
                                      x_range = countries, 
                                      y_range = (0.9 * np.min(y), 1.1 * np.max(y)), 
                                      x_axis_label = 'Countries',
                                      y_axis_label=unit)

            p.extra_y_ranges = {'rate': bokeh.models.Range1d(start=0, end=40)}
            p.add_layout(bokeh.models.LinearAxis(y_range_name='rate',
                                                 axis_label='Obesity Rate(%)'), 'right')
            p.vbar(x=countries, top=x, width=0.9, y_range_name='rate', color = '#c9d9d3')

            p.line(x=countries, y=y, line_width=2, color = color, legend = nutrition)
            p.legend.location = 'top_left'
            p.legend.label_text_font_size = '12pt'
            p.xaxis.major_label_text_font_size = '11pt'
            p.yaxis.major_label_text_font_size = '14pt'
            p.xaxis.axis_label_text_font_size = '14pt'
            p.yaxis.axis_label_text_font_size = '14pt'
            tabs.append(bokeh.models.Panel(child=p, title=nutrition))

        Tabs = bokeh.models.Tabs(tabs=tabs)
        bokeh.plotting.output_file(save_path)
        bokeh.plotting.save(Tabs)
        
    def plot_scatter(self, save_path='./img/lr.html'):
        '''
        Scatter plot of nutrition and health data.

        Parameters
        ----------
        save_path: str
        - A filepath that saves the output image

        '''

        assert isinstance(save_path, str)

        figures = []
        for nutrition, unit, color in zip(self.nutritions, self.units, bokeh.palettes.Category10[6]):
            x = np.array(self.df['obesity_rate'])
            y = np.array(self.df[nutrition])
            m = np.polyfit(x, y, 1)
            corr = (np.cov(x, y)[1][0]) / (np.std(x) * np.std(y))
            
            p = bokeh.plotting.figure(title = nutrition + ' (Correlation Coefficient: {:.3f})'.format(corr),
                                      x_axis_label = 'Obesity Rate(%)',
                                      y_axis_label = unit)

            p.title.text_font_size = '18pt'
            p.xaxis.major_label_text_font_size = '16pt'
            p.yaxis.major_label_text_font_size = '16pt'
            p.xaxis.axis_label_text_font_size = '16pt'
            p.yaxis.axis_label_text_font_size = '16pt'
            p.scatter(x=x, y=y, size=10, color = color)
#             lx = np.array([0, 40])
#             p.line(x=lx, y=m[0] * lx + m[1], line_width=2, color = color)
            figures.append(p)

        bokeh.plotting.output_file(save_path)
        bokeh.plotting.save(bokeh.layouts.column(bokeh.layouts.row(figures[:3]), bokeh.layouts.row(figures[3:])))
#         bokeh.io.export_png(bokeh.layouts.row([figures[0], figures[1], figures[3]]), 'lr_1.png')
#         bokeh.io.export_png(bokeh.layouts.row([figures[2], figures[4], figures[5]]), 'lr_2.png')


if __name__ == '__main__':
	n = plot_nutrition()
	n.plot_bar_line()
	n.plot_scatter()
