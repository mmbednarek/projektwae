.PHONY: test plots clean

test:
	python2 -m unittest projektwae.tests

plots:
	Rscript make_plots.r

clean:
	rm logs/*
	rm plots/optimum_error/*
	rm plots/value_error/*
