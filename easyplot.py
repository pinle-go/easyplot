# -*- coding: utf-8 -*-
"""
Author: Sudeep Mandal
"""

import matplotlib.pyplot as plt
import matplotlib as mpl

class EasyPlot(object):
    """
    Class that implements thin matplotlib wrapper for easy, reusable plotting
    """
                  
    def __init__(self, *args, **kwargs):
        """
        Arguments
        =========
        *args : Support for plot(y), plot(x, y), plot(x, y, 'b-o'). x, y and
                format string are passed through for plotting
        
        **kwargs: All kwargs are optional
            fig : figure instance for drawing plots
            ax : axes instance for drawing plots (If user wants to supply axes,
                 figure externally, both ax and fig must be supplied together)
            figSize : tuple of integers ~ width & height in inches
            label : Label for line plot as determined by *args, string
            linewidth / lw : Plot linewidth
            linestyle / ls : Plot linestyle ['-','--','-.',':','None',' ','']
            marker : '+', 'o', '*', 's', 'D', ',', '.', '<', '>', '^', '1', '2'
            markerfacecolor / mfc : Face color of marker
            markeredgewidth / mew :
            markeredgecolor / mec : 
            markersize / ms : Size of markers
            markevery / mev : Mark every Nth marker 
                              [None|integer|(startind, stride)]
            alpha : Opacity of line plot (0 - 1.0), default = 1.0
            title : Plot title, string
            xlabel : X-axis label, string
            ylabel : Y-axis label, string
            xlim : X-axis limits - tuple. eg: xlim=(0,10). Set to None for auto
            ylim : Y-axis limits - tuple. eg: ylim=(0,10). Set to None for auto
            showlegend : set to True to display legend
            framealpha : Legend box opacity (0 - 1.0), default = 1.0
            loc : Location of legend box in plot, default = 'best'
            numpoints : number of markers in legend, default = 1.0
            color / c : Color of line plot, overrides format string in *args if
                        supplied. Accepts any valid matplotlib color
            colorcycle / cs: Set plot colorcycle to list of valid matplotlib
                             colors
            fontsize : Global fontsize for all plots
        """
        self._default_kwargs = {'fig': None,
                                'ax': None,
                                'figsize': None,
                                'label': None,
                                'showlegend': False,
                                'fancybox': True,
                                'framealpha': 1.0,
                                'loc': 'best',
                                'numpoints': 1
                               }
        self.kwargs = self._default_kwargs.copy()
        
        # Dictionary of plot parameter aliases               
        self.alias_dict = {'lw': 'linewidth', 'ls': 'linestyle', 
                           'mfc': 'markerfacecolor', 'mew': 'markeredgewidth', 
                           'mec': 'markeredgecolor', 'ms': 'markersize',
                           'mev': 'markevery', 'c': 'color', 'fs': 'fontsize'}
                           
        self.plot_kwargs = ['label', 'linewidth', 'linestyle', 'marker',
                            'markerfacecolor', 'markeredgewidth', 'markersize',
                            'markeredgecolor', 'markevery', 'alpha']
        
        # Parameters that should only be passed to the plot once                    
        self._uniqueparams = ['color', 'label', 'linestyle', 'marker',
                              'colorcycle']
                            
        self._ax_funcs = {'xlabel': 'set_xlabel',
                         'ylabel': 'set_ylabel',
                         'xlim': 'set_xlim',
                         'ylim': 'set_ylim',
                         'title': 'set_title',
                         'colorcycle': 'set_color_cycle'}
                         
        self.kwargs = self._default_kwargs.copy() #Prevent mutating dictionary
        self.args = []
        self.line_list = [] # List of all Line2D items that are plotted
        self.add_plot(*args, **kwargs)

    def add_plot(self, *args, **kwargs):
        """
        Add plot using supplied parameters and existing instance parameters
        
        Creates new Figure and Axes object if 'fig' and 'ax' parameters not
        supplied. Stores references to all Line2D objects plotted in 
        self.line_list. 
        Arguments
        =========
            *args : Support for plot(y), plot(x, y), plot(x, y, 'b-'). x, y and
                    format string are passed through for plotting
            **kwargs : Plot parameters. Refer to __init__ docstring for details
        """
        self._update(*args, **kwargs)

        # Create figure and axes if needed
        if self.kwargs['fig'] is None:
            self.kwargs['fig'] = plt.figure(figsize=self.kwargs['figsize'])
