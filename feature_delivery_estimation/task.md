# Feature Delivery Estimation

## Задача

Подготовить оценку сроков разработки функций (features) модуля Output Formatting.

## Исходные данные

### Категории оценки времени:
- **Large** — assumes days
- **Medium** — from hours to a couple of days  
- **Small** — hours

### Список функций (11 задач):

**T1.** Universal "Save As" dialog (Large Frontend + Medium Backend)
**T2.** Template-based export (Large Backend + Small Frontend)
**T3.** Site Plan scale options (Medium Frontend + Medium Backend)
**T4.** CAD export formats with proper layer structure (Small Backend)
**T5.** Revit-optimized DWG export (Medium Backend)
**T6.** GIS export formats (Large Backend)
**T7.** ALTA/NSPS compliance (Medium/Large Backend)
**T8.** Color and black-white toggle (Small Frontend + Small Backend)
**T9.** Dynamic legend generation (Small Backend)
**T10.** Interactive PDF and SketchUp export (Large Backend)
**T11.** Site Plan AI Q&A integration (Small Backend) — ⚠️ заблокирована

### Зависимости:
- T1 — независимая
- T2 — зависит от T1 (интеграция)
- T3-T6 — независимые
- T7 — может зависеть от T4-T6
- T8 — зависит от T4-T6
- T9-T11 — независимые