import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

_COLOURS = ['blue', 'red', 'orange', 'black', 'green', 'cyan', 'yellow', 'magenta', 'white', 'b', 'g', 'r', 'c', 'm', 'k', 'w', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
DEFAULT_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

class Graphing2D:
    def __init__(self, *args):    
        self._data = []
        self._headers = {}
        self._working_headers = ['0', '1']

        if not args:
            raise ParameterMissing

        if len(args) == 1:
            if not isinstance(args[0], str):
                raise BadParameter
            if args[0].endswith('.csv'):
                _file = pd.read_csv(args[0], sep=';')
            elif args[0].endswith('.tsv'):
                _file = pd.read_csv(args[0], sep='\t')
            elif args[0].endswith('.xlsx'):
                _file = pd.read_xlsx(args[0])
            else:
                raise BadParameter
            i = 0
            for h in _file:
                self._data.append(list())
                for n in _file[h]:
                    self._data[-1].append(n)
                self._headers.update({h : i})
                i += 1
        else:
            for arg in args:
                if not isinstance(arg, list):
                    raise BadParameter
                for c in arg:
                    if not (isinstance(c, int) or isinstance(c, float)):
                        raise BadParameter
            i = 0
            for arg in args:
                self._data.append(arg)
                self._headers.update({str(i) : i})
                i += 1

        self._legends = []
        self._x = 0
        self._y = 1
        self.set_working_data(0, 1)

    def set_working_data(self, x_name, y_name):
        self._x = self._get_column_input(x_name)
        self._y = self._get_column_input(y_name)
        if self._x >= len(self._data) or self._x >= len(self._data):
            raise NonExistingData
        self._working_headers[0] = str(list(self._headers.keys())[self._x])
        self._working_headers[1] = str(list(self._headers.keys())[self._y])

    def add_plot(self, *args, **kwargs):
        # accepted kwargs
        # autolabel = bool
        # autolegend = bool
        # legend = string (is overrides autolegend)

        if args:
            self._manage_working_data_args(args)        

        # manage kwargs
        _finallegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs)

        plt.plot([x + _x_shift for x in self._data[self._x]], [y + _y_shift for y in self._data[self._y]], label=_finallegend, color=_colour)

    def add_scatter(self, *args, **kwargs):

        if args:
            self._manage_working_data_args(args) 

        # manage kwargs
        _finallegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs)

        plt.scatter([x + _x_shift for x in self._data[self._x]], [y + _y_shift for y in self._data[self._y]], label=_finallegend, color=_colour)

    def add_linear_fit(self, *args, **kwargs):

        if args:
            self._manage_working_data_args(args)  

        # manage kwargs
        m, b = np.polyfit(self._data[self._x], self._data[self._y], 1)

        yf = np.array([m*x+b for x in self._data[self._x]])

        _finallegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs, fit='linear', m=m, b=b)

        plt.plot([x + _x_shift for x in self._data[self._x]], [y + _y_shift for y in yf], label=_finallegend, color=_colour)

    def add_quadratic_fit(self, *args, **kwargs):

        if args:
            self._manage_working_data_args(args)  

        # manage kwargs
        p = np.polyfit(self._data[self._x], self._data[self._y], 2)

        yf = np.array([p[0]*(x**2) + p[1]*x + p[2] for x in self._data[self._x]])

        _finallegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs, fit='quadratic', a=p[0], b=p[1], c=p[2])

        plt.plot([x + _x_shift for x in self._data[self._x]], [y + _y_shift for y in yf], label=_finallegend, color=_colour)

    def add_exponential_fit(self, *args, **kwargs):

        if args:
            self._manage_working_data_args(args) 

        for y in self._data[self._y]:
            if y <= 0:
                raise NegativeLog

        # manage kwargs
        p = np.polyfit(self._data[self._x], np.log(self._data[self._y]), 1)

        yf = np.array([np.exp(p[1]) * np.exp(p[0]*x) for x in self._data[self._x]])
        
        _finallegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs, fit='exponential', k=np.exp(p[1]), gamma = p[0])

        plt.plot([x + _x_shift for x in self._data[self._x]], [y + _y_shift for y in yf], label=_finallegend, color=_colour)

    def set_title(self, title):
        if not isinstance(title, str):
            raise BadParameter
        plt.title(title)

    def set_labels(self, x_label, y_label):
        if not (isinstance(x_label, str) and isinstance(x_label, str)):
            raise BadParameter
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    def _manage_kwargs(self, kwargs, **nkwargs):
        _autoaxis = False
        _autolegend = None

        _finallegend = '_nolegend_'
        _colour = DEFAULT_COLORS[0]
        _x_shift = 0
        _y_shift = 0

        if 'autoaxis' in kwargs:
            if not isinstance(kwargs['autoaxis'], bool):
                raise BadParameter
            if kwargs['autoaxis']:
                _autoaxis = True
                plt.xlabel(self._working_headers[0])
                plt.ylabel(self._working_headers[1])

        _addLegend = False
        if 'legend' in kwargs:
                if not isinstance(kwargs['legend'], str):
                    raise BadParameter
                _finallegend = kwargs['legend']
                _addLegend = True
        elif 'fit' in nkwargs:
            if nkwargs['fit'] == 'linear':
                _finallegend = 'Linear Fit: m = {0}, b = {1}\n'.format(round(nkwargs['m'], 2), round(nkwargs['b'], 2))
            elif nkwargs['fit'] == 'quadratic':
                # requires to pass to nkwargs the parameters 'a', 'b' and 'c' corresponding to the quadratic fit
                _finallegend = 'Quadratic Fit: a = {0}, b = {1}, c = {2}\n'.format(round(nkwargs['a'], 2), round(nkwargs['b'], 2), round(nkwargs['c'], 2))
            elif nkwargs['fit'] == 'exponential':
                _finallegend = 'Exponential Fit: k = {0}, '.format(round(nkwargs['k'], 2)) + r'$\gamma$' + ' = {0}\n'.format(round(nkwargs['gamma'], 2))
            else:
                raise InternalError
            if 'customlegend' in kwargs:
                if not isinstance(kwargs['customlegend'], str):
                    raise BadParameter
                _finallegend += kwargs['customlegend']
                _addLegend = True
            elif 'autolegend' in kwargs:
                if not isinstance(kwargs['autolegend'], bool):
                    raise BadParameter
                _finallegend += self._working_headers[1]
                _addLegend = True
        elif 'autolegend' in kwargs:
            if not isinstance(kwargs['autolegend'], bool):
                raise BadParameter
            _finallegend = self._working_headers[1]
            _addLegend = True

        if not _addLegend:
            _finallegend = '_nolegend_'
        self._legends.append(_finallegend)     

        if 'colour' in kwargs:
            if not isinstance(kwargs['colour'], str):
                raise BadParameter
            if kwargs['colour'] in _COLOURS:
                _colour = kwargs['colour']
        elif 'color' in kwargs:
            if not isinstance(kwargs['color'], str):
                raise BadParameter
            if kwargs['color'] in _COLOURS:
                _colour = kwargs['color']

        if 'x_shift' in kwargs:
            if not (isinstance(kwargs['x_shift'], float) or isinstance(kwargs['x_shift'], int)):
                raise BadParameter
            _x_shift = kwargs['x_shift']
        if 'y_shift' in kwargs:
            if not (isinstance(kwargs['y_shift'], float) or isinstance(kwargs['y_shift'], int)):
                raise BadParameter
            _y_shift = kwargs['y_shift']

        return _finallegend, _colour, _x_shift, _y_shift

    def _manage_working_data_args(self, args):
        if not len(args) == 2:
            raise BadParameter
        for arg in args:
            if not (isinstance(arg, str) or isinstance(arg, int)):
                raise BadParameter

        self._x = self._get_column_input(args[0])
        self._y = self._get_column_input(args[1])

    def _get_column_input(self, param):
        if isinstance(param, str):
            return self._headers[param]
        elif isinstance(param, int):
            return param
        raise BadParameter

    def show(self):
        _show_legends = False
        for l in self._legends:
            if l != '_nolegend_':
                _show_legends = True
                break
        if _show_legends:
            plt.legend()
        plt.show()

    @staticmethod
    def help():
        s = 'This library simplifies the graphic representations of datasets that can be python lists or excel-like files.'
        s += 'When calling Graphing2D for the first time you have two options: either\n'
        s += '\t- pass a string with the file path to a .csv/.tsv/.xlsx file\n'
        s += '\t- pass all the lists of (numerical) values\n\n'
        s += 'Although you can load multiple data "axis" only 2 (4 projected) can be active at the same time as "x" and "y".\n'
        s += 'This can be set with the "set_working_data()" method.\n\n'
        s += 'The different "add_...()" methods allow you to plot the data. Passing data axis as arguments changes the active axis.\n'
        s += 'Options can be passed as "add_...(Option1=parameter, Option2=parameter, ...)\n'
        s += 'The options currently available are:\n'
        s += '\t- autolabel=bool -> labels the drawn plot automagically\n'
        s += '\t- legend=str -> adds a user-written legend to the drawn plot\n'
        s += '\t- autolegend=bool -> automagically adds a legend to the drawn plot (overridden by "legend")\n'
        s += '\t- colour/color=str -> draws the plot with the specified colour (for more info visit matplotlibs documentation)\n'
        s += '\t- x_shift=float -> shifts the plot by the input in the "x" axis\n'
        s += '\t- y_shift=float -> like x_shift but in the "y" axis\n'
        print(s)


class BadParameter(Exception):
    # print('Bad parameter was given')
    pass

class NegativeLog(Exception):
    # print('Exponential fit with negative data in son yet supported')
    pass

class ParameterMissing(Exception):
    pass

class InternalError(Exception):
    pass

class NonExistingData(Exception):
    pass

if __name__ == '__main__':
    a = list(range(7))
    b = [0, 2, 4.1, 5.9, 8,2, 9.8]
    c = [0, 1.05, 4.1, 9.2, 15, 26, 35]

    g = Graphing2D(a, b, c)

    g.add_plot()
    g.add_linear_fit(colour='blue')
    g.add_plot(0, 2, colour='orange')
    g.add_quadratic_fit(colour='red')
    g.show()