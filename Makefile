pdm:
	powershell.exe hack/pdm-install.ps1

test:
	cd tests && python -m unittest

install:
	pdm install

run:
	python -m cvapr.boilerplate