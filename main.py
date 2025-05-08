# -*- coding: utf-8 -*-
import os
import json
import random
import shutil
import base64
import sys
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.app import App
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout  # Para superponer widgets
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from kivy.uix.image import Image
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.scrollview import ScrollView
from plyer import filechooser
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from android.storage import primary_external_storage_path


# Obtener el tamaño de la pantalla actual
screen_width, screen_height = Window.size

# Función para mostrar el error en pantalla
def mostrar_error_en_pantalla(mensaje):
    """
    Muestra un mensaje de error en una ventana emergente.
    La aplicación no se cerrará hasta que el usuario cierre la ventana.
    """
    # Crear un layout vertical para el contenido del popup
    content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10))
    
    # Etiqueta con el mensaje de error
    label = Label(
        text=f"Error: {mensaje}",
        size_hint_y=None,
        height=dp(100),
        halign="center",
        valign="middle"
    )
    content.add_widget(label)
    
    # Botón para cerrar el popup
    btn_cerrar = Button(
        text="Cerrar",
        size_hint_y=None,
        height=dp(50)
    )
    
    # Crear el popup
    popup = Popup(
        title="Error Crítico",
        content=content,
        size_hint=(0.8, 0.4)  # Tamaño relativo de la ventana emergente
    )
    
    # Asociar el botón de cierre al popup
    btn_cerrar.bind(on_release=lambda *args: popup.dismiss())
    content.add_widget(btn_cerrar)
    
    # Mostrar el popup
    popup.open()

# Manejador global de excepciones
def manejar_excepcion(exc_type, exc_value, exc_traceback):
    """
    Captura excepciones no controladas y muestra un mensaje de error en pantalla.
    """
    # Evitar que la aplicación se cierre inmediatamente
    if issubclass(exc_type, KeyboardInterrupt):
        # Si es una interrupción manual (Ctrl+C), dejar que Kivy maneje la salida
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # Formatear el mensaje de error
    import traceback
    mensaje_error = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Error capturado: {mensaje_error}")  # Imprimir el error en la consola
    
    # Mostrar el error en pantalla
    try:
        mostrar_error_en_pantalla(mensaje_error)
    except Exception as e:
        print(f"No se pudo mostrar el error en pantalla: {e}")

# Configurar el manejador global de excepciones
sys.excepthook = manejar_excepcion





# Función para calcular tamaños relativos
def relative_size(base_size, reference=360):
    """Calcula un tamaño relativo basado en el ancho o alto de la pantalla."""
    screen_width, screen_height = Window.size
    return dp(base_size * (min(screen_width, screen_height) / reference))
    
 
    
def generar_codigo_maestro():
    """Genera un código maestro de 8 caracteres alfanuméricos."""
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))

def transformar_codigo(codigo):
    """
    Transforma el código usando una lógica específica.
    - Invertir el código.
    - Intercambiar cada par de caracteres adyacentes.
    - Añadir un carácter fijo al final (por ejemplo, 'X').
    """
    invertido = codigo[::-1]
    intercambiado = ''.join([invertido[i+1] + invertido[i] if i+1 < len(invertido) else invertido[i] for i in range(0, len(invertido), 2)])
    return intercambiado + "X"  # Añadir un carácter fijo al final
    

def obtener_ruta_app_data():
    """Devuelve la ruta correcta de la carpeta app_data en diferentes sistemas."""
    if platform == "android":
        return os.path.join(primary_external_storage_path(), "app_data")
    else:
        # Detecta la carpeta app_data basada en la ubicación del script
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_app_data = os.path.join(ruta_script, "app_data")
        if not os.path.exists(ruta_app_data):
            os.makedirs(ruta_app_data)  # Crear la carpeta si no existe
        return ruta_app_data


def get_config_file():
    return os.path.join(obtener_ruta_app_data(), "config.json")


def get_progress_file():
    return os.path.join(obtener_ruta_app_data(), "progreso.json")


def obtener_ruta_temario():
    """Devuelve la ruta correcta de la carpeta temario dentro de app_data."""
    ruta_temario = os.path.join(obtener_ruta_app_data(), "temario")
    if not os.path.exists(ruta_temario):
        os.makedirs(ruta_temario)  # Crear la carpeta si no existe
    return ruta_temario


# Guardar configuración del usuario
def guardar_configuracion(config):
    ruta = get_config_file()
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


