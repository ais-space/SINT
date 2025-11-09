SINT V2.2: Универсальный Интерактивный Каскадный Процессор (5 Кейсов)

ЦЕЛЬ: Обеспечивает интерактивную генерацию, выполнение и архивирование 5 SINT-кейсов в режиме диалога.
ЯЗЫК: Все сгенерированные документы (задачи, FD, SINT промпты, вывод) ДОЛЖНЫ БЫТЬ на английском языке.
РЕЖИМ: Выполняется в интерактивной среде (диалоговая система).

# -----------------------------------------------------------------------------
# ЭТАП 0: ИНИЦИАЛИЗАЦИЯ И ПРОВЕРКА ГОТОВНОСТИ
# -----------------------------------------------------------------------------

Действие 0.0: Создание чек-листа выполнения этого промпта
Описание: Проверьте существование вспомогательного файла checklist.md. При его наличии очистите содержимое, при его отсутствии создайте его. Заполните его подробным иерархическим списком шагов по выполнению этого промпта с возможностью отметки выполнения каждого шага.
Ожидаемый результат: Файл checklist.md существует и он правильно заполнен
ПРОВЕРКА: Убедитесь, что checklist.md существует и он правильно заполнен
ВАЖНО: Обязательно и всегда только после выполнения каждого шага отмечайте в файле выполненный шаг
Дополнительно: Поставить отметку в чек-лист

Действие 0.1: Создание корневой директории
Описание: Создайте директорию MyCases, если она не существует
Ожидаемый результат: Директория MyCases существует
ПРОВЕРКА: Убедитесь, что директория MyCases существует
Дополнительно: Поставить отметку в чек-лист

Действие 0.2: Проверка наличия файлов промптов
Описание: Убедитесь, что файлы SP1_Designer_CLI_RU.md и SP2_Coder_CLI_RU.md доступны в системе
Ожидаемый результат: Файлы промптов существуют и доступны
ВАЖНО: Если файлы отсутствуют, процесс не должен продолжаться
Дополнительно: Поставить отметку в чек-лист

Действие 0.3: Проверка чистоты директории MyCases
Описание: Убедитесь, что директория MyCases не содержит результатов предыдущих запусков, если запуск производится с нуля
Ожидаемый результат: Подготовленная чистая среда выполнения
Дополнительно: Поставить отметку в чек-лист

Действие 0.4: Проверка чек-листа выполнения этого промпта
Описание: Убедитесь, что в чек-листе checklist.md отмечено выполнение всех предыдущих шагов
Ожидаемый результат: В чек-листе отмечено выполнение всех предыдущих шагов

# -----------------------------------------------------------------------------
# ЭТАП 1: ОКРУЖЕНИЕ И НАСТРОЙКА ПЕРЕМЕННЫХ
# -----------------------------------------------------------------------------

Действие 1.1: Подготовка поддиректорий
Описание: Создайте 5 поддиректорий в MyCases/: Case1, Case2, Case3, Case4, Case5
Ожидаемый результат: Все 5 поддиректорий существуют
ПРОВЕРКА: Убедитесь, что все 5 поддиректорий созданы
Дополнительно: Поставить отметку в чек-лист

# META_TASK_INPUT: Содержимое первой задачи (Кейс 1), встроенное для автономности сценария.
# Явно указывает LLM генерировать весь вывод на английском языке.

META_TASK_INPUT_CONTENT:
Request Type: System Design Request (SINT System Designer V2.2)
Project Name: Generation of Diverse Complex Analytical Tasks
Customer: SINT Research Laboratory
1.0. Objective: Generate a single, detailed, and technically complete Formal Definition (FD), which will be used by the 'Code Generator' agent to create a SINT prompt that in turn should generate 4 different complex analytical tasks, each requiring a unique interdisciplinary approach with detailed expert analysis, numerical ratings, iterative convergence, and comprehensive synthesis.
2.0. Context: The generated tasks should cover fundamentally different areas of knowledge, require various sets of experts and methodologies, demonstrate the broad spectrum of SINT framework capabilities, and require highly detailed analysis with numerical ratings and iterative synthesis.
2.3.2. Task Specification (Generation Result): The 4 generated tasks must strictly demonstrate the following SINT modes: Task 1 (Case 2): Debates (N=3) + Conflict (Step 3A) with detailed expert positions, numerical ratings (1-10), cross-criticism, and iterative convergence. Task 2 (Case 3): Debates (N=3) + Consensus (Step 3B) with structured rating system, detailed arguments, and multi-round synthesis. Task 3 (Case 4): Generator + Critic (N=2) with comprehensive feedback loops and detailed analysis. Task 4 (Case 5): Debates (N=4) + Conflict (Step 3A) with numerical ratings, cross-evaluation, and iterative synthesis.
3.0. Constraints: Each of the 4 tasks must require a separate full SINT application. All tasks must be fundamentally different in thematic and approaches. All tasks must be formulated considering the principle of contextual grounding (PCG). Each task must have clearly defined objectives and expected outcomes. All expert positions must include detailed arguments, numerical ratings (1-10), cross-evaluation scores, and specific examples. The output must include multiple rounds of criticism, iterative convergence, and comprehensive synthesis.
4.0. Language Constraint: All output (including 4 generated tasks) MUST BE in English.
4.1. Analysis Requirements: Each expert must provide detailed, specific arguments with concrete examples, data points, and numerical ratings. The process must include iterative rounds of criticism and synthesis with detailed cross-evaluation between experts.

