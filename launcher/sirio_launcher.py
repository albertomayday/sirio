"""
SIRIO TPV x64 - Application Launcher
Punto de entrada para ejecutar toda la aplicación en Windows x64
"""

import os
import sys
import json
import time
import socket
import subprocess
import threading
import webbrowser
from pathlib import Path
from datetime import datetime


class Config:
    """Configuración de la aplicación"""
    APP_NAME = "Sirio TPV"
    VERSION = "1.0.0"
    PLATFORM = "x64"
    BACKEND_PORT = 8000
    FRONTEND_PORT = 9000
    
    @classmethod
    def get_app_root(cls):
        """Obtiene la raíz de la aplicación"""
        if getattr(sys, 'frozen', False):
            # Ejecutable compilado con PyInstaller
            return Path(sys.executable).parent
        else:
            # Ejecución desde Python
            return Path(__file__).parent.parent


class Logger:
    """Sistema de logging simple"""
    
    def __init__(self):
        self.log_dir = config.app_root / "data" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"sirio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    def info(self, message):
        """Log de información"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] INFO: {message}"
        print(log_msg)
        with open(self.log_file, 'a') as f:
            f.write(log_msg + "\n")
    
    def error(self, message):
        """Log de error"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] ERROR: {message}"
        print(f"\033[91m{log_msg}\033[0m")
        with open(self.log_file, 'a') as f:
            f.write(log_msg + "\n")
    
    def success(self, message):
        """Log de éxito"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] SUCCESS: {message}"
        print(f"\033[92m{log_msg}\033[0m")
        with open(self.log_file, 'a') as f:
            f.write(log_msg + "\n")


class SystemCheck:
    """Verificaciones del sistema"""
    
    @staticmethod
    def check_python():
        """Verifica versión de Python"""
        version = sys.version_info
        required = (3, 11)
        if (version.major, version.minor) >= required:
            logger.success(f"Python {version.major}.{version.minor}.{version.micro} OK")
            return True
        else:
            logger.error(f"Python 3.11+ requerido (tienes {version.major}.{version.minor})")
            return False
    
    @staticmethod
    def check_port(port):
        """Verifica si el puerto está disponible"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result != 0
    
    @staticmethod
    def check_ports():
        """Verifica que los puertos estén disponibles"""
        if not SystemCheck.check_port(Config.BACKEND_PORT):
            logger.error(f"Puerto {Config.BACKEND_PORT} en uso")
            return False
        if not SystemCheck.check_port(Config.FRONTEND_PORT):
            logger.error(f"Puerto {Config.FRONTEND_PORT} en uso")
            return False
        logger.success(f"Puertos {Config.BACKEND_PORT}, {Config.FRONTEND_PORT} disponibles")
        return True
    
    @staticmethod
    def check_directories():
        """Verifica y crea directorios necesarios"""
        dirs_needed = [
            "data",
            "data/licenses",
            "data/records",
            "data/logs",
            "data/backups",
        ]
        
        for dir_name in dirs_needed:
            dir_path = config.app_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
        
        logger.success("Directorios verificados")
        return True
    
    @staticmethod
    def run_all():
        """Ejecuta todas las verificaciones"""
        logger.info("Iniciando verificaciones del sistema...")
        
        checks = [
            ("Python versión", SystemCheck.check_python),
            ("Directorios", SystemCheck.check_directories),
            ("Puertos disponibles", SystemCheck.check_ports),
        ]
        
        all_ok = True
        for check_name, check_func in checks:
            try:
                if not check_func():
                    all_ok = False
            except Exception as e:
                logger.error(f"{check_name}: {e}")
                all_ok = False
        
        return all_ok


