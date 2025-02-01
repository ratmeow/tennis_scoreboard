что нужно сделать
-руфф
-деплой


В качестве линтера используется `ruff`. Также он используется для форматирования кода.
Ниже приведены примеры команд для проверки кода ruff'ом.
```shell
ruff check src/ --select I
ruff check tests/ --select I
ruff check src/ --ignore F821
ruff check tests/
ruff format --check src/
ruff format --check tests/
```
Для автоматического исправления кода для `ruff check` нужно добавить `--fix`.
Для форматирования кода в `ruff format` нужно убрать флаг `--check`.