#            if self.kwargs['ax'] is None:
            self.kwargs['ax'] = plt.gca()
            self.kwargs['fig'].add_axes(self.kwargs['ax'])

        ax, fig = self.kwargs['ax'], self.kwargs['fig']
        
        
        # Add plot only if new args passed to this instance
        if self.isnewargs:
            # Create updated name, value dict to pass to plot method
            plot_kwargs = {kwarg: self.kwargs[kwarg] for kwarg 
                                in self.plot_kwargs if kwarg in self.kwargs}
            if 'color' in self.kwargs:
                plot_kwargs['color'] = self.kwargs['color']
            
            line, = ax.plot(*self.args, **plot_kwargs)
            self.line_list.append(line)            
          
        # Apply axes functions if present in kwargs
        for kwarg in self.kwargs:
            if kwarg in self._ax_funcs:
                # eg: f = getattr(ax,'set_title'); f('new title')
                func = getattr(ax, self._ax_funcs[kwarg])
                func(self.kwargs[kwarg])
           
        # Display legend if required
        if self.kwargs['showlegend']:
            leg = ax.legend(fancybox=self.kwargs['fancybox'],
                      framealpha=self.kwargs['framealpha'],
                      loc=self.kwargs['loc'],
                      numpoints=self.kwargs['numpoints'])
            leg.draggable(state=True)
        
        if 'fontsize' in self.kwargs:
            self.set_fontsize(self.kwargs['fontsize'])
            
        self._delete_uniqueparams() # Clear unique parameters from kwargs list
        self.redraw()
          
    def update_plot(self, **kwargs):
        """"Update plot parameters (keyword arguments) and replot figure
        
        Usage:
            a = ConvenientPlot([1,2,3], [2,4,8], 'r-o', label='label 1')
            a.plot() # Plots graph
            # Update title and xlabel string and redraw plot
            a.update_plot(title='Title', xlabel='xlabel')
        """
        self.add_plot(**kwargs)
        
    def new_plot(self, *args, **kwargs):
        """
        Plot new plot using Convenience Plot object and default parameters
        
        Pass a named argument reset=True if all plotting parameters should
        be reset to original defaults
        """
        reset = kwargs['reset'] if 'reset' in kwargs else False
        self._reset(reset=reset)
        self.kwargs['fig'] = None
        self.kwargs['ax'] = None
        self.add_plot(*args, **kwargs)
    
    def autoscale(self, enable=True, axis='both', tight=None):
        """Autoscale the axis view to the data (toggle).
        
        Convenience method for simple axis view autoscaling. It turns 
        autoscaling on or off, and then, if autoscaling for either axis is on,
        it performs the autoscaling on the specified axis or axes.
        
        Arguments
        =========
        enable: [True | False | None]
        axis: ['x' | 'y' | 'both']
        tight: [True | False | None]
        """
        ax = self.get_axes()
        ax.autoscale(enable=enable, axis=axis, tight=tight)
        self.redraw()
        
    def get_figure(self):
        """Returns figure instance of current plot"""
        return self.kwargs['fig']
        
    def get_axes(self):
        """Returns axes instance for current plot"""
        return self.kwargs['ax']
        
    def redraw(self):
        """
        Redraw plot. Use after custom user modifications of axis & fig objects
        """
        fig = self.kwargs['fig']
        #Redraw figure if it was previously closed prior to updating it
        if not plt.fignum_exists(fig.number):
            fig.show()
            
        fig.canvas.draw()
    
    def set_fontsize(self, font_size):
        """ Updates global font size for all plot elements"""
        mpl.rcParams['font.size'] = font_size
        self.redraw()
#        params = {'font.family': 'serif',
#          'font.size': 16,
#          'axes.labelsize': 18,
#          'text.fontsize': 18,
#          'legend.fontsize': 18,
#          'xtick.labelsize': 18,
#          'ytick.labelsize': 18,
#          'text.usetex': True}
#        mpl.rcParams.update(params)
    
#    def reset_params(self, *args):
#        """
#        Reset list of supplied plot parameters to defaults
#            *args : Comma separated list of strings with plot parameter names
#        Usage:
#            easyplotobj.reset_params('title', 'linestyle', 'lw')
#        """
#        arglist = list(args)  # Convert args tuple to list
#        # Replace aliased plot parameters in args with full parameter name
#        for alias in self.alias_dict:
#            if alias in arglist:
#                arglist[arglist.index(alias)] = self.alias_dict[alias]
#                
#        # Delete parameters from self.kwargs
#        for param in arglist:
#            if param not in self._default_kwargs:
#                self.kwargs.pop(param, None)
                
#    def set_font(self, family=None, weight=None, size=None):
#        """ Updates global font properties for all plot elements
#        
#        TODO: Font family and weight don't update dynamically"""
#        if family is None:
#            family = mpl.rcParams['font.family']
#        if weight is None:
#            weight = mpl.rcParams['font.weight']
#        if size is None:
#            size = mpl.rcParams['font.size']
#        mpl.rc('font', family=family, weight=weight, size=size)
#        self.redraw()
        
    def _delete_uniqueparams(self):
        """Delete plot parameters that are unique per plot
        
        Prevents unique parameters (eg: label) carrying over to future plots"""
        for param in self._uniqueparams:
            self.kwargs.pop(param, None)
        
    def _update(self, *args, **kwargs):
        """Update instance variables args and kwargs with supplied values """
        if args:
            self.args = args # Args to be directly passed to plot command
            self.isnewargs = True
        else:
            self.isnewargs = False
        # Update self.kwargs with full parameter name of aliased plot parameter
        for alias in self.alias_dict:
            if alias in kwargs:
                self.kwargs[self.alias_dict[alias]] = kwargs.pop(alias)
            
        # Update kwargs dictionary
        for key in kwargs:
            self.kwargs[key] = kwargs[key]
           
    def _reset(self, reset=False):
        """Reset instance variables in preparation for new plots
        reset: True if current instance defaults for plotting parameters should
               be reset to Class defaults"""
        self.args = []
        self.line_list = []
        if reset:
            self.kwargs = self._default_kwargs.copy()