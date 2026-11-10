#!/bin/bash
set -e

# Iniciar el servidor OpenSSH (Requerido para la Parte B)
service ssh start

# Mantener el contenedor en ejecución continua
exec tail -f /dev/null