# API Integration Package: Takeoff ↔ Estimator

## Задача
Создать документацию и demo приложения для интеграции двух AEC сервисов:
- Takeoff Service (измерения на чертежах)
- Estimator Service (оценка стоимости)

## Цель
Подготовить минимальный, но понятный пакет для технического руководителя и разработчиков.

## Исходные данные
- OpenAPI спецификация с эндпойнтами и моделями данных
- Опечатка: PostAllConditionsState должен быть GetAllConditionsState (метод GET)

## Deliverables
1. Документация (README + sequence/ER диаграммы)
2. Исправленная OpenAPI спецификация
3. Два FastAPI demo приложения с in-memory данными
4. Примеры запросов

## Технические требования
- Python/FastAPI
- Swagger UI автогенерация
- Happy path only
- Без overengineering