# Cargar configuración
def cargar_configuracion():
    ruta = get_config_file()
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Asegurarse de que todos los campos necesarios existan
                config.setdefault("aleatorio", False)  # Respuestas aleatorias
                config.setdefault("json_seleccionado", "")  # Archivo JSON seleccionado
                config.setdefault("num_preguntas", 10)  # Número de preguntas
                config.setdefault("modo_oscuro", False)  # Modo oscuro (predeterminado: desactivado)
                config.setdefault("preguntas_aleatorias", False)
                return config
        else:
            # Crear un archivo de configuración predeterminado si no existe
            config_predeterminado = {
                "aleatorio": False,
                "json_seleccionado": "",
                "num_preguntas": 10,
                "modo_oscuro": False,  # Valor predeterminado para el modo oscuro
                "preguntas_aleatorias": False
            }
            guardar_configuracion(config_predeterminado)
            return config_predeterminado
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return {
            "aleatorio": False,
            "json_seleccionado": "",
            "num_preguntas": 10,
            "modo_oscuro": False,  # Valor predeterminado para el modo oscuro
            "preguntas_aleatorias": False
        }


# Guardar y cargar progreso
def guardar_progreso(progreso):
    with open(get_progress_file(), "w", encoding="utf-8") as f:
        json.dump(progreso, f, ensure_ascii=False, indent=4)


def cargar_progreso():
    ruta = get_progress_file()
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"correctas": 0, "contestadas": 0}


class RegisterScreen(MDScreen):
    def on_enter(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation="vertical", spacing=relative_size(20), padding=relative_size(20))
        # Título de la pantalla
        layout.add_widget(
            MDLabel(
                text="Registro de la Aplicación",
                font_style="H5",
                halign="center",
                theme_text_color="Custom",
                text_color="#9C1AB6",
                font_size=relative_size(20)
            )
        )
        # Generar un código alfanumérico de 8 caracteres
        self.generated_code = generar_codigo_maestro()
        self.validated_code = transformar_codigo(self.generated_code)  # Código validado es el transformado
        layout.add_widget(
            MDLabel(
                text=f"Código de Registro: {self.generated_code}",
                font_style="Body1",
                halign="center",
                theme_text_color="Custom",
                text_color="#9C1AB6",
                font_size=relative_size(16)
            )
        )
        # Campo de entrada para el código validado
        self.code_input = MDTextField(
            hint_text="Introduce el código validado",
            size_hint=(1, None),
            height=relative_size(50),
            pos_hint={"center_x": 0.5},
            mode="rectangle"
        )
        layout.add_widget(self.code_input)
        # Botón para validar el código
        btn_validar = MDRaisedButton(
            text="Validar Código",
            size_hint=(None, None),
            size=(relative_size(200), relative_size(50)),
            md_bg_color="#F78F1E",
            text_color="#FFFFFF"
        )
        btn_validar.bind(on_release=self.validar_codigo)
        layout.add_widget(btn_validar)
        self.add_widget(layout)

    def validar_codigo(self, instance):
        user_code = self.code_input.text.strip()
        if not user_code:
            return
        # Validar el código introducido
        if user_code == self.validated_code:
            config = cargar_configuracion()
            config["progreso"] = "true"  # Marcar como registrado
            guardar_configuracion(config)
            self.manager.current = "menu"  # Ir al menú principal
        else:
            self.code_input.error = True


