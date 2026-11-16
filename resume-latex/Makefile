LATEXMK ?= latexmk
LATEXMK_FLAGS = -xelatex -interaction=nonstopmode -halt-on-error -outdir=build

.PHONY: all llm full

all: llm full

llm:
	$(LATEXMK) $(LATEXMK_FLAGS) resume_llm.tex

full:
	$(LATEXMK) $(LATEXMK_FLAGS) resume2.tex