# -----------------------------------------------------------------------------
# ЭТАП 2: ПОЛНЫЙ SINT-ЦИКЛ ДЛЯ КЕЙСА 1 (СПЕЦИАЛЬНЫЙ СЛУЧАЙ)
# ПРЕДУПРЕЖДЕНИЕ: Case1 использует META_TASK_INPUT_CONTENT напрямую в SP1, а не task.txt
# ПРЕДУПРЕЖДЕНИЕ: Из результата Case1 (output_raw.xml) будут извлечены 4 задачи для Cases 2-5
# -----------------------------------------------------------------------------

Действие 2.1: Запуск SP1 (System Designer) для Кейса 1
Входные данные:
- SP1_Designer_CLI_RU.md (Промпт 1)
- META_TASK_INPUT_CONTENT (содержимое из вышеуказанного блока)
Описание:
- Загрузите содержимое SP1_Designer_CLI_RU.md
- Обработайте META_TASK_INPUT_CONTENT с помощью SP1_Designer
- Сохраните результат в MyCases/Case1/fd.xml
Ожидаемый результат: Файл MyCases/Case1/fd.xml содержит формализованное задание, созданное SP1_Designer на основе META_TASK_INPUT_CONTENT
ПРОВЕРКА: Убедитесь, что MyCases/Case1/fd.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 2.2: Запуск SP2 (Code Generator) для Кейса 1
Входные данные:
- SP2_Coder_CLI_RU.md (Промпт 2)
- MyCases/Case1/fd.xml (результат Действия 2.1)
Описание:
- Загрузите содержимое SP2_Coder_CLI_RU.md
- Загрузите содержимое MyCases/Case1/fd.xml
- Выполните сессию 2 (SINT Code Generator) с fd.xml в качестве входных данных
- Сохраните результат в MyCases/Case1/sint_prompt.txt
Ожидаемый результат: Файл MyCases/Case1/sint_prompt.txt содержит SINT-промпт для Case1
ПРОВЕРКА: Убедитесь, что MyCases/Case1/sint_prompt.txt существует
Дополнительно: Поставить отметку в чек-лист

Действие 2.3: Запуск Executor для Кейса 1
Входные данные:
- MyCases/Case1/sint_prompt.txt (результат Действия 2.2)
Описание:
- Загрузите содержимое MyCases/Case1/sint_prompt.txt
- Выполните сессию 3 (SINT Executor) с промптом
- Сохраните результат в MyCases/Case1/output_raw.xml
Ожидаемый результат: Файл MyCases/Case1/output_raw.xml содержит результаты выполнения, включая 4 дополнительные задачи
ПРОВЕРКА: Убедитесь, что MyCases/Case1/output_raw.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 2.4: Разбор 4 задач и сохранение в task.txt файлы (Cases 2-5)
Входные данные:
- MyCases/Case1/output_raw.xml (результат Действия 2.3)
Описание:
- Извлеките 4 отдельных задачи из MyCases/Case1/output_raw.xml
- Сохраните задачу 1 в MyCases/Case2/task.txt
- Сохраните задачу 2 в MyCases/Case3/task.txt
- Сохраните задачу 3 в MyCases/Case4/task.txt
- Сохраните задачу 4 в MyCases/Case5/task.txt
Ожидаемый результат: 4 файла task.txt созданы с соответствующими задачами (для Cases 2-5)
ПРОВЕРКА: Убедитесь, что все 4 task.txt файлов (для Cases 2-5) существуют и содержат задачи
Дополнительно: Поставить отметку в чек-лист

Действие 2.5: Проверка чек-листа выполнения этого промпта
Описание: Убедитесь, что в чек-листе checklist.md отмечено выполнение всех предыдущих шагов
Ожидаемый результат: В чек-листе отмечено выполнение всех предыдущих шагов

# -----------------------------------------------------------------------------
# ЭТАП 3: ПОЛНЫЕ SINT-ЦИКЛЫ ДЛЯ ОСТАВШИХСЯ КЕЙСОВ (2-5)
# ПРЕДУПРЕЖДЕНИЕ: Выполняйте каждый подэтап ТОЛЬКО ПОСЛЕ завершения предыдущего
# ПРЕДУПРЕЖДЕНИЕ: Каждый подэтап использует СВОЙ task.txt файл (Cases 2-5)
# ПРЕДУПРЕЖДЕНИЕ: Case1 уже завершен, этот этап обслуживает только Cases 2-5
# -----------------------------------------------------------------------------

# ПОДЭТАП 3.1: Обработка Кейса 2
# ВХОДНЫЕ ДАННЫЕ: MyCases/Case2/task.txt (извлекается из MyCases/Case1/output_raw.xml на этапе 2.4)
Действие 3.1.1: Запуск SP1 (System Designer) для Кейса 2
Входные данные:
- MyCases/Case2/task.txt (результат Действия 2.4)
- SP1_Designer_CLI_RU.md (Промпт 1)
Описание:
- Загрузите содержимое MyCases/Case2/task.txt
- Загрузите содержимое SP1_Designer_CLI_RU.md
- Выполните сессию 1 (SINT System Designer) с task.txt в качестве входных данных
- Сохраните результат в MyCases/Case2/fd.xml
Ожидаемый результат: Файл MyCases/Case2/fd.xml содержит результаты сессии 1 для задачи 2
ПРОВЕРКА: Убедитесь, что MyCases/Case2/fd.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.1.2: Запуск SP2 (Code Generator) для Кейса 2
Входные данные:
- MyCases/Case2/fd.xml (результат Действия 3.1.1)
- SP2_Coder_CLI_RU.md (Промпт 2)
Описание:
- Загрузите содержимое MyCases/Case2/fd.xml
- Загрузите содержимое SP2_Coder_CLI_RU.md
- Выполните сессию 2 (SINT Code Generator) с fd.xml в качестве входных данных
- Сохраните результат в MyCases/Case2/sint_prompt.txt
Ожидаемый результат: Файл MyCases/Case2/sint_prompt.txt содержит SINT-промпт для задачи 2
ПРОВЕРКА: Убедитесь, что MyCases/Case2/sint_prompt.txt существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.1.3: Запуск Executor для Кейса 2
Входные данные:
- MyCases/Case2/sint_prompt.txt (результат Действия 3.1.2)
Описание:
- Загрузите содержимое MyCases/Case2/sint_prompt.txt
- Выполните сессию 3 (SINT Executor) с промптом
- Сохраните результат в MyCases/Case2/output.xml
Ожидаемый результат: Файл MyCases/Case2/output.xml содержит финальный результат для задачи 2
ПРОВЕРКА: Убедитесь, что MyCases/Case2/output.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.1.4: Проверка чек-листа выполнения этого промпта
Описание: Убедитесь, что в чек-листе checklist.md отмечено выполнение всех предыдущих шагов
Ожидаемый результат: В чек-листе отмечено выполнение всех предыдущих шагов

# ПОДЭТАП 3.2: Обработка Кейса 3
# ВХОДНЫЕ ДАННЫЕ: MyCases/Case3/task.txt (извлекается из MyCases/Case1/output_raw.xml на этапе 2.4)
Действие 3.2.1: Запуск SP1 (System Designer) для Кейса 3
Входные данные:
- MyCases/Case3/task.txt (результат Действия 2.4)
- SP1_Designer_CLI_RU.md (Промпт 1)
Описание:
- Загрузите содержимое MyCases/Case3/task.txt
- Загрузите содержимое SP1_Designer_CLI_RU.md
- Выполните сессию 1 (SINT System Designer) с task.txt в качестве входных данных
- Сохраните результат в MyCases/Case3/fd.xml
Ожидаемый результат: Файл MyCases/Case3/fd.xml содержит результаты сессии 1 для задачи 3
ПРОВЕРКА: Убедитесь, что MyCases/Case3/fd.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.2.2: Запуск SP2 (Code Generator) для Кейса 3
Входные данные:
- MyCases/Case3/fd.xml (результат Действия 3.2.1)
- SP2_Coder_CLI_RU.md (Промпт 2)
Описание:
- Загрузите содержимое MyCases/Case3/fd.xml
- Загрузите содержимое SP2_Coder_CLI_RU.md
- Выполните сессию 2 (SINT Code Generator) с fd.xml в качестве входных данных
- Сохраните результат в MyCases/Case3/sint_prompt.txt
Ожидаемый результат: Файл MyCases/Case3/sint_prompt.txt содержит SINT-промпт для задачи 3
ПРОВЕРКА: Убедитесь, что MyCases/Case3/sint_prompt.txt существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.2.3: Запуск Executor для Кейса 3
Входные данные:
- MyCases/Case3/sint_prompt.txt (результат Действия 3.2.2)
Описание:
- Загрузите содержимое MyCases/Case3/sint_prompt.txt
- Выполните сессию 3 (SINT Executor) с промптом
- Сохраните результат в MyCases/Case3/output.xml
Ожидаемый результат: Файл MyCases/Case3/output.xml содержит финальный результат для задачи 3
ПРОВЕРКА: Убедитесь, что MyCases/Case3/output.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.2.4: Проверка чек-листа выполнения этого промпта
Описание: Убедитесь, что в чек-листе checklist.md отмечено выполнение всех предыдущих шагов
Ожидаемый результат: В чек-листе отмечено выполнение всех предыдущих шагов

# ПОДЭТАП 3.3: Обработка Кейса 4
# ВХОДНЫЕ ДАННЫЕ: MyCases/Case4/task.txt (извлекается из MyCases/Case1/output_raw.xml на этапе 2.4)
Действие 3.3.1: Запуск SP1 (System Designer) для Кейса 4
Входные данные:
- MyCases/Case4/task.txt (результат Действия 2.4)
- SP1_Designer_CLI_RU.md (Промпт 1)
Описание:
- Загрузите содержимое MyCases/Case4/task.txt
- Загрузите содержимое SP1_Designer_CLI_RU.md
- Выполните сессию 1 (SINT System Designer) с task.txt в качестве входных данных
- Сохраните результат в MyCases/Case4/fd.xml
Ожидаемый результат: Файл MyCases/Case4/fd.xml содержит результаты сессии 1 для задачи 4
ПРОВЕРКА: Убедитесь, что MyCases/Case4/fd.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.3.2: Запуск SP2 (Code Generator) для Кейса 4
Входные данные:
- MyCases/Case4/fd.xml (результат Действия 3.3.1)
- SP2_Coder_CLI_RU.md (Промпт 2)
Описание:
- Загрузите содержимое MyCases/Case4/fd.xml
- Загрузите содержимое SP2_Coder_CLI_RU.md
- Выполните сессию 2 (SINT Code Generator) с fd.xml в качестве входных данных
- Сохраните результат в MyCases/Case4/sint_prompt.txt
Ожидаемый результат: Файл MyCases/Case4/sint_prompt.txt содержит SINT-промпт для задачи 4
ПРОВЕРКА: Убедитесь, что MyCases/Case4/sint_prompt.txt существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.3.3: Запуск Executor для Кейса 4
Входные данные:
- MyCases/Case4/sint_prompt.txt (результат Действия 3.3.2)
Описание:
- Загрузите содержимое MyCases/Case4/sint_prompt.txt
- Выполните сессию 3 (SINT Executor) с промптом
- Сохраните результат в MyCases/Case4/output.xml
Ожидаемый результат: Файл MyCases/Case4/output.xml содержит финальный результат для задачи 4
ПРОВЕРКА: Убедитесь, что MyCases/Case4/output.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.3.4: Проверка чек-листа выполнения этого промпта
Описание: Убедитесь, что в чек-листе checklist.md отмечено выполнение всех предыдущих шагов
Ожидаемый результат: В чек-листе отмечено выполнение всех предыдущих шагов

