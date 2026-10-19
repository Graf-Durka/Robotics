# Дерево координатных фреймов (tf2) робота course_ackermann

## 1. Иерархия фреймов (Transform Tree)

Дерево координатных фреймов робота имеет единый корневой фрейм `base_link`. Все кинематические звенья и сенсоры соединены с ним напрямую или через поворотные кулаки передней оси.

```text
base_link (корневой фрейм)
├── camera_link                  (joint: camera_joint, fixed, x=0.28, y=0.00, z=0.38)
├── imu_link                     (joint: imu_joint, fixed, x=0.28, y=0.00, z=0.38)
├── lidar_link                   (joint: lidar_joint, fixed, x=0.28, y=0.00, z=0.38)
├── front_left_knuckle           (joint: front_left_steering_joint, revolute, x=0.40, y=0.31, z=0.00)
│   └── front_left_wheel         (joint: front_left_wheel_joint, continuous, x=0.00, y=0.00, z=0.00)
├── front_right_knuckle          (joint: front_right_steering_joint, revolute, x=0.40, y=-0.31, z=0.00)
│   └── front_right_wheel        (joint: front_right_wheel_joint, continuous, x=0.00, y=0.00, z=0.00)
├── rear_left_wheel              (joint: rear_left_wheel_joint, continuous, x=-0.40, y=0.31, z=0.00)
└── rear_right_wheel             (joint: rear_right_wheel_joint, continuous, x=-0.40, y=-0.31, z=0.00)
```

## 2. Параметры соединений и смещения

| Соединение (Joint) | Тип | Родитель (Parent) | Потомок (Child) | Смещение (XYZ, м) | Ориентация (RPY, рад) | Ось вращения (Axis) |
|---|---|---|---|---|---|---|
| `front_left_steering_joint` | `revolute` | `base_link` | `front_left_knuckle` | `0.40, 0.31, 0.00` | `0.0, 0.0, 0.0` | `[0, 0, 1]` |
| `front_right_steering_joint` | `revolute` | `base_link` | `front_right_knuckle` | `0.40, -0.31, 0.00` | `0.0, 0.0, 0.0` | `[0, 0, 1]` |
| `front_left_wheel_joint` | `continuous` | `front_left_knuckle` | `front_left_wheel` | `0.00, 0.00, 0.00` | `0.0, 0.0, 0.0` | `[0, 1, 0]` |
| `front_right_wheel_joint` | `continuous` | `front_right_knuckle` | `front_right_wheel` | `0.00, 0.00, 0.00` | `0.0, 0.0, 0.0` | `[0, 1, 0]` |
| `rear_left_wheel_joint` | `continuous` | `base_link` | `rear_left_wheel` | `-0.40, 0.31, 0.00` | `0.0, 0.0, 0.0` | `[0, 1, 0]` |
| `rear_right_wheel_joint` | `continuous` | `base_link` | `rear_right_wheel` | `-0.40, -0.31, 0.00` | `0.0, 0.0, 0.0` | `[0, 1, 0]` |
| `camera_joint` | `fixed` | `base_link` | `camera_link` | `0.28, 0.00, 0.38` | `0.0, 0.0, 0.0` | — |
| `lidar_joint` | `fixed` | `base_link` | `lidar_link` | `0.28, 0.00, 0.38` | `0.0, 0.0, 0.0` | — |
| `imu_joint` | `fixed` | `base_link` | `imu_link` | `0.28, 0.00, 0.38` | `0.0, 0.0, 0.0` | — |

## 3. Кинематические константы
- **База колёс (Wheelbase)**: $L = 0.80$ м (расстояние между передней осью $x = +0.40$ и задней осью $x = -0.40$).
- **Колея (Track / Wheel separation)**: $W = 0.62$ м (расстояние между левыми колёсами $y = +0.31$ и правыми $y = -0.31$).
- **Радиус колеса (Wheel radius)**: $R = 0.12$ м.
- **Ширина колеса**: $H = 0.07$ м.
- **Масса шасси**: $12.0$ кг; масса колеса: $0.8$ кг; масса поворотного кулака: $0.2$ кг.

## 4. Маршрутизация и публикация трансформаций

1. **Статические трансформации (`/tf_static`)**:
   - Публикуются узлом `robot_state_publisher` однократно при инициализации.
   - Охватывают фиксированные соединения сенсорного оборудования: `camera_joint`, `lidar_joint`, `imu_joint`.
   - Профиль QoS: `Durability: TRANSIENT_LOCAL`, `Reliability: RELIABLE`. Это гарантирует доставку сохранённых трансформаций любым узлам, запустившимся позже.

2. **Динамические трансформации (`/tf`)**:
   - Публикуются узлом `robot_state_publisher` на основе актуальных состояний углов сочленений из топика `/joint_states`.
   - Охватывают поворот рулевых кулаков (`front_left_steering_joint`, `front_right_steering_joint`) и вращение колёс (`front_left_wheel_joint`, `front_right_wheel_joint`, `rear_left_wheel_joint`, `rear_right_wheel_joint`).
   - Профиль QoS: `Durability: VOLATILE`, `Reliability: RELIABLE`.