class BackendManager:
    """Gestión del backend FastAPI"""
    
    def __init__(self):
        self.backend_dir = config.app_root / "backend"
        self.process = None
    
    def setup_environment(self):
        """Configura el entorno del backend"""
        logger.info("Configurando backend...")
        
        # Copiar .env si no existe
        env_file = self.backend_dir / ".env"
        env_example = self.backend_dir / ".env.example"
        
        if not env_file.exists() and env_example.exists():
            import shutil
            shutil.copy2(env_example, env_file)
            logger.info("Archivo .env creado")
        
        # Establecer variables de entorno
        os.environ["DATABASE_URL"] = "sqlite:///./data/sirio.db"
        os.environ["DONGLE_REQUIRED"] = "false"
        os.environ["DEBUG"] = "true"
        
        if not env_file.exists():
            env_file.write_text(
                "DATABASE_URL=sqlite:///./sirio.db\n"
                "DONGLE_REQUIRED=false\n"
                "DEBUG=true\n"
                "LOG_LEVEL=INFO\n"
            )
    
    def install_dependencies(self):
        """Instala las dependencias de Python"""
        logger.info("Instalando dependencias (esto puede tardar...)...")
        
        req_file = self.backend_dir / "requirements.txt"
        if not req_file.exists():
            logger.error("requirements.txt no encontrado")
            return False
        
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "-r", str(req_file)],
                cwd=str(self.backend_dir),
                timeout=300,
                check=False
            )
            logger.success("Dependencias instaladas")
            return True
        except Exception as e:
            logger.error(f"Error instalando dependencias: {e}")
            return False
    
    def start(self):
        """Inicia el backend"""
        logger.info("Iniciando backend FastAPI en puerto 8000...")
        
        self.setup_environment()
        self.install_dependencies()
        
        try:
            cmd = [
                sys.executable, "-m", "uvicorn",
                "main:app",
                "--host", "0.0.0.0",
                "--port", str(Config.BACKEND_PORT),
                "--log-level", "info"
            ]
            
            self.process = subprocess.Popen(
                cmd,
                cwd=str(self.backend_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Esperar a que el backend esté listo
            time.sleep(3)
            
            if self.process.poll() is None:
                logger.success("Backend iniciado en puerto 8000")
                return True
            else:
                logger.error("Backend falló al iniciar")
                return False
                
        except Exception as e:
            logger.error(f"Error iniciando backend: {e}")
            return False
    
    def stop(self):
        """Detiene el backend"""
        if self.process:
            self.process.terminate()
            logger.info("Backend detenido")


class FrontendManager:
    """Gestión del frontend"""
    
    def __init__(self):
        self.frontend_dir = config.app_root / "frontend"
    
    def open_browser(self):
        """Abre el navegador con la aplicación"""
        logger.info("Abriendo interfaz web...")
        
        url = f"http://localhost:{Config.FRONTEND_PORT}"
        time.sleep(1)
        
        try:
            webbrowser.open(url)
            logger.success(f"Navegador abierto: {url}")
            return True
        except Exception as e:
            logger.error(f"Error abriendo navegador: {e}")
            return False


class SirioLauncher:
    """Lanzador principal de Sirio"""
    
    def __init__(self):
        self.backend = BackendManager()
        self.frontend = FrontendManager()
    
    def display_header(self):
        """Muestra el header de bienvenida"""
        print()
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║              🚀 SIRIO TPV x64 - Iniciando...                   ║")
        print(f"║                    Versión {Config.VERSION}                              ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print()
    
    def display_footer(self):
        """Muestra la información de acceso"""
        print()
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║             ✅ SIRIO TPV iniciado correctamente                ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print()
        print("🌐 ACCESO A LA APLICACIÓN:")
        print(f"   • Frontend:        http://localhost:{Config.FRONTEND_PORT}")
        print(f"   • API Backend:     http://localhost:{Config.BACKEND_PORT}")
        print(f"   • Documentación:   http://localhost:{Config.BACKEND_PORT}/docs")
        print()
        print("📁 DATOS Y LOGS:")
        print(f"   • Almacenamiento:  {config.app_root / 'data'}")
        print(f"   • Logs:            {config.app_root / 'data' / 'logs'}")
        print()
        print("📝 NOTAS:")
        print("   • Presiona Ctrl+C para detener la aplicación")
        print("   • Los datos se guardan automáticamente")
        print()
    
    def run(self):
        """Ejecuta la aplicación completa"""
        try:
            self.display_header()
            
            # Verificaciones
            if not SystemCheck.run_all():
                logger.error("Falló verificación del sistema")
                return False
            
            print()
            
            # Iniciar backend
            if not self.backend.start():
                logger.error("Falló al iniciar backend")
                return False
            
            # Abrir frontend
            self.frontend.open_browser()
            
            self.display_footer()
            
            # Mantener la aplicación activa
            logger.info("Aplicación ejecutando. Presiona Ctrl+C para salir...")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Detectada solicitud de parada...")
                self.shutdown()
                return True
                
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return False
    
    def shutdown(self):
        """Detiene la aplicación"""
        print()
        logger.info("Deteniendo Sirio TPV...")
        self.backend.stop()
        logger.success("Goodbye! 👋")


# Instancias globales
config = Config()
logger = Logger()


def main():
    """Punto de entrada principal"""
    launcher = SirioLauncher()
    success = launcher.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
