# Configuración de Gunicorn para Render con memoria limitada
import os
import multiprocessing

# Bind
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Workers
# En plan Free: 1 worker para ahorrar memoria
# En planes pagados: 2-4 workers
workers = 1

# Worker class
worker_class = "sync"

# Timeout extendido para entrenamiento de modelos
timeout = 300  # 5 minutos (antes era 30 segundos)

# Graceful timeout
graceful_timeout = 120

# Keep alive
keepalive = 5

# Max requests (reciclar workers después de N requests)
max_requests = 100
max_requests_jitter = 10

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"

# Preload app (reduce memoria pero aumenta tiempo de inicio)
preload_app = False

