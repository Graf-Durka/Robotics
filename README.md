# Курс «Робототехника · ROS 2»

Репозиторий практических работ по курсу робототехники (НГУ).

---

## ПР05. Launch, QoS и повтор записи

### Цель работы
Создание пакета `course_bringup` с launch-файлом `patrol.launch.py`, обеспечивающим единый запуск системы в изолированном пространстве имён (`namespace:=robot_a`), переназначение топиков команд на глобальный симулятор (`/turtle1/cmd_vel`), параметризацию надёжности подписчика (`subscriber_reliability`) и опциональную запись топиков в формат MCAP (`ros2 bag record`). Воспроизведение дефекта несовместимости политик качества обслуживания (QoS Incompatibility: `best_effort` издатель сенсора vs `reliable` подписчик), устранение несовместимости и проверка воспроизведения записи (replay) с переопределением QoS через `config/qos-overrides.yaml`.

---

### Порядок локального воспроизведения ПР05

#### 1. Сборка пакетов
```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select turtle_bringup patrol course_bringup
source install/setup.bash
```

#### 2. Запуск тестов
```bash
python3 -s -m pytest src/patrol/test
python3 -s -m pytest src/course_bringup/test
python3 -s -m pytest src/turtle_bringup/test
```

#### 3. Запуск глобального симулятора
```bash
export ROS_DOMAIN_ID=16
ros2 launch turtle_bringup sim.launch.py
```

#### 4. Воспроизведение дефекта QoS (до исправления)
```bash
export ROS_DOMAIN_ID=16

# Запуск системы с несовместимым reliable-подписчиком:
ros2 launch course_bringup patrol.launch.py namespace:=robot_a subscriber_reliability:=reliable record:=false

# В отдельном терминале попытка прочитать /robot_a/sensor_pose с reliable QoS:
# Топик виден в ros2 topic list, но сообщения не приходят (таймаут 3с):
timeout 3s ros2 topic echo /robot_a/sensor_pose --qos-reliability reliable --once > evidence/pr05/qos-before.txt
```

#### 5. Устранение дефекта и запись MCAP (после исправления)
```bash
# Перезапуск с согласованным best_effort QoS и включенной записью:
ros2 launch course_bringup patrol.launch.py namespace:=robot_a subscriber_reliability:=best_effort record:=true bag_dir:=evidence/pr05/bag

# Проверка успешного получения сообщения:
timeout 3s ros2 topic echo /robot_a/sensor_pose --qos-reliability best_effort --once > evidence/pr05/qos-after.txt
```

#### 6. Повтор записи (Replay) и инспекция bag
```bash
# Проигрывание записанного потока с переопределением профиля QoS:
ros2 bag play evidence/pr05/bag --qos-profile-overrides-path config/qos-overrides.yaml

# Просмотр метаданных записи:
ros2 bag info evidence/pr05/bag >> evidence/pr05/qos-after.txt
cp evidence/pr05/bag/metadata.yaml evidence/pr05/bag-metadata.yaml
```

---

### Автоматическая проверка
```bash
python3 .course-kit/v1/tools/check_practice.py PR05 --submission .
```
