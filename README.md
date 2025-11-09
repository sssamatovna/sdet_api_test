# Автотесты для API

---
## 📝 Описание
Проект для автоматизации тестирования раздела "Manager" на сайте
https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager
Реализован с использованием Selenium WebDriver, Pytest и Allure Reports по паттерну Page Object Model. 

## 🚀 Технологии 
- Python 3.10+
- Pytest
- Requests
- Pydantic
- Allure Report
- pytest-xdist
- python-dotenv

## ⚙️ Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/sssamatovna/sdet_api_test.git
    cd sdet_api_test
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    # Для Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Для macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройте переменные окружения:**
    Скопируйте файл `.env.example` в новый файл с именем `.env` и при необходимости измените значение `API_HOST`.
    ```bash
    # Для Windows
    copy .env.example .env

    # Для macOS / Linux
    cp .env.example .env
    ```
    
##  ▶️ Запуск тестов

### Простой запуск

Выполняет все тесты в одном потоке.
```bash
pytest
```

### Параллельный запуск

Запускает тесты в несколько потоков.
```bash
pytest -n auto
```

### Запуск с генерацией Allure-отчета

1.  **Выполните тесты и соберите результаты:**
    ```bash
    pytest --alluredir=allure-results -n auto
    ```

2.  **Сгенерируйте и откройте HTML-отчет:**
    (Требуется установленный [Allure Commandline](https://docs.qameta.io/allure/#_installing_a_commandline))
    ```bash
    allure serve allure-results

## ⚙️ CI/CD

Проект настроен для автоматического запуска тестов с помощью GitHub Actions. 