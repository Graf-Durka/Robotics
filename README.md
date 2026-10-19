# Курс «Робототехника · ROS 2»

Репозиторий практических работ по курсу робототехники (НГУ).

---

## ПР06. Модель робота, tf2 и QoS преобразований

### Цель работы
Создание пакета описания кинематической модели робота `course_description` с описанием на базе Xacro (`vehicle.urdf.xacro`) для колёсного шасси с рулевым управлением Аккермана. Модель параметризует базу колёс (`wheel_base = 0.8`), колею (`wheel_separation = 0.62`), радиус колеса (`wheel_radius = 0.12`), кузов и сенсорный обвес (`camera_link`, `lidar_link`, `imu_link`). Реализация launch-файла `display.launch.py` с узлом `robot_state_publisher`, исследование поведения QoS топика `/tf_static` (`transient_local` vs `volatile`), воспроизведение и исправление дефекта привязки дерева трансформаций (неверный родительский фрейм для `lidar_link`).

---

### Структура пакета `course_description`
- `urdf/vehicle.urdf.xacro`: параметризованная кинематическая модель робота и сенсоров.
- `launch/display.launch.py`: запуск публикации дерева tf через `robot_state_publisher`.
- `test/test_urdf.py`: автоматические тесты структуры URDF, параметров геометрии и иерархии фреймов.

---

### Порядок локального воспроизведения ПР06

#### 1. Сборка пакетов
```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select turtle_bringup patrol course_bringup course_description
source install/setup.bash
```

#### 2. Запуск тестов
```bash
python3 -s -m pytest src/patrol/test
python3 -s -m pytest src/course_bringup/test
python3 -s -m pytest src/turtle_bringup/test
python3 -s -m pytest src/course_description/test
```

#### 3. Проверка синтаксиса и структуры URDF
```bash
xacro src/course_description/urdf/vehicle.urdf.xacro > /tmp/vehicle.urdf
check_urdf /tmp/vehicle.urdf
```

#### 4. Запуск robot_state_publisher и проверка QoS /tf_static
```bash
# В терминале 1:
ros2 launch course_description display.launch.py

# В терминале 2:
# 1. Проверка информации о топике:
ros2 topic info /tf_static --verbose

# 2. Получение статических трансформаций с durability transient_local (успешно, exit=0):
timeout 4 ros2 topic echo /tf_static --once --qos-durability transient_local --qos-reliability reliable; echo "exit=$?"

# 3. Попытка чтения с durability volatile (сообщения отбрасываются, таймаут, exit=124):
timeout 4 ros2 topic echo /tf_static --once --qos-durability volatile --qos-reliability reliable; echo "exit=$?"
```

---

### Автоматическая проверка
```bash
python3 .course-kit/v1/tools/check_practice.py PR06 --submission .
```