class ConfigScreen(MDScreen):
    def on_enter(self):
        self.clear_widgets()
        
        # Crear un FloatLayout como contenedor principal con la imagen de fondo
        main_layout = FloatLayout()

        # Agregar la imagen de fondo
        background_image = Image(
            source="assets/background.png",  # Asegúrate de que la ruta sea correcta
            allow_stretch=True,
            keep_ratio=False
        )
        main_layout.add_widget(background_image)

        # Contenedor vertical para los widgets
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=relative_size(10),
            padding=relative_size(10),
            size_hint=(1, 1)  # Ocupar toda la pantalla
        )

        # Título de la pantalla
        content_layout.add_widget(
            MDLabel(
                text="Configuración",
                font_style="H5",
                halign="center",
                font_size=relative_size(20),
                theme_text_color="Custom",
                text_color="#FFFFFF"  # Texto blanco para contraste
            )
        )

        # Cargar la configuración
        self.config = cargar_configuracion()

        # Switch para Modo Oscuro
        fila_switch_modo_oscuro = MDBoxLayout(
            orientation="horizontal",
            spacing=relative_size(5),  # Reducir el espaciado interno
            size_hint_y=None,
            height=relative_size(40)  # Reducir la altura del contenedor
        )
        switch_label_modo_oscuro = MDLabel(
            text="Modo Oscuro",
            font_style="Body1",
            size_hint_x=0.8,
            valign="middle",
            theme_text_color="Custom",
            text_color="#FFFFFF",  # Texto blanco para contraste
            font_size=relative_size(16)
        )
        modo_oscuro = self.config.get("modo_oscuro", False)
        self.switch_modo_oscuro = MDSwitch(
            active=modo_oscuro,
            size_hint=(None, None),
            size=(relative_size(60), relative_size(30)),
            pos_hint={"center_y": 0.5}
        )
        self.switch_modo_oscuro.bind(active=self.cambiar_modo_oscuro)
        fila_switch_modo_oscuro.add_widget(switch_label_modo_oscuro)
        fila_switch_modo_oscuro.add_widget(self.switch_modo_oscuro)
        content_layout.add_widget(fila_switch_modo_oscuro)

        # Switch para Preguntas Aleatorias
        fila_switch_preguntas_aleatorias = MDBoxLayout(
            orientation="horizontal",
            spacing=relative_size(5),  # Reducir el espaciado interno
            size_hint_y=None,
            height=relative_size(40)  # Reducir la altura del contenedor
        )
        switch_label_preguntas_aleatorias = MDLabel(
            text="Preguntas Aleatorias",
            font_style="Body1",
            size_hint_x=0.8,
            valign="middle",
            theme_text_color="Custom",
            text_color="#FFFFFF",  # Texto blanco para contraste
            font_size=relative_size(16)
        )
        preguntas_aleatorias = self.config.get("preguntas_aleatorias", True)
        self.switch_preguntas_aleatorias = MDSwitch(
            active=preguntas_aleatorias,
            size_hint=(None, None),
            size=(relative_size(60), relative_size(30)),
            pos_hint={"center_y": 0.5}
        )
        self.switch_preguntas_aleatorias.bind(active=self.cambiar_preguntas_aleatorias)
        fila_switch_preguntas_aleatorias.add_widget(switch_label_preguntas_aleatorias)
        fila_switch_preguntas_aleatorias.add_widget(self.switch_preguntas_aleatorias)
        content_layout.add_widget(fila_switch_preguntas_aleatorias)

        # Switch para Respuestas Aleatorias
        fila_switch_respuestas_aleatorias = MDBoxLayout(
            orientation="horizontal",
            spacing=relative_size(5),  # Reducir el espaciado interno
            size_hint_y=None,
            height=relative_size(40)  # Reducir la altura del contenedor
        )
        switch_label_respuestas_aleatorias = MDLabel(
            text="Respuestas Aleatorias",
            font_style="Body1",
            size_hint_x=0.8,
            valign="middle",
            theme_text_color="Custom",
            text_color="#FFFFFF",  # Texto blanco para contraste
            font_size=relative_size(16)
        )
        respuestas_aleatorias = self.config.get("aleatorio", True)
        self.switch_respuestas_aleatorias = MDSwitch(
            active=respuestas_aleatorias,
            size_hint=(None, None),
            size=(relative_size(60), relative_size(30)),
            pos_hint={"center_y": 0.5}
        )
        self.switch_respuestas_aleatorias.bind(active=self.cambiar_orden)
        fila_switch_respuestas_aleatorias.add_widget(switch_label_respuestas_aleatorias)
        fila_switch_respuestas_aleatorias.add_widget(self.switch_respuestas_aleatorias)
        content_layout.add_widget(fila_switch_respuestas_aleatorias)

        # Etiqueta para mostrar el nombre del archivo JSON seleccionado
        nombre_archivo = self.config.get("json_seleccionado", "Ninguno")
        nombre_archivo_sin_extension = (
            os.path.splitext(nombre_archivo)[0] if nombre_archivo != "Ninguno" else "Ninguno"
        )
        self.json_label = MDLabel(
            text=f"Temario seleccionado: {nombre_archivo_sin_extension}",
            font_style="Body1",
            halign="left",
            theme_text_color="Custom",
            text_color="#FFFFFF",  # Texto blanco para contraste
            font_size=relative_size(14)
        )
        content_layout.add_widget(self.json_label)

        # Selección de JSON en "app_data/temario/"
        content_layout.add_widget(
            MDLabel(
                text="Seleccionar Base de Preguntas",
                font_style="Subtitle1",
                halign="left",
                theme_text_color="Custom",
                text_color="#FFFFFF",  # Texto blanco para contraste
                font_size=relative_size(16)
            )
        )
        temario_path = obtener_ruta_temario()
        json_files = [f for f in os.listdir(temario_path) if f.endswith(".json")]
        json_files_sin_extension = [os.path.splitext(f)[0] for f in json_files]
        self.json_selector = MDDropdownMenu(
            caller=content_layout,
            items=[
                {"text": nombre, "viewclass": "OneLineListItem", "on_release": lambda x=nombre: self.cambiar_json(x)}
                for nombre in json_files_sin_extension
            ],
            width_mult=4
        )
        btn_seleccionar_json = MDRaisedButton(
            text="Seleccionar Temario",
            size_hint=(None, None),
            size=(relative_size(200), relative_size(50)),
            md_bg_color="#F78F1E",
            text_color="#FFFFFF"
        )
        btn_seleccionar_json.bind(on_release=self.abrir_menu_json)
        content_layout.add_widget(btn_seleccionar_json)

        # Nuevo Botón para Agregar Temarios
        btn_agregar_temario = MDRaisedButton(
            text="Agregar Temario",
            size_hint=(None, None),
            size=(relative_size(200), relative_size(50)),
            md_bg_color="#F78F1E",
            text_color="#FFFFFF"
        )
        btn_agregar_temario.bind(on_release=self.abrir_navegador_archivos)
        content_layout.add_widget(btn_agregar_temario)

        # Menú desplegable para seleccionar el número de preguntas
        content_layout.add_widget(
            MDLabel(
                text="Número de Preguntas",
                font_style="Subtitle1",
                halign="left",
                theme_text_color="Custom",
                text_color="#FFFFFF",  # Texto blanco para contraste
                font_size=relative_size(16)
            )
        )
        num_preguntas_items = [
            {
                "text": str(num),
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x=num: self.cambiar_num_preguntas(x)
            }
            for num in [10, 25, 50, 75, 100, 200]
        ]
        self.num_preguntas_selector = MDDropdownMenu(
            caller=content_layout,
            items=num_preguntas_items,
            width_mult=4
        )
        self.btn_seleccionar_num_preguntas = MDRaisedButton(
            text=f"{self.config.get('num_preguntas', 10)} preguntas",
            size_hint=(None, None),
            size=(relative_size(200), relative_size(50)),
            md_bg_color="#F78F1E",
            text_color="#FFFFFF"
        )
        self.btn_seleccionar_num_preguntas.bind(on_release=self.abrir_menu_num_preguntas)
        content_layout.add_widget(self.btn_seleccionar_num_preguntas)

        # Botón para Volver
        btn_volver = MDRaisedButton(
            text="Volver",
            size_hint=(None, None),
            size=(relative_size(200), relative_size(50)),
            md_bg_color="#F78F1E",
            text_color="#FFFFFF"
        )
        btn_volver.bind(on_release=self.volver_menu)
        content_layout.add_widget(btn_volver)

        # Añadir el layout de contenido al FloatLayout principal
        main_layout.add_widget(content_layout)

        # Añadir el layout principal a la pantalla
        self.add_widget(main_layout)


    def abrir_navegador_archivos(self, instance):
        """
        Abre un navegador de archivos para seleccionar un archivo JSON.
        Si se selecciona un archivo, lo copia a la carpeta app_data/temario.
        Además, actualiza dinámicamente el menú desplegable de temarios.
        """
        try:
            # Abrir el navegador de archivos y filtrar solo archivos JSON
            file_path = filechooser.open_file(filters=["*.json"], multiple=False)
            if file_path:  # Si se seleccionó un archivo
                origen = file_path[0]  # Ruta del archivo seleccionado
                nombre_archivo = os.path.basename(origen)  # Nombre del archivo
                destino = os.path.join(obtener_ruta_temario(), nombre_archivo)  # Carpeta destino
                shutil.copy(origen, destino)  # Copiar el archivo
                print(f"Archivo '{nombre_archivo}' agregado correctamente.")
                
                # Actualizar dinámicamente el menú desplegable de temarios
                temario_path = obtener_ruta_temario()
                json_files = [f for f in os.listdir(temario_path) if f.endswith(".json")]
                json_files_sin_extension = [os.path.splitext(f)[0] for f in json_files]
                self.json_selector.items = [
                    {"text": nombre, "viewclass": "OneLineListItem", "on_release": lambda x=nombre: self.cambiar_json(x)}
                    for nombre in json_files_sin_extension
                ]
                print("Menú de temarios actualizado.")
            else:
                print("No se seleccionó ningún archivo.")
        except Exception as e:
            print(f"Error al agregar el temario: {e}")

    def cambiar_modo_oscuro(self, switch, value):
        """
        Guarda el estado del modo oscuro en el archivo de configuración
        y cambia el tema de la aplicación en tiempo real.
        """
        # Guardar el valor en el archivo de configuración
        self.config["modo_oscuro"] = value
        guardar_configuracion(self.config)
        # Cambiar el tema de la aplicación en tiempo real
        app = App.get_running_app()
        if value:
            app.theme_cls.theme_style = "Dark"  # Activar modo oscuro
        else:
            app.theme_cls.theme_style = "Light"  # Activar modo claro

    def cambiar_json(self, nombre):
        # Recuperar el nombre completo del archivo (con extensión)
        nombre_completo = f"{nombre}.json"
        self.config["json_seleccionado"] = nombre_completo
        guardar_configuracion(self.config)
        # Actualizar la etiqueta sin mostrar la extensión
        self.json_label.text = f"Temario seleccionado: {nombre}"
        self.json_selector.dismiss()

    def abrir_menu_json(self, instance):
        self.json_selector.open()

    def cambiar_num_preguntas(self, num_preguntas):
        self.config["num_preguntas"] = num_preguntas
        guardar_configuracion(self.config)
        self.btn_seleccionar_num_preguntas.text = f"{num_preguntas} preguntas"  # Actualizar el texto del botón
        self.num_preguntas_selector.dismiss()

    def abrir_menu_num_preguntas(self, instance):
        self.num_preguntas_selector.open()

    def cambiar_orden(self, switch, value):
        self.config["aleatorio"] = value
        guardar_configuracion(self.config)

    def cambiar_preguntas_aleatorias(self, switch, value):
        """
        Guarda el estado del switch para "Preguntas Aleatorias" en el archivo de configuración.
        """
        self.config["preguntas_aleatorias"] = value
        guardar_configuracion(self.config)

    def volver_menu(self, instance):
        self.manager.current = "menu"


class TemaScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        # Crear un ScrollView para manejar temas largos
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        layout = BoxLayout(orientation="vertical", spacing=dp(20), padding=dp(20), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        app = App.get_running_app()
        config = cargar_configuracion()
        ruta_temario = os.path.join(obtener_ruta_temario(), config.get("json_seleccionado", "preguntas.json"))
        if not os.path.exists(ruta_temario):
            shutil.copy(
                os.path.join(os.path.dirname(__file__), "assets", config.get("json_seleccionado", "preguntas.json")),
                ruta_temario
            )
        with open(ruta_temario, "r", encoding="utf-8") as f:
            self.temario = json.load(f)["temario_general"]["temas"]
        # Título
        layout.add_widget(MDLabel(
            text="Selecciona uno o varios temas",
            font_style="H5",
            halign="center",
            theme_text_color="Custom",
            text_color="#9C1AB6"
        ))
        # Lista para almacenar las selecciones
        self.temas_seleccionados = []
        self.botones = []
        # Almacenar referencias a los botones
        # Crear botones para cada tema
        for i, tema in enumerate(self.temario):
            btn_label = MDLabel(
                text=tema["nombre"],
                halign="center",
                valign="middle",
                size_hint_y=None,
                text_size=(Window.width * 0.8, None),  # Ancho máximo del texto
                theme_text_color="Custom",
                text_color="white"
            )
            btn_label.bind(texture_size=self.ajustar_altura_boton)  # Ajustar altura dinámicamente
            btn = MDRaisedButton(
                size_hint=(1, None),
                height=dp(70),  # Altura inicial (se ajustará dinámicamente)
                md_bg_color="#F8B400",  # Color inicial (amarillo)
                text_color="#FFFFFF"
            )
            btn.add_widget(btn_label)  # Vincular el botón a su índice y agregarlo a la lista de botones
            btn.bind(on_release=lambda btn, idx=i: self.toggle_seleccion(btn, idx))
            self.botones.append(btn)
            layout.add_widget(btn)
        
        # Botón para seleccionar todos los temas
        btn_seleccionar_todos = MDRaisedButton(
            text="Seleccionar Todos los Temas",
            size_hint=(1, None),
            height=dp(50),
            md_bg_color="#F8B400",
            text_color="#FFFFFF"
        )
        btn_seleccionar_todos.bind(on_release=self.seleccionar_todos)
        layout.add_widget(btn_seleccionar_todos)

        # Botón de confirmación
        btn_confirmar = MDRaisedButton(
            text="Confirmar Selección",
            size_hint=(1, None),
            height=dp(50),
            md_bg_color="#F8B400",
            text_color="#FFFFFF"
        )
        btn_confirmar.bind(on_release=self.confirmar_seleccion)
        layout.add_widget(btn_confirmar)
        scroll.add_widget(layout)
        self.add_widget(scroll)
        
        
    def seleccionar_todos(self, instance):
            # Seleccionar todos los temas
            self.temas_seleccionados = [i for i in range(len(self.temario))]
            for btn in self.botones:
                btn.md_bg_color = "#2196F3"  # Color seleccionado (azul)

    def ajustar_altura_boton(self, label, texture_size):
        """Ajusta dinámicamente la altura del botón según el tamaño del texto."""
        label.parent.height = max(dp(70), texture_size[1] + dp(20))

    def toggle_seleccion(self, btn, idx):
        """
        Alterna la selección de un tema al hacer clic en el botón.
        Cambia el color del botón y actualiza la lista de temas seleccionados.
        """
        if idx in self.temas_seleccionados:
            # Desmarcar el tema
            self.temas_seleccionados.remove(idx)
            btn.md_bg_color = "#F8B400"  # Color inicial (amarillo)
        else:
            # Marcar el tema
            self.temas_seleccionados.append(idx)
            btn.md_bg_color = "#2196F3"  # Color seleccionado (azul)

    def confirmar_seleccion(self, *args):
        """Confirma la selección de temas y pasa a la pantalla de cuestionario."""
        if not self.temas_seleccionados:
            # Mostrar mensaje de error si no se seleccionó ningún tema
            print("Debes seleccionar al menos un tema.")
            return
        app = App.get_running_app()
        # Filtrar preguntas de los temas seleccionados
        app.preguntas = [
            pregunta
            for idx in self.temas_seleccionados
            for pregunta in self.temario[idx]["preguntas"]
        ]
        # Mezclar preguntas si están habilitadas como aleatorias
        config = cargar_configuracion()
        if config.get("preguntas_aleatorias", True):
            random.shuffle(app.preguntas)
        # Reiniciar el progreso
        progreso = {"correctas": 0, "contestadas": 0}
        guardar_progreso(progreso)
        # Cambiar a la pantalla de cuestionario
        app.root.current = "quiz"


class QuizScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.current_index = 0
        self.correctas = 0
        self.tiempo_transcurrido = 0  # Inicializar el tiempo transcurrido en segundos
        # Usar un BoxLayout vertical para organizar los elementos
        self.layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10))
        # Contenedor superior para el reloj y el botón de salida
        top_bar = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50))
        # Temporizador en la parte superior izquierda
        self.temporizador = MDLabel(
            text="00:00",
            font_style="H5",
            size_hint=(0.5, 1),
            theme_text_color="Custom",
            text_color="black"
        )
        top_bar.add_widget(self.temporizador)
        # Botón de "Abandonar test" en la parte superior derecha
        btn_abandonar = MDIconButton(
            icon="close",
            size_hint=(0.1, 1),
            on_release=self.salir_test,
            theme_text_color="Custom",
            text_color="red"
        )
        top_bar.add_widget(btn_abandonar)
        self.layout.add_widget(top_bar)
        # Contenedor para la pregunta y las opciones
        self.contenedor_preguntas = BoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20),
            size_hint=(1, 1)  # Ocupa el resto del espacio disponible
        )
        self.layout.add_widget(self.contenedor_preguntas)
        # Etiqueta para la pregunta
        self.label = MDLabel(
            text="Cargando pregunta...",
            font_style="H5",
            halign="center",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(50)
        )
        self.contenedor_preguntas.add_widget(self.label)
        # Espaciador para aumentar el espacio entre la pregunta y las opciones
        espaciador = Widget(size_hint_y=None, height=dp(50))  # Ajusta la altura (dp(20)) según el espacio que desees
        self.contenedor_preguntas.add_widget(espaciador)
        # Botones para las opciones
        self.botones = []
        for _ in range(4):
            btn = MDRaisedButton(
                font_size=dp(16),
                size_hint=(1, None),
                height=dp(50),
                md_bg_color="blue",
                text_color="white"
            )
            btn.bind(on_release=self.verificar_respuesta)
            self.botones.append(btn)
            self.contenedor_preguntas.add_widget(btn)
        # Botón "Siguiente"
        self.btn_siguiente = MDRaisedButton(
            text="Siguiente",
            size_hint=(1, None),
            height=dp(50),
            md_bg_color="#F78F1E",
            text_color="#FFFFFF",
            disabled=True  # Inicialmente deshabilitado
        )
        self.btn_siguiente.bind(on_release=self.siguiente_pregunta)
        self.contenedor_preguntas.add_widget(self.btn_siguiente)
        self.add_widget(self.layout)
        # Iniciar el temporizador
        self.temporizador_evento = Clock.schedule_interval(self.actualizar_temporizador, 1)
        # Limitar el número de preguntas según la configuración
        app = App.get_running_app()
        config = cargar_configuracion()
        num_preguntas = config.get("num_preguntas", 10)
        preguntas_aleatorias = config.get("preguntas_aleatorias", True)  # Cargar el valor de "preguntas_aleatorias"
        # Aplicar el orden de las preguntas según "preguntas_aleatorias"
        if preguntas_aleatorias:
            random.shuffle(app.preguntas)  # Mezclar las preguntas si están habilitadas como aleatorias
        else:
            # Mantener el orden original del archivo JSON
            pass  # No hacer nada, ya que las preguntas ya están en el orden original
        app.preguntas = app.preguntas[:num_preguntas]  # Limitar el número de preguntas
        self.mostrar_pregunta()

    def actualizar_temporizador(self, dt):
        """Actualiza el temporizador cada segundo."""
        self.tiempo_transcurrido += 1
        minutos = self.tiempo_transcurrido // 60
        segundos = self.tiempo_transcurrido % 60
        self.temporizador.text = f"{minutos:02}:{segundos:02}"

    def mostrar_pregunta(self):
        app = App.get_running_app()
        if self.current_index < len(app.preguntas):
            # Reiniciar el flag de respuesta seleccionada
            self.respuesta_seleccionada = False
            # Obtener la pregunta actual
            pregunta = app.preguntas[self.current_index]
            self.label.text = pregunta["enunciado"]
            opciones = pregunta["opciones"]
            config = cargar_configuracion()
            # Separar letras y textos
            letras = [op["letra"] for op in opciones]
            textos = [op["texto"] for op in opciones]
            # Guardar la respuesta correcta original (por ejemplo, "a")
            respuesta_correcta_original = pregunta["respuesta_correcta"]
            # Si la opción "Respuestas aleatorias" está activada, mezclar solo los textos
            if config.get("aleatorio", False):
                random.shuffle(textos)
                # Encontrar la nueva letra asociada al texto correcto
                texto_correcto = next(op["texto"] for op in opciones if op["letra"] == respuesta_correcta_original)
                nueva_letra_correcta = letras[textos.index(texto_correcto)]
                self.respuesta_correcta_actualizada = nueva_letra_correcta  # Guardar la nueva letra correcta
            else:
                # Mantener el orden original y usar la respuesta correcta del JSON
                self.respuesta_correcta_actualizada = respuesta_correcta_original
            # Volver a combinar letras con los textos mezclados (si aplica)
            opciones_mezcladas = [{"letra": letra, "texto": texto} for letra, texto in zip(letras, textos)]
            # Limpiar los botones antes de agregar nuevas opciones
            for btn in self.botones:
                btn.clear_widgets()  # Limpiar el contenido del botón
                btn.md_bg_color = "blue"  # Restablecer el color de los botones
                btn.disabled = False  # Habilitar los botones explícitamente
            # Cargar las opciones en los botones
            for i, opcion in enumerate(opciones_mezcladas):
                btn = self.botones[i]
                btn.correcta = opcion["letra"] == self.respuesta_correcta_actualizada  # Usar la respuesta actualizada
                # Agregar un MDLabel dentro del botón para ajustar el texto en varias líneas
                btn_label = MDLabel(
                    text=f"{opcion['letra']}) {opcion['texto']}",
                    halign="left",
                    valign="middle",
                    bold=True,
                    size_hint_y=None,
                    text_size=(btn.width - dp(20), None),
                    theme_text_color="Custom",
                    text_color="white"
                )
                btn_label.bind(texture_size=btn_label.setter("size"))
                btn.add_widget(btn_label)
                # Ajustar la altura del botón dinámicamente según el texto
                btn.height = max(dp(100), btn_label.texture_size[1] + dp(40))
            # Deshabilitar el botón "Siguiente" hasta que se seleccione una respuesta
            self.btn_siguiente.disabled = True

    def verificar_respuesta(self, instance):
        # Verificar si ya se seleccionó una respuesta
        if hasattr(self, "respuesta_seleccionada") and self.respuesta_seleccionada:
            return  # Ignorar nuevas interacciones si ya se seleccionó una respuesta
        # Marcar que se ha seleccionado una respuesta
        self.respuesta_seleccionada = True
        # Cambiar el color del botón seleccionado
        if instance.correcta:
            instance.md_bg_color = "green"  # Respuesta correcta: verde
            self.correctas += 1
        else:
            instance.md_bg_color = "red"  # Respuesta incorrecta: rojo
            # Cambiar el color del botón de la respuesta correcta a verde
            for btn in self.botones:
                if btn.correcta:
                    btn.md_bg_color = "green"
        # Habilitar el botón "Siguiente"
        self.btn_siguiente.disabled = False

    def siguiente_pregunta(self, instance):
        self.current_index += 1
        if self.current_index >= len(App.get_running_app().preguntas):
            # Detener el temporizador al finalizar el test
            Clock.unschedule(self.temporizador_evento)
            # Guardar el progreso
            progreso = cargar_progreso()
            progreso["correctas"] += self.correctas
            progreso["contestadas"] += self.current_index
            guardar_progreso(progreso)
            # Ir a la pantalla de progreso
            self.manager.current = "progreso"
        else:
            self.mostrar_pregunta()

    def salir_test(self, instance):
        # Detener el temporizador al abandonar el test
        Clock.unschedule(self.temporizador_evento)
        # Volver al menú principal
        self.manager.current = "menu"


class ProgresoScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation="vertical", spacing=dp(20), padding=dp(20))
        layout.add_widget(MDLabel(text="Resultados", font_style="H5", halign="center", font_size=dp(20), theme_text_color="Custom", text_color="#9C1AB6"))
        progreso = cargar_progreso()
        layout.add_widget(MDLabel(text=f"Correctas: {progreso['correctas']}", font_size=dp(18), theme_text_color="Custom", text_color="#9C1AB6"))
        layout.add_widget(MDLabel(text=f"Contestadas: {progreso['contestadas']}", font_size=dp(18), theme_text_color="Custom", text_color="#9C1AB6"))
        btn_volver = MDRaisedButton(text="Volver", size_hint=(None, None), size=(dp(200), dp(50)), md_bg_color="#F78F1E", text_color="#FFFFFF")
        btn_volver.bind(on_release=self.volver_menu)
        layout.add_widget(btn_volver)
        self.add_widget(layout)

    def volver_menu(self, instance):
        self.manager.current = "menu"


class MenuScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        # Crear un FloatLayout para superponer widgets
        layout = FloatLayout()
        # Cargar background.png
        background_image = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False
        )
        layout.add_widget(background_image)
        # Crear el BoxLayout principal
        box_layout = BoxLayout(orientation="vertical", spacing=dp(20), padding=dp(20))
        # Título de la pantalla
        box_layout.add_widget(
            MDLabel(
                text="",
                font_style="H4",
                halign="center",
                font_size=dp(20),
                theme_text_color="Custom",
                text_color="#FFFFFF"  # Cambiar el color del texto para que sea visible sobre el fondo
            )
        )
        # Botones
        botones = [
            ("Iniciar Cuestionario", "iniciar"),
            ("Ver Últimos Resultados", "progreso"),
            ("Configuración", "config"),
            ("Salir", "salir"),
        ]
        for texto, screen in botones:
            if screen == "salir":
                btn = MDRaisedButton(text=texto, size_hint=(None, None), size=(dp(200), dp(50)), md_bg_color="#F78F1E", text_color="#FFFFFF")
            else:
                btn = MDRaisedButton(text=texto, size_hint=(None, None), size=(dp(200), dp(50)), md_bg_color="#F8B400", text_color="#FFFFFF")
            btn.bind(on_release=lambda btn, scr=screen: self.cambiar_pantalla(scr))
            box_layout.add_widget(btn)
        # Añadir el BoxLayout al FloatLayout
        layout.add_widget(box_layout)
        self.add_widget(layout)

    def cambiar_pantalla(self, screen_name):
        if screen_name == "salir":
            App.get_running_app().stop()
        else:
            self.manager.current = screen_name


class CuestionarioApp(MDApp):
    def build(self):
        # Cargar la configuración al iniciar la aplicación
        self.config = cargar_configuracion()
        # Establecer el tema inicial según el valor de "modo_oscuro"
        if self.config.get("modo_oscuro", False):  # Si "modo_oscuro" es True
            self.theme_cls.theme_style = "Dark"  # Activar modo oscuro
        else:
            self.theme_cls.theme_style = "Light"  # Activar modo claro
        # Crear el ScreenManager y agregar las pantallas
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name="menu"))
        self.sm.add_widget(ConfigScreen(name="config"))
        self.sm.add_widget(TemaScreen(name="iniciar"))
        self.sm.add_widget(ProgresoScreen(name="progreso"))
        self.sm.add_widget(QuizScreen(name="quiz"))
        self.sm.add_widget(RegisterScreen(name="register"))  # Añadir la pantalla de registro
        # Comprobar si la app está registrada
        if not self.config.get("progreso", "false") == "true":
            # Si no está registrada, mostrar la pantalla de registro
            self.sm.current = "register"
        else:
            # Si está registrada, mostrar el menú principal
            self.sm.current = "menu"
        return self.sm  # Devolver el ScreenManager completo


if __name__ == "__main__":
    CuestionarioApp().run()