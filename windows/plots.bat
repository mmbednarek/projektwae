cd %~dp0..
del /Q plots\optimum_error\*
del /Q plots\value_error\*

RScript make_plots.r
