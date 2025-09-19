import os
import requests
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuración de la API y AnkiConnect ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Error: La clave de API no está configurada. Asegúrate de crear un archivo .env con GOOGLE_API_KEY.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- Funciones ---
def obtener_info_completa_ia(palabra_en_ingles):
    """
    Obtiene la información completa sobre una palabra usando la IA de Gemini y la formatea como un JSON válido.
    """
    prompt = f""". Estoy aprendiendo ingles. Proporciona información completa y detallada sobre la palabra en inglés "{palabra_en_ingles}". Responde únicamente con el objeto JSON y no incluyas texto adicional.

    JSON {{
        "Palabra": "{palabra_en_ingles}",
        "Significado": "[Lista con los significados en español]. Solo palabra clave o frase corta sin oraciones completas",
        "Pronunciacion": "La pronunciación fonética simplificada en español. No la pronunciación oficial, sino en español, por ejemplo Hello = /jelou/ o Help=/jelp/",
        "Gramatica": "Incluye el infinitivo, los tiempos verbales y las conjugaciones más comunes (si aplica)",
        "Etimologia": "Explica el origen y la historia de la palabra",
        "Oracion_Comun": "Una de las oraciones de ejemplo en contexto general",
        "Oracion_medica": "Una de las oraciones de ejemplo en contexto médico",
    }}"""

    try:
        response = model.generate_content(prompt)
        # Limpia el texto de la respuesta y carga el JSON
        json_limpio = response.text.strip().replace("```json", "").replace("```", "")
        datos_json = json.loads(json_limpio)
        print("\n--- Respuesta detallada de la IA (JSON) ---")
        print(json.dumps(datos_json, indent=2, ensure_ascii=False))
        return datos_json
    except Exception as e:
        print(f"Error al obtener y parsear la información: {e}")
        return None

def editar_datos_json(datos_json):
    """
    Permite al usuario editar los campos del JSON antes de crear la tarjeta.
    """
    print("\n--- Modo de edición ---")
    print("Deja el campo vacío para no modificarlo.")

    # Edición de la palabra en inglés
    print(f"Palabra actual: {datos_json.get('Palabra', 'N/A')}")
    nueva_palabra = input("Nueva palabra: ")
    if nueva_palabra.strip():
        datos_json['Palabra'] = nueva_palabra

    # Edición de Significado
    print(f"Significado actual: {datos_json.get('Significado', 'N/A')}")
    nuevo_significado = input("Nuevo significado (separado por comas): ")
    if nuevo_significado.strip():
        datos_json['Significado'] = [s.strip() for s in nuevo_significado.split(',')]

    # Edición de Pronunciación
    print(f"\nPronunciación actual: {datos_json.get('Pronunciacion', 'N/A')}")
    nueva_pronunciacion = input("Nueva pronunciación: ")
    if nueva_pronunciacion.strip():
        datos_json['Pronunciacion'] = nueva_pronunciacion

    # Edición de Oración Médica
    print(f"\nOración Médica actual: {datos_json.get('Oracion_medica', 'N/A')}")
    nueva_oracion_medica = input("Nueva oración médica: ")
    if nueva_oracion_medica.strip():
        datos_json['Oracion_medica'] = nueva_oracion_medica
    
    print("\n✅ Edición completada. Los datos actualizados son:")
    print(json.dumps(datos_json, indent=2, ensure_ascii=False))
    return datos_json

def crear_tarjeta_anki(datos_json, modelName):
    """
    Crea una tarjeta en Anki con los datos extraídos del JSON.
    """
    # Formatea el contenido de la parte de adelante y atrás de la tarjeta.
    # Usamos <br><br> para el renglón en blanco en el anverso.
    contenido_front = f"{datos_json.get('Palabra')} ({datos_json.get('Pronunciacion')})<br><br>{datos_json.get('Oracion_medica')}"
    
    # Formatea el contenido del reverso para que cada significado esté en una nueva línea.
    significados_html = ""
    if isinstance(datos_json.get('Significado'), list):
        significados_html = "<ul>"
        for significado in datos_json.get('Significado'):
            significados_html += f"<li>{significado}</li>"
        significados_html += "</ul>"
    
    # Se ha eliminado "<b>Significado:</b>" para que no aparezca en el reverso.
    contenido_back = f"{significados_html}<br>"
    
    anki_payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "Prueba",
                "modelName": modelName,
                "fields": {
                    "Front": contenido_front,
                    "Back": contenido_back
                },
                "options": {
                    "allowDuplicate": False
                }
            }
        }
    }
    
    try:
        response = requests.post("http://localhost:8765", json=anki_payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al conectar con AnkiConnect: {e}. Asegúrate de que Anki esté abierto y AnkiConnect instalado."}

# --- Bucle principal del script ---
print("Iniciando el creador de tarjetas Anki con IA.")
print("Escribe 'salir' para terminar el programa.")

while True:
    print("-" * 20)
    palabra_ingles = input("Introduce la palabra en inglés: ")
    if palabra_ingles.lower() == 'salir':
        print("Saliendo del programa. ¡Hasta pronto!")
        break

    # Paso 1: Obtener la información completa (ahora devuelve el JSON directamente)
    print(f"Obteniendo información completa para '{palabra_ingles}'...")
    datos_anki = obtener_info_completa_ia(palabra_ingles)
    if datos_anki is None:
        continue

    # Paso 2: Bucle de confirmación y edición
    while True:
        print("-----------------------------------")
        print("\n--- Resumen para la tarjeta ---")
        # Asegúrate de usar las nuevas claves del JSON
        print(f"Palabra: {datos_anki.get('Palabra')}")
        print(f"Significado: {datos_anki.get('Significado')}")
        print(f"Pronunciación: {datos_anki.get('Pronunciacion')}")
        print(f"Oración Médica: {datos_anki.get('Oracion_medica')}")
        print("-----------------------------------")
        
        print("\n¿Deseas agregar la tarjeta a Anki?")
        print(" (s)í: crear tarjeta")
        print(" (n)o: cancelar creación")
        print(" (e)ditar: modificar datos antes de crear la tarjeta")

        confirmar = input("=========> ").lower()
        
        if confirmar == 's':
            # Proceso de creación
            print("Elegí el tipo de carta que deseas crear:")
            print("1. Basic")
            print("2. Basic (and reversed card)")
            
            modelName = ""
            while True:
                opcion_card = input("1 / 2: ")
                if opcion_card == "1":
                    modelName = "Basic"
                    break
                elif opcion_card == "2":
                    modelName = "Basic (and reversed card)"
                    break
                else:
                    print("Entrada no válida. Por favor, elige 1 o 2.")

            resultado = crear_tarjeta_anki(datos_anki, modelName)
            
            print("\n----------------------")
            print("\n--- Tarjeta creada ---")
            print("\n----------------------")
            break
        
        elif confirmar == 'e':
            datos_anki = editar_datos_json(datos_anki)
        
        elif confirmar == 'n':
            print("Creación de tarjeta cancelada.")
            break
        
        else:
            print("Opción no válida. Por favor, elige 's', 'n' o 'e'.")
