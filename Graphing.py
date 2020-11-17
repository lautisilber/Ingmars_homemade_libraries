import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from Logging import log

_COLOURS = ['blue', 'red', 'orange', 'black', 'green', 'cyan', 'yellow', 'magenta', 'white', 'b', 'g', 'r', 'c', 'm', 'k', 'w', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
DEFAULT_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
_ERRORBAR_OPTION_TYPES = {'ecolor' : '', 'elinewidth' : 0.0, 'capsize' : 0.0, 'capthick' : 0.0, 'barsabove' : False, 'lolims' : False, 'uplims' : False, 'xlolims' : False, 'xuplims' : False, 'errorevery' : 1}
_PLOT_KWARGS = ['autoaxis', 'autolegend', 'legend', 'customlegend', 'colour', 'color', 'x_shift', 'y_shift', 'errorbars']
_SCATTER_KWARGS = ['marker', 's']
_SCATTER_STYLES = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] # or expression between $

class Graphing2D:
    def __init__(self, *args):    
        self._data = []
        self._headers = {}
        self._working_headers = ['0', '1']

        if not args:
            raise ParameterMissing

        processed_args = []

        for arg in args:
            if isinstance(arg, str):
                processed_args.append(arg)
            elif isinstance(arg, list) or isinstance(arg, np.ndarray):
                if not False in [isinstance(e, float) or isinstance(e, int) for e in arg]:
                    # list of numbers
                    processed_args.append(arg)
                elif not False in [isinstance(e, list) or isinstance(e, np.ndarray) or isinstance(e, str) for e in arg]:
                    # list of lists or directories
                    for e in arg:
                        processed_args.append(arg)
                else:
                    raise BadParameter

        for arg in processed_args:
            if isinstance(arg, str):
                if arg.endswith('.csv'):
                    _file = pd.read_csv(arg, sep=';')
                elif arg.endswith('.tsv'):
                    _file = pd.read_csv(arg, sep='\t')
                elif arg.endswith('.xlsx'):
                    _file = pd.read_excel(arg)
                else:
                    raise BadParameter

                i = 0
                for h in _file:
                    self._data.append(np.array(_file[h]))
                    self._headers.update({h : i})
                    i += 1

            elif isinstance(arg, list) or isinstance(arg, np.ndarray):
                if isinstance(arg, np.ndarray):
                    self._data.append(arg)
                else:
                    self._data.append(np.array(arg))
                for i in range(len(self._data[-1])):
                    self._headers.update({str(i) : i})

            else:
                raise BadParameter

        self._legends = []
        self._x = 0
        self._y = 1
        self._x_error = None
        self._y_error = None

        self._errorbar_options = {
            'ecolor' : DEFAULT_COLORS[0],
            'elinewidth' : None,
            'capsize' : 0.0,
            'capthick' : None,
            'barsabove' : False,
            'lolims' : False,
            'uplims' : False,
            'xlolims' : False,
            'xuplims' : False,
            'errorevery' : 1
        }

        self.set_working_data(0, 1)

    def set_working_data(self, x_name, y_name, x_error_name=None, y_error_name=None):
        x = self._get_column_input(x_name)
        y = self._get_column_input(y_name)
        if x >= len(self._data) or y >= len(self._data):
            raise NonExistingData
        self._x = x
        self._y = y
        if not x_error_name is None:
            x_error = self._get_column_input(x_error_name)
            if x_error >= len(self._data):
                raise NonExistingData
            self._x_error = x_error
        if not y_error_name is None:
            y_error = self._get_column_input(y_error_name)
            if y_error >= len(self._data):
                raise NonExistingData
            self._y_error = y_error
        self._working_headers[0] = str(list(self._headers.keys())[self._x])
        self._working_headers[1] = str(list(self._headers.keys())[self._y])

    def set_working_error_data(self, x_error_name, y_error_name):
        x_error = self._get_column_input(x_error_name)
        y_error = self._get_column_input(y_error_name)
        if x_error >= len(self._data) or y_error >= len(self._data):
            raise NonExistingData
        self._x_error = x_error
        self._y_error = y_error

    def set_errorbars_options(self, **kwargs):
        for key in kwargs.keys():
            if key in _ERRORBAR_OPTION_TYPES:
                if isinstance(_ERRORBAR_OPTION_TYPES[key], bool) and isinstance(kwargs[key], bool):
                    pass
                elif kwargs[key] is None:
                    pass
                elif isinstance(_ERRORBAR_OPTION_TYPES[key], float) and (isinstance(kwargs[key], float) or isinstance(kwargs[key], int)):
                    pass
                elif type(_ERRORBAR_OPTION_TYPES[key]) == type(kwargs[key]):
                    pass
                else:
                    raise BadParameter
                self._errorbar_options[key] = kwargs[key]
            else:
                log.warning('In "set_errorbars_options": The passed key "{0}" is not valid'.format(key))

    def add_plot(self, *args, **kwargs):
        # accepted kwargs
        # autolabel = bool
        # autolegend = bool
        # legend = string (is overrides autolegend)

        if args:
            self._manage_working_data_args(args)        

        # manage kwargs
        _finallegend, _colour, _x_shift, _y_shift, _errorbars, _marker, _s = self._manage_kwargs(kwargs)

        X = [x + _x_shift for x in self._data[self._x]]
        Y = [y + _y_shift for y in self._data[self._y]]

        plt.plot(X, Y, label=_finallegend, color=_colour)
        if _errorbars:
            self._add_errorbars(X, Y) 

    def add_scatter(self, *args, **kwargs):

        if args:
            self._manage_working_data_args(args) 

        # manage kwargs
        _finallegend, _colour, _x_shift, _y_shift, _errorbars, _marker, _s = self._manage_kwargs(kwargs, scatter=True)

        X = [x + _x_shift for x in self._data[self._x]]
        Y = [y + _y_shift for y in self._data[self._y]]

        plt.scatter(X, Y, label=_finallegend, color=_colour, marker=_marker, s=_s)
        if _errorbars:
            self._add_errorbars(X, Y) 

    def add_linear_fit(self, *args, **kwargs):

        if args:
            self._manage_working_data_args(args)  

        # manage kwargs
        m, b = np.polyfit(self._data[self._x], self._data[self._y], 1)

        yf = np.array([m*x+b for x in self._data[self._x]])

        _finallegend, _colour, _x_shift, _y_shift, _errorbars, _marker, _s = self._manage_kwargs(kwargs, fit='linear', m=m, b=b)

        X = [x + _x_shift for x in self._data[self._x]]
        Y = [y + _y_shift for y in yf]

        plt.plot(X, Y, label=_finallegend, color=_colour)
        if _errorbars:
            self._add_errorbars(X, Y)

    def add_quadratic_fit(self, *args, **kwargs):

        if args:
            self._manage_working_data_args(args)  

        # manage kwargs
        p = np.polyfit(self._data[self._x], self._data[self._y], 2)

        yf = np.array([p[0]*(x**2) + p[1]*x + p[2] for x in self._data[self._x]])

        _finallegend, _colour, _x_shift, _y_shift, _errorbars, _marker, _s = self._manage_kwargs(kwargs, fit='quadratic', a=p[0], b=p[1], c=p[2])

        X = [x + _x_shift for x in self._data[self._x]]
        Y = [y + _y_shift for y in yf]

        plt.plot(X, Y, label=_finallegend, color=_colour)
        if _errorbars:
            self._add_errorbars(X, Y)

    def add_exponential_fit(self, *args, **kwargs):

        if args:
            self._manage_working_data_args(args) 

        for y in self._data[self._y]:
            if y <= 0:
                raise NegativeLog

        # manage kwargs
        p = np.polyfit(self._data[self._x], np.log(self._data[self._y]), 1)

        yf = np.array([np.exp(p[1]) * np.exp(p[0]*x) for x in self._data[self._x]])
        
        _finallegend, _colour, _x_shift, _y_shift, _errorbars, _marker, _s = self._manage_kwargs(kwargs, fit='exponential', k=np.exp(p[1]), gamma = p[0])

        X = [x + _x_shift for x in self._data[self._x]]
        Y = [y + _y_shift for y in yf]

        plt.plot(X, Y, label=_finallegend, color=_colour)
        if _errorbars:
            self._add_errorbars(X, Y)

    def add_marker(self, x_pos, y_pos, **kwargs):
        # to date only args supported is style (shape)
        _finallegend, _colour, _x_shift, _y_shift, _errorbars, _marker, _s = self._manage_kwargs(kwargs, scatter=True)
        
        x = x_pos + _x_shift
        y = y_pos + _y_shift

        plt.scatter(x, y, marker=_marker, label=_finallegend, color=_colour, s=_s)

    def set_title(self, title):
        if not isinstance(title, str):
            raise BadParameter
        plt.title(title)

    def set_labels(self, x_label, y_label):
        if not (isinstance(x_label, str) and isinstance(x_label, str)):
            raise BadParameter
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    def _add_errorbars(self, X, Y):
        XError = self._data[self._x_error]
        YError = self._data[self._y_error]
        plt.errorbar(X, Y, XError, YError, ecolor=self._errorbar_options['ecolor'], elinewidth=self._errorbar_options['elinewidth'],
            capsize=self._errorbar_options['capsize'], barsabove=self._errorbar_options['barsabove'], lolims=self._errorbar_options['lolims'],
            uplims=self._errorbar_options['uplims'], xlolims=self._errorbar_options['xlolims'], xuplims=self._errorbar_options['xuplims'],
            errorevery=self._errorbar_options['errorevery'], capthick=self._errorbar_options['capthick'])

    def _manage_kwargs(self, kwargs, **nkwargs):
        _autoaxis = False
        _autolegend = None
        _finallegend = '_nolegend_' # internal. gets updated with legend, autolegend or customlegend (for fits)
        _colour = DEFAULT_COLORS[0]
        _x_shift = 0
        _y_shift = 0
        _errorbars = False
        _marker = rcParams['scatter.marker']
        _s = rcParams['lines.markersize'] ** 2

        for k in kwargs:
            if not (k in _PLOT_KWARGS or k in _SCATTER_KWARGS):
                log.warning('In "plotting": The passed key "{0}" is not valid'.format(k))

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

        if 'errorbars' in kwargs:
            if not isinstance(kwargs['errorbars'], bool):
                raise BadParameter
            if kwargs['errorbars']:
                _errorbars = True

        if 'scatter' in nkwargs:
            if nkwargs['scatter']:
                if 'marker' in kwargs:
                    if not (isinstance(kwargs['marker'], str) or isinstance(kwargs['marker'], int)):
                        raise BadParameter
                    if isinstance(kwargs['marker'], str):
                        if kwargs['marker'] in _SCATTER_STYLES or (kwargs['marker'].startswith('$') and kwargs['marker'].endswith('4')):
                            _marker = kwargs['marker']
                    elif kwargs['marker'] in _SCATTER_STYLES:
                        _marker = kwargs['marker']
                if 's' in kwargs:
                    if not (isinstance(kwargs['s'], float) or isinstance(kwargs['s'], int)):
                        raise BadParameter
                    _s = kwargs['s']

        return _finallegend, _colour, _x_shift, _y_shift, _errorbars, _marker, _s

    def _manage_working_data_args(self, args):
        if len(args) == 2:
            self.set_working_data(args[0], args[1])
        elif len(args) == 4:
            self.set_working_data(args[0], args[1], args[2], args[3])
        else:
            raise BadParameter

        self._x = self._get_column_input(args[0])
        self._y = self._get_column_input(args[1])
        if len(args) == 4:
            self._x_error = self._get_column_input(args[2])
            self._y_error = self._get_column_input(args[3])

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
    a = list(range(11))
    b = [i**2 for i in a]
    aerror = [1 for i in a]
    berror = [0.75 for i in a]

    g = Graphing2D([a, b], [aerror, berror])
    g.add_marker(a[5], b[5], legend='supermarker', colour=DEFAULT_COLORS[6], marker='H', s=150)
    g.set_working_data(0, 1, 2, 3)
    g.set_errorbars_options(capsize=1.5, ecolor='cyan')
    g.add_plot(errorbars=True)
    g.show()