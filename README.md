# Курс «Робототехника · ROS 2»

Репозиторий практических работ по курсу робототехники (НГУ).

---

## ПР03. Первая нода: поза и команда

### Цель работы
Создание и сборка Python-пакета `patrol` с управляющей нодой `patrol_node`. Реализация подписки на топик `/turtle1/pose` (`turtlesim/msg/Pose`), периодической публикации управляющих команд в относительный топик `cmd_vel` (`geometry_msgs/msg/Twist`) по таймеру с частотой 10 Гц (0.1 с), модульное тестирование логики вычисления скоростей (`compute_cmd_vel`), а также исследование механизма переназначения топиков (remap) для связи относительного имени `cmd_vel` с `/turtle1/cmd_vel`.

---

### Порядок локального воспроизведения ПР03

#### 1. Сборка пакетов
```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select turtle_bringup patrol
source install/setup.bash
```

#### 2. Запуск тестов
```bash
python3 -s -m pytest src/patrol/test
```

#### 3. Запуск симулятора
```bash
export ROS_DOMAIN_ID=16
ros2 launch turtle_bringup sim.launch.py
```

#### 4. Воспроизведение дефекта относительного имени топика
```bash
# Получение начальной позы черепахи:
ros2 topic echo /turtle1/pose --once

# Запуск ноды патрулирования без ремапа:
export ROS_DOMAIN_ID=16
ros2 run patrol patrol

# Проверка конечных точек топиков в отдельном терминале:
ros2 topic info /cmd_vel --verbose          # Subscription count: 0 (нет подписчиков)
ros2 topic info /turtle1/cmd_vel --verbose  # Subscription count: 1, Publisher count: 0

# Проверка позы (черепаха остаётся на месте):
ros2 topic echo /turtle1/pose --once
```

#### 5. Устранение дефекта с помощью переназначения (remap)
```bash
# Запуск ноды с ремапом топика cmd_vel на /turtle1/cmd_vel:
export ROS_DOMAIN_ID=16
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel

# Проверка связности конечных точек:
ros2 topic info /turtle1/cmd_vel --verbose  # Subscription count: 1, Publisher count: 1

# Замер частоты публикации команд:
ros2 topic hz /turtle1/cmd_vel

# Проверка изменившейся позы (черепаха движется по окружности):
ros2 topic echo /turtle1/pose --once
```

---

### Автоматическая проверка
```bash
python3 .course-kit/v1/tools/check_practice.py PR03 --submission .
```
