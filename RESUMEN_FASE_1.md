# Resumen Técnico: Cotizador (Días 1 y 2)

Este documento resume los conceptos críticos, herramientas y decisiones de arquitectura tomadas durante los primeros dos días de desarrollo del proyecto **Cotizador**.

##  Estrategia del Proyecto
* **Filosofía:** "Aprender construyendo". No hacemos tutoriales descartables; construimos un producto real (Sistema de Cotizaciones para PYMES) que eventualmente se venderá a clientes locales.
* **Enfoque:** Código profesional desde el día 1. Sin atajos, sin malos hábitos.

---

##  Día 1: Entorno Profesional y Git

### 1. Control de Versiones (Git y GitHub)
* **Git vs GitHub:** Git es la herramienta local de control de versiones. GitHub es el servidor remoto donde vive el repositorio.
* **SSH:** Configuramos autenticación segura mediante llaves SSH (pública/privada) para no tener que escribir contraseñas en cada `push`.
* **Conventional Commits:** Estandarizamos los mensajes de commit. Usamos prefijos como:
  * `feat:` (nueva funcionalidad)
  * `fix:` (corrección de bugs)
  * `chore:` (tareas de mantenimiento, configuración)
  * `docs:` (documentación)
  * `test:` (pruebas)

### 2. Estructura del Proyecto
* **Layout `src/`:** El código fuente vive dentro de `src/cotizador/`. Esto evita que Python importe archivos por accidente desde la raíz y fuerza a que el paquete esté bien instalado.
* **`pyproject.toml`:** Es el estándar moderno (PEP 621) de Python. Reemplaza al viejo `requirements.txt` y `setup.py`. Aquí declaramos dependencias y herramientas.
* **Entornos Virtuales (`.venv`):** Aislamiento de dependencias. **Regla de oro:** Nunca se sube a Git.

### 3. El archivo `.gitignore` (Crítico)
* Evita subir archivos basura (entornos virtuales, cachés de Python, secretos).
* **Lección crítica:** Si haces `git add .` antes de configurar el `.gitignore`, Git rastreará los archivos. Si esto pasa, debes usar `git rm -r --cached <carpeta>` o `git reset` para limpiar el *staging area*.

---

##  Día 2: Modelos, Validación y Testing

### 1. Modelos de Dominio con Pydantic v2
* Representan entidades del mundo real (`Producto`, `Cliente`, `Cotizacion`).
* **Pydantic v2:** Usa Rust en su núcleo, es ultrarrápido. Valida los datos automáticamente al instanciar la clase. Si los datos son inválidos, lanza un `ValidationError`.

### 2. Validaciones: `Field` vs `@field_validator`
* **`Field(...)` (Declarativo):** Para reglas simples que Pydantic ya entiende. Ej: `min_length=2`, `gt=0` (mayor a cero), `max_length=50`.
* **`@field_validator` (Imperativo):** Para lógica personalizada. Ej: Limpiar strings, convertir a mayúsculas (`valor.strip().upper()`), o comparar campos entre sí.

### 3. Valores por Defecto: `default` vs `default_factory`
* **`default`:** Se evalúa UNA SOLA VEZ cuando se carga el módulo. (Mal uso: fechas dinámicas).
* **`default_factory`:** Se evalúa CADA VEZ que se crea un objeto nuevo. (Correcto uso: `datetime.now()` para la fecha de creación de cada cotización).

### 4. Testing con `pytest`
* Escribimos pruebas unitarias en la carpeta `tests/`.
* **Patrón Given-When-Then:** (Preparar, Actuar, Verificar).
* **`pytest.raises(ValidationError)`:** Se usa para probar que nuestro código falla correctamente cuando recibe datos inválidos. Validar el "camino feliz" no es suficiente.

### 5. Calidad de Código (Ruff)
* **Ruff:** Linter y formateador escrito en Rust (reemplaza a Flake8, Black e Isort).
* `ruff check .` busca errores de estilo y código muerto.
* `ruff format .` aplica el formato estándar.

---

##  Errores Comunes que Evitamos (y Aprendimos)
1. **Subir el `.venv` a GitHub:** Error clásico de principiante. Solucionado agregándolo al `.gitignore` y sacándolo del staging.
2. **Usar `TU-USUARIO` literal en Git:** Los tutoriales usan eso como placeholder; hay que reemplazarlo por el nombre real.
3. **Mezclar Acceso a Datos con Lógica de Negocio:** (Visto en el código original del inventario). Ahora separaremos todo usando patrones de diseño.
4. **No hacer tests:** Escribir código sin tests es como construir un puente sin verificar los cálculos.

---

##  Cheat Sheet (Comandos Clave)

**Git:**
```bash
git status                  # Ver estado actual
git add <archivo>           # Preparar archivo específico
git commit -m "feat: ..."   # Guardar cambios
git push                    # Subir a GitHub
git reset                   # Deshacer el staging (sin borrar archivos)
