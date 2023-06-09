pdm:
	powershell.exe hack/pdm-install.ps1

test:
	cd tests && python -m unittest

install:
	pip install -r requirements.txt

run:
	python -m cvapr.boilerplate