# ПОДЭТАП 3.4: Обработка Кейса 5
# ВХОДНЫЕ ДАННЫЕ: MyCases/Case5/task.txt (извлекается из MyCases/Case1/output_raw.xml на этапе 2.4)
Действие 3.4.1: Запуск SP1 (System Designer) для Кейса 5
Входные данные:
- MyCases/Case5/task.txt (результат Действия 2.4)
- SP1_Designer_CLI_RU.md (Промпт 1)
Описание:
- Загрузите содержимое MyCases/Case5/task.txt
- Загрузите содержимое SP1_Designer_CLI_RU.md
- Выполните сессию 1 (SINT System Designer) с task.txt в качестве входных данных
- Сохраните результат в MyCases/Case5/fd.xml
Ожидаемый результат: Файл MyCases/Case5/fd.xml содержит результаты сессии 1 для задачи 5
ПРОВЕРКА: Убедитесь, что MyCases/Case5/fd.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.4.2: Запуск SP2 (Code Generator) для Кейса 5
Входные данные:
- MyCases/Case5/fd.xml (результат Действия 3.4.1)
- SP2_Coder_CLI_RU.md (Промпт 2)
Описание:
- Загрузите содержимое MyCases/Case5/fd.xml
- Загрузите содержимое SP2_Coder_CLI_RU.md
- Выполните сессию 2 (SINT Code Generator) с fd.xml в качестве входных данных
- Сохраните результат в MyCases/Case5/sint_prompt.txt
Ожидаемый результат: Файл MyCases/Case5/sint_prompt.txt содержит SINT-промпт для задачи 5
ПРОВЕРКА: Убедитесь, что MyCases/Case5/sint_prompt.txt существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.4.3: Запуск Executor для Кейса 5
Входные данные:
- MyCases/Case5/sint_prompt.txt (результат Действия 3.4.2)
Описание:
- Загрузите содержимое MyCases/Case5/sint_prompt.txt
- Выполните сессию 3 (SINT Executor) с промптом
- Сохраните результат в MyCases/Case5/output.xml
Ожидаемый результат: Файл MyCases/Case5/output.xml содержит финальный результат для задачи 5
ПРОВЕРКА: Убедитесь, что MyCases/Case5/output.xml существует
Дополнительно: Поставить отметку в чек-лист

Действие 3.4.4: Проверка чек-листа выполнения этого промпта
Описание: Убедитесь, что в чек-листе checklist.md отмечено выполнение всех предыдущих шагов
Ожидаемый результат: В чек-листе отмечено выполнение всех предыдущих шагов

# -----------------------------------------------------------------------------
# ЭТАП 4: ФИНАЛИЗАЦИЯ И ПРОВЕРКА ЦЕЛОСТНОСТИ
# -----------------------------------------------------------------------------

Действие 4.1: Проверка полноты результатов
Описание: Убедитесь, что все файлы результатов существуют:
- Для Case1: fd.xml, sint_prompt.txt, output_raw.xml (без task.txt)
- Для Cases 2-5: по 3 файла (fd.xml, sint_prompt.txt, output.xml) для каждого
Файлы для проверки:
- MyCases/Case1/fd.xml
- MyCases/Case1/sint_prompt.txt
- MyCases/Case1/output_raw.xml
- MyCases/Case2/fd.xml
- MyCases/Case2/sint_prompt.txt
- MyCases/Case2/output.xml
- MyCases/Case2/task.txt
- MyCases/Case3/fd.xml
- MyCases/Case3/sint_prompt.txt
- MyCases/Case3/output.xml
- MyCases/Case3/task.txt
- MyCases/Case4/fd.xml
- MyCases/Case4/sint_prompt.txt
- MyCases/Case4/output.xml
- MyCases/Case4/task.txt
- MyCases/Case5/fd.xml
- MyCases/Case5/sint_prompt.txt
- MyCases/Case5/output.xml
- MyCases/Case5/task.txt
Ожидаемый результат: Все 19 файлов существуют
Дополнительно: Поставить отметку в чек-лист

Действие 4.2: Проверка чек-листа выполнения этого промпта
Описание: Убедитесь, что в чек-листе checklist.md отмечено выполнение всех предыдущих шагов
Ожидаемый результат: В чек-листе отмечено выполнение всех предыдущих шагов

Финальное сообщение: "SINT Cascade Validation успешно завершена. Результаты сохранены в MyCases/."
Дополнительно: Поставить отметку в чек-лист

# -----------------------------------------------------------------------------
# ОБРАБОТКА ОШИБОК И ОТКАТ
# -----------------------------------------------------------------------------

# Если на любом этапе произошла ошибка:
# 1. Зафиксируйте ошибку и причину
# 2. При необходимости очистите частично созданные файлы
# 3. Вернитесь к последней проверенной точке
# 4. Продолжите выполнение после устранения причины ошибки

# -----------------------------------------------------------------------------
# ДОПОЛНЕНИЕ: ИНТЕРАКТИВНОЕ ИСПОЛЬЗОВАНИЕ
# -----------------------------------------------------------------------------

1. Начните с META_TASK_INPUT
2. Выполняйте каждый этап по запросу пользователя
3. Все результаты сохраняются в формате, подходящем для диалога
4. Переходите к следующему этапу только после завершения предыдущего и прохождения проверки
5. Особое внимание уделите Case1: он использует META_TASK_INPUT_CONTENT напрямую, а не task.txt

Этот универсальный промпт можно использовать:
- В CLI системах с поддержкой диалога
- В интерактивных сессиях с LLM
- В системах командной строки с поддержкой многократных взаимодействий
- В любом инструменте, поддерживающем диалоговый режим работы