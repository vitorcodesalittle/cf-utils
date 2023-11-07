# To see what the make can do in this project
# run make `help`

##@ Dependencies
BUILD_DIR = dist/
SRC = cf.py requirements.txt pyproject.toml

build: $(SRC)
	pip install build
	python -m build --wheel --outdir $(BUILD_DIR) .

install: $(BUILD_DIR)
	echo 'Y ' | python -m pip uninstall $(BUILD_DIR)/*.whl
	python -m pip install $(BUILD_DIR)/*.whl

clean:
	rm -rf $(BUILD_DIR)
	rm -rf build/
	rm -rf cf_vlma.egg-info


