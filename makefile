.PHONY: install run run-csv run-verlet run-luna test test-pure clean help

# En Windows usamos 'python', en Linux/Mac usan 'python3'.
# Si en Windows el comando 'python3' no funciona, cámbialo a 'python'.
PYTHON := python

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) main.py

run-csv:
	$(PYTHON) main.py --salida csv

run-verlet:
	$(PYTHON) main.py --metodo verlet

run-luna:
	$(PYTHON) main.py --g 1.62

test:
	$(PYTHON) -m pytest tests/ -v

test-pure:
	$(PYTHON) -m venv .venv_pure
	.venv_pure\Scripts\pip install pytest -q
	.venv_pure\Scripts\pytest tests/test_dominio.py -v
	@echo "OK — el dominio pasa sin numpy ni matplotlib"

clean:
	for /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul || true
	del /q resultados.csv 2>nul || true
