from src.repositories.json_solicitud_repository import JsonSolicitudRepository
from src.services.soporte_service import SoporteService
from src.ui.gui import iniciar_gui

def main():
    # Inicializar el repositorio con persistencia en JSON
    repositorio = JsonSolicitudRepository("datos_solicitudes.json")
    
    # Inicializar el servicio inyectando el repositorio
    servicio = SoporteService(repositorio)
    
    # Iniciar la interfaz gráfica
    iniciar_gui(servicio)

if __name__ == "__main__":
    main()
