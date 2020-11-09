import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

_COLOURS = ['blue', 'red', 'orange', 'black', 'green', 'cyan', 'yellow', 'magenta', 'white', 'b', 'g', 'r', 'c', 'm', 'k', 'w', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
DEFAULT_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

class Graphing2D:
    def __init__(self, *args):    
        self._data = []
        self._headers = {}

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
                self._data.append(pd.to_numeric(self._data[h], downcast='float'))
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
                i += 0

        self._legends = []

    def add_plot(self, x_title, y_title, **kwargs):
        # accepted kwargs
        # autolabel = bool
        # autolegend = bool
        # legend = string (is overridden by autolegend)
        _x = self._get_column_input(x_title)
        _y = self._get_column_input(y_title)

        # manage kwargs
        _autolabel, _legend, _autolegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs)
        if _autolabel:
            plt.xlabel(_x)
            plt.ylabel(_y)
        _label = 'plot'
        _addLegend = False
        if _legend != None:
            _label = _legend
            _addLegend = True
        if _autolegend != None:
            if _autolegend:
                _label = _y
                _addLegend = True
            else:
                _addLegend = False

        if _addLegend:
            self._legends.append(_label)

        plt.plot([x + _x_shift for x in self._data[_x]], [y + _y_shift for y in self._data[_y]], label=_label, color=_colour)

    def add_scatter(self, x_title, y_title, **kwargs):
        _x = self._get_column_input(x_title)
        _y = self._get_column_input(y_title)

        # manage kwargs
        _autolabel, _legend, _autolegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs)
        if _autolabel:
            plt.xlabel(_x)
            plt.ylabel(_y)
        _label = 'plot'
        _addLegend = False
        if _legend != None:
            _label = _legend
            _addLegend = True
        if _autolegend != None:
            if _autolegend:
                _label = _y
                _addLegend = True
            else:
                _addLegend = False

        if _addLegend:
            self._legends.append(_label)

        plt.scatter([x + _x_shift for x in self._data[_x]], [y + _y_shift for y in self._data[_y]], label=_label, color=_colour)

    def add_linear_fit(self, x_title, y_title, **kwargs):
        _x = self._get_column_input(x_title)
        _y = self._get_column_input(y_title)

        # manage kwargs
        m, b = np.polyfit(self._data[_x], self._data[_y], 1)

        _autolabel, _legend, _autolegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs)
        if _autolabel:
            plt.xlabel(_x)
            plt.ylabel(_y)
        _label = 'plot'
        _addLegend = False
        if _legend != None:
            _label = _legend
            _addLegend = True
        if _autolegend != None:
            if _autolegend:
                _label = 'Linear Fit: m = {0}, b = {1}\n'.format(round(m, 2), round(b, 2)) + _y
                _addLegend = True
            else:
                _addLegend = False
        if 'customlegend' in kwargs:
            if not isinstance(kwargs['customlegend'], str):
                raise BadParameter
            _label = 'Linear Fit: m = {0}, b = {1}\n'.format(round(m, 2), round(b, 2)) + kwargs['customlegend']
            _addLegend = True

        if _addLegend:
            self._legends.append(_label)

        plt.plot([x + _x_shift for x in self._data[_x]], [m*x+b+_y_shift for x in self._data[_x]], label=_label, color=_colour)

    def add_quadratic_fit(self, x_title, y_title, **kwargs):
        _x = self._get_column_input(x_title)
        _y = self._get_column_input(y_title)

        # manage kwargs
        p = np.polyfit(self._data[_x], self._data[_y], 2)

        yf = np.array([p[0]*(x**2) + p[1]*x + p[2] for x in self._data[_x]])
        

        _autolabel, _legend, _autolegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs)
        if _autolabel:
            plt.xlabel(_x)
            plt.ylabel(_y)
        _label = 'plot'
        _addLegend = False
        if _legend != None:
            _label = _legend
            _addLegend = True
        if _autolegend != None:
            if _autolegend:
                _label = 'Quadratic Fit: a = {0}, b = {1}, c = {2}\n'.format(round(p[0], 2), round(p[1], 2), round(p[2], 2)) + _y
                _addLegend = True
            else:
                _addLegend = False
        if 'customlegend' in kwargs:
            if not isinstance(kwargs['customlegend'], str):
                raise BadParameter
            _label = 'Quadratic Fit: a = {0}, b = {1}, c = {2}\n'.format(round(p[0], 2), round(p[1], 2), round(p[2], 2)) + kwargs['customlegend']
            _addLegend = True

        if _addLegend:
            self._legends.append(_label)


        plt.plot([x + _x_shift for x in self._data[_x]], [y + _y_shift for y in yf], label=_label, color=_colour)

    def add_exponential_fit(self, x_title, y_title, **kwargs):
        _x = self._get_column_input(x_title)
        _y = self._get_column_input(y_title)

        for y in self._data[_y]:
            if y <= 0:
                raise NegativeLog

        # manage kwargs
        p = np.polyfit(self._data[_x], np.log(self._data[_y]), 1)

        yf = np.array([np.exp(p[1]) * np.exp(p[0]*x) for x in self._data[_x]])
        
        _autolabel, _legend, _autolegend, _colour, _x_shift, _y_shift = self._manage_kwargs(kwargs)
        if _autolabel:
            plt.xlabel(_x)
            plt.ylabel(_y)
        _label = 'plot'
        _addLegend = False
        if _legend != None:
            _label = _legend
            _addLegend = True
        if _autolegend != None:
            if _autolegend:
                _label = 'Exponential Fit: k = {0}, '.format(round(p[0], 2)) + r'$\gamma$' + ' = {1}\n'.format(round(p[1], 2)) + _y
                _addLegend = True
            else:
                _addLegend = False
        if 'customlegend' in kwargs:
            if not isinstance(kwargs['customlegend'], str):
                raise BadParameter
            _label = 'Exponential Fit: k = {0}, '.format(round(p[0], 2)) + r'$\gamma$' + ' = {1}\n'.format(round(p[1], 2)) + kwargs['customlegend']
            _addLegend = True

        if _addLegend:
            self._legends.append(_label)

        plt.plot([x + _x_shift for x in self._data[_x]], [y + _y_shift for y in yf], label=_label, color=_colour)

    def set_title(self, title):
        if not isinstance(title, str):
            raise BadParameter
        plt.title(title)

    def set_labels(self, x_label, y_label):
        if not (isinstance(x_label, str) and isinstance(x_label, str)):
            raise BadParameter
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    def _manage_kwargs(self, kwargs):
        _autolabel = False
        _legend = ''
        _autolegend = None
        _colour = DEFAULT_COLORS[0]
        _x_shift = 0
        _y_shift = 0

        if 'autolabel' in kwargs:
            if not isinstance(kwargs['autolabel'], bool):
                raise BadParameter
            if kwargs['autolabel']:
                _autolabel = True

        if 'legend' in kwargs:
            if not isinstance(kwargs['legend'], str):
                BadParameter
            _legend = kwargs['legend']
        else:
            _legend = None
        
        if 'autolegend' in kwargs:
            if not isinstance(kwargs['autolegend'], bool):
                raise BadParameter
            if kwargs['autolegend']:
                _autolegend = True
            else:
                _autolegend = False

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

        return _autolabel, _legend, _autolegend, _colour, _x_shift, _y_shift

    def _get_column_input(self, param):
        if isinstance(param, str):
            return self._headers[param]
        elif isinstance(param, int):
            return param
        raise BadParameter

    def show(self):
        if len(self._legends) > 0:
            plt.legend(self._legends)
        plt.show()

    @staticmethod
    def help():
        s = '*Insert documention*. Will be added in future update :)'
        print(s)
            
class BadParameter(Exception):
    pass

class NegativeLog(Exception):
    pass

if __name__ == '__main__':
    graphing = Graphing2D('Datos_Lauti_SuperAcotado.csv')
    graphing.add_plot(0, 1, legend='Datos del Giroscopio', x_shift=-4)
    graphing.add_linear_fit(0, 1, customlegend='Datos', color=DEFAULT_COLORS[1], x_shift=-4)
    graphing.set_labels('tiempo (s)', 'Velocidad Angular (rad/s)')
    graphing.set_title('Velocidad Angular')
    graphing.show()