venv:
		uv venv  

dependencies: venv 
	uv pip install pandas
	uv pip install -r requirements.txt


describe:
	uv run python src/describe.py datasets/dataset_train.csv


histogram:
	uv run python src/histogram.py
