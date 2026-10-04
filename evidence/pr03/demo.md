# Демонстрация работы узла patrol (ПР03)

## 1. Сборка и запуск модульных тестов

### Сборка пакетов
```bash
$ source /opt/ros/jazzy/setup.bash
$ colcon build --symlink-install --packages-select turtle_bringup patrol
Starting >>> patrol
Starting >>> turtle_bringup
Finished <<< patrol [2.57s]
Finished <<< turtle_bringup [2.58s]

Summary: 2 packages finished [2.70s]
```

### Запуск модульных тестов логики
```bash
$ source install/setup.bash
$ cd src/patrol
$ python3 -s -m pytest -v test/
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
rootdir: /media/denis/C/NSU_rutina/3_Course/Robotics/src/patrol
plugins: launch-testing-3.4.11, ament-lint-0.17.5, ament-pep257-0.17.5, launch-testing-ros-0.26.12, ament-copyright-0.17.5, ament-flake8-0.17.5, ament-xmllint-0.17.5
collecting ... collected 5 items

test/test_copyright.py::test_copyright SKIPPED (No copyright header ...) [ 20%]
test/test_flake8.py::test_flake8 PASSED                                  [ 40%]
test/test_patrol.py::test_compute_cmd_vel_before_first_pose PASSED       [ 60%]
test/test_patrol.py::test_compute_cmd_vel_after_pose PASSED              [ 80%]
test/test_pep257.py::test_pep257 PASSED                                  [100%]

=================== 4 passed, 1 skipped, 8 warnings in 0.53s ===================
```

---

## 2. Воспроизведение дефекта относительного имени топика

### Порядок действий
1. Запуск симулятора:
   ```bash
   ros2 launch turtle_bringup sim.launch.py
   ```
2. Начальная поза черепахи:
   ```bash
   $ ros2 topic echo /turtle1/pose --once
   x: 5.544444561004639
   y: 5.544444561004639
   theta: 0.0
   linear_velocity: 0.0
   angular_velocity: 0.0
   ---
   ```
3. Запуск ноды `patrol` без аргументов переназначения:
   ```bash
   ros2 run patrol patrol
   ```
4. Инспекция топиков:
   ```bash
   $ ros2 topic info /cmd_vel --verbose
   Type: geometry_msgs/msg/Twist

   Publisher count: 1

   Node name: patrol
   Node namespace: /
   Topic type: geometry_msgs/msg/Twist
   Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
   Endpoint type: PUBLISHER
   GID: 01.0f.e7.4a.af.64.44.c3.00.00.00.00.00.00.14.03
   QoS profile:
     Reliability: RELIABLE
     History (Depth): UNKNOWN
     Durability: VOLATILE
     Lifespan: Infinite
     Deadline: Infinite
     Liveliness: AUTOMATIC
     Liveliness lease duration: Infinite

   Subscription count: 0
   ```
   ```bash
   $ ros2 topic info /turtle1/cmd_vel --verbose
   Type: geometry_msgs/msg/Twist

   Publisher count: 0

   Subscription count: 1

   Node name: turtlesim
   Node namespace: /
   Topic type: geometry_msgs/msg/Twist
   Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
   Endpoint type: SUBSCRIPTION
   GID: 01.0f.e7.4a.3e.64.72.93.00.00.00.00.00.00.1d.04
   QoS profile:
     Reliability: RELIABLE
     History (Depth): UNKNOWN
     Durability: VOLATILE
     Lifespan: Infinite
     Deadline: Infinite
     Liveliness: AUTOMATIC
     Liveliness lease duration: Infinite
   ```
5. Проверка позы:
   ```bash
   $ ros2 topic echo /turtle1/pose --once
   x: 5.544444561004639
   y: 5.544444561004639
   theta: 0.0
   linear_velocity: 0.0
   angular_velocity: 0.0
   ---
   ```
Черепаха остается на месте, команды публикуются в топик `/cmd_vel`, где нет подписчиков.

---

## 3. Устранение дефекта и доказательство работоспособности

### Запуск с переназначением топика
```bash
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
```

