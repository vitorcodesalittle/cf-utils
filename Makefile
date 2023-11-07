# To see what the make can do in this project
# run make `help`

##@ Dependencies
OUTPUT_DIR = dist/
SRC = cf.py

build: $(SRC)
	pip install build
	python -m build --wheel --outdir $(OUTPUT_DIR) .

install: $(OUTPUT_DIR)
	echo 'Y ' | python -m pip uninstall $(OUTPUT_DIR)/*.whl
	python -m pip install $(OUTPUT_DIR)/*.whl

clean:
	rm -rf $(OUTPUT_DIR)
	rm -rf build/
	rm -rf cf_vlma.egg-info


