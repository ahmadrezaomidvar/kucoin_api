
install:
	conda env create -f environment.yml

auto_sell:
	python auto_sell.py

time_based_sell:
	python time_based_sell.py