### Проверка связности конечных точек
```bash
$ ros2 topic info /turtle1/cmd_vel --verbose
Type: geometry_msgs/msg/Twist

Publisher count: 1

Node name: patrol
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: PUBLISHER
GID: 01.0f.e7.4a.fd.65.d4.3e.00.00.00.00.00.00.14.03
QoS profile:
  Reliability: RELIABLE
  History (Depth): UNKNOWN
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite

Subscription count: 1

Node name: turtlesim
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: SUBSCRIPTION
GID: 01.0f.e7.4a.86.65.9e.88.00.00.00.00.00.00.1d.04
QoS profile:
  Reliability: RELIABLE
  History (Depth): UNKNOWN
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite
```

### Замер частоты публикации топика
```bash
$ ros2 topic hz /turtle1/cmd_vel
average rate: 10.001
	min: 0.099s max: 0.100s std dev: 0.00033s window: 11
average rate: 10.000
	min: 0.099s max: 0.100s std dev: 0.00031s window: 22
average rate: 10.000
	min: 0.099s max: 0.101s std dev: 0.00033s window: 32
average rate: 10.000
	min: 0.099s max: 0.101s std dev: 0.00031s window: 43
average rate: 10.001
	min: 0.099s max: 0.101s std dev: 0.00033s window: 54
average rate: 10.000
	min: 0.099s max: 0.101s std dev: 0.00033s window: 64
average rate: 10.000
	min: 0.099s max: 0.101s std dev: 0.00031s window: 74
average rate: 10.000
	min: 0.099s max: 0.101s std dev: 0.00031s window: 85
```
Частота составляет стабильные 10.0 Гц с интервалом между сообщениями 0.1 с, что в точности соответствует заданному периоду таймера `create_timer(0.1, ...)`.

### Проверка изменения позы
```bash
$ ros2 topic echo /turtle1/pose --once
x: 4.477997303009033
y: 8.495237350463867
theta: -2.4527852535247803
linear_velocity: 0.5
angular_velocity: 0.30000001192092896
---
```
Координаты изменились, черепаха движется по окружности с постоянной линейной скоростью 0.5 м/с и угловой скоростью 0.3 рад/с.

---

## 4. Ответы на контрольные вопросы

1. **Зачем нужны `init` и `spin`?**
   - `rclpy.init(args=args)` выполняет инициализацию контекста middleware ROS 2, разбор стандартных аргументов командной строки (`--ros-args`) и подготовку инфраструктуры DDS.
   - `rclpy.spin(node)` блокирует вызывающий поток и запускает цикл диспетчеризации событий (SingleThreadedExecutor по умолчанию). Он слушает входящие события от middleware (таймеры, поступление сообщений в подписки, сервисы) и вызывает соответствующие зарегистрированные callback-функции. Без вызова `spin` колбэки таймеров и подписок никогда не были бы выполнены.

2. **Как работают callbacks и таймеры?**
   - Подписка `create_subscription` и таймер `create_timer` регистрируют вызываемые объекты (callbacks) в узле.
   - При срабатывании таймера (по истечении заданного интервала времени) или поступлении нового сообщения из DDS-очереди соответствующий callback ставится в очередь исполнителя (executor).
   - В однопоточном исполнителе колбэки выполняются последовательно в потоке `spin()`. Таймер периодически генерирует события с заданным интервалом (0.1 с), вызывая публикацию скорости.

3. **Что происходит при нажатии `Ctrl+C`?**
   - Операционная система посылает процессу сигнал `SIGINT`.
   - Внутри Python этот сигнал перехватывается стандартным обработчиком, прерывающим `rclpy.spin(node)` исключением `KeyboardInterrupt`.
   - Блок `try ... except KeyboardInterrupt` корректно перехватывает исключение и передает управление в блок `finally`, где вызываются `node.destroy_node()` и `rclpy.shutdown()`, освобождающие ресурсы ноды и корректно завершающие контекст ROS 2.

4. **Почему черепаха не останавливается мгновенно при остановке ноды патрулирования?**
   - Нода симулятора `turtlesim` хранит текущую заданную скорость черепахи в своем внутреннем состоянии.
   - Завершение процесса ноды `patrol` по `Ctrl+C` просто прекращает поток отправки новых сообщений `Twist`. При этом сообщение с нулевой скоростью (`Twist(linear=0, angular=0)`) в топик не отправляется.
   - В `turtlesim` отсутствует механизм таймаута команд скорости (watchdog / command timeout). Симулятор продолжает интегрировать физику движения на основе последнего полученного сообщения о скорости до тех пор, пока черепаха не упрется в стену или пока в топик `/turtle1/cmd_vel` явно не поступит нулевая скорость.
