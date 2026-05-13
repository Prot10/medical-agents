TEX     := neurobench_v5
FIGURES := figures/condition_distribution.pdf \
           figures/difficulty_pie.pdf         \
           figures/demographics.pdf           \
           figures/encounter_and_followups.pdf \
           figures/tool_usage.pdf             \
           figures/groundtruth_structure.pdf

.PHONY: all figures clean distclean

all: $(TEX).pdf

figures: $(FIGURES)

$(FIGURES): make_figures.py
	cd .. && uv run python presentations/neurobench_v5/make_figures.py

$(TEX).pdf: $(TEX).tex $(FIGURES)
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(TEX).tex

clean:
	latexmk -c $(TEX).tex || true
	rm -f $(TEX).{aux,log,nav,out,snm,toc,vrb,bbl,blg,fdb_latexmk,fls}

distclean: clean
	rm -f $(TEX).pdf
