# STOKA

**Sistema de Gestión de Stock** — aplicación de escritorio para administrar inventario, ventas, usuarios y chat interno.

Proyecto desarrollado para la escuela secundaria técnica (CABA). Incluye roles de usuario, reportes en PDF/Excel, notificaciones de stock bajo y servidor de chat por sockets.

## Características principales

- **Roles**: Administrador, Encargado de Stock y Vendedor (cada uno con menús y permisos distintos).
- **Inventario**: productos con SKU, stock mínimo, movimientos (entrada/salida/ajuste/venta).
- **Ventas**: registro de ventas y descuento automático de stock.
- **Reportes**: generación de PDF y Excel mensuales.
- **Chat interno**: servidor de sockets + cliente integrado en la GUI.
- **Seguridad**: contraseñas con PBKDF2 + salt, sesiones por rol.
- **Concurrencia**: hilos + asyncio + proceso hijo para estadísticas (multiprocessing).
- **Base de datos**: SQLite (se crea y se siembra automáticamente al primer arranque).
- **Empaquetado**: compatible con PyInstaller (`.exe` de un solo archivo).

## Requisitos

- Python 3.10 o superior (probado con 3.11 / 3.12)
- Dependencias listadas en `requirements.txt`

```bash
pip install -r requirements.txt
```

## Cómo ejecutar

### Modo desarrollo

```bash
python main.py
```

### Generar el .exe (Windows)

```bash
build_exe.bat
```

O manualmente:

```bash
python -m pip install -r requirements.txt
python tools/generate_logo.py
python -m PyInstaller --noconfirm --onefile --windowed --name STOKA --icon assets/logo.ico --add-data "assets/logo.png;assets" --add-data "assets/logo.ico;assets" --hidden-import PIL._tkinter_finder main.py
```

El ejecutable queda en `dist/STOKA.exe`.

## Usuarios de prueba

| Usuario   | Contraseña | Rol                  |
|-----------|------------|----------------------|
| admin     | admin123   | Administrador        |
| stock     | stock123   | Encargado de Stock   |
| vendedor  | venta123   | Vendedor             |

## Estructura del proyecto

```
STOKA/
├── main.py                 # Punto de entrada
├── auth/                   # Login y sesiones
├── database/               # Capa SQLite
├── gui/                    # Interfaz Tkinter (ventanas, paneles, tema)
├── chat/                   # Servidor y cliente de chat
├── reports/                # Generadores PDF y Excel
├── utils/                  # Concurrencia, seguridad, notificaciones, paths
├── assets/                 # Logo e icono
├── tools/                  # Utilidades (generar logo)
├── requirements.txt
└── build_exe.bat
```

## Tecnologías

- Python + Tkinter (GUI)
- SQLite
- Sockets (chat)
- Threading / asyncio / multiprocessing
- ReportLab + openpyxl (reportes)
- Matplotlib (gráficos)
- Pillow
- PyInstaller

---

Desarrollado como trabajo práctico de la escuela secundaria técnica.
