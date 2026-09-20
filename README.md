# Курс «Робототехника · ROS 2»

Репозиторий практических работ по курсу робототехники (НГУ).

---

## ПР01. Окружение и граф ROS 2

### Цель работы
Исследование графа вычислений ROS 2 (`turtlesim`), анализ механизма обнаружения узлов (DDS Discovery) и изоляции взаимодействия через `ROS_DOMAIN_ID`.

---

### Порядок локального воспроизведения

#### 1. Подготовка терминалов
В терминалах настраивается окружение ROS 2 Jazzy и задаётся базовый домен:
```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=16
```

#### 2. Запуск исправного графа
- **Терминал A (симулятор):**
  ```bash
  ros2 run turtlesim turtlesim_node
  ```
- **Терминал B (телеуправление с клавиатуры):**
  ```bash
  ros2 run turtlesim turtle_teleop_key
  ```
- **Терминал C (диагностика графа):**
  ```bash
  ros2 node list --no-daemon --spin-time 2
  ros2 topic list -t
  ros2 node info /turtlesim
  ros2 topic type /turtle1/pose
  ros2 topic echo /turtle1/pose --once
  ros2 topic hz /turtle1/pose
  ```

#### 3. Воспроизведение дефекта (изоляция доменов)
- В **Терминале B** перезапуск teleop в домене 17:
  ```bash
  export ROS_DOMAIN_ID=17
  ros2 run turtlesim turtle_teleop_key
  ```
- В **Терминале C** попытка чтения позы в домене 17 (ожидается таймаут 5 с, код завершения 124):
  ```bash
  export ROS_DOMAIN_ID=17
  timeout 5s ros2 topic echo /turtle1/pose turtlesim/msg/Pose --once
  ```

#### 4. Восстановление связи
- В **Терминале B** возврат в домен 16:
  ```bash
  export ROS_DOMAIN_ID=16
  ros2 run turtlesim turtle_teleop_key
  ```
- В **Терминале C** чтение позы в домене 16 (поза успешно получена, код 0):
  ```bash
  export ROS_DOMAIN_ID=16
  timeout 5s ros2 topic echo /turtle1/pose turtlesim/msg/Pose --once
  ```

---

### Автоматическая проверка
Проверка соответствия контракту сдачи:
```bash
python3 .course-kit/v1/tools/check_practice.py PR01 --submission .
```
