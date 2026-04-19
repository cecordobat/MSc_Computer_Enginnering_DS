from flask import Flask, request
from flask_restx import Api, Resource, fields
from models.registro import Registro
from services.storage import guardar_registro, obtener_registros, obtener_por_indice

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="ControlAcceso API",
    description="Sistema de Registro de Ingreso de Personal",
    doc="/swagger"
)
ns = api.namespace("ingresos", description="Operaciones de ingreso")

modelo_input = api.model("RegistroInput", {
    "nombre_empleado": fields.String(required=True, min_length=1, description="Nombre completo del empleado"),
    "ingresa_computador": fields.Boolean(required=True, description="¿Ingresa con computador?"),
    "fecha_hora_entrada": fields.String(required=False, description="Fecha y hora en formato ISO 8601"),
    "marca_computador": fields.String(required=False, description="Marca del computador"),
    "serial_computador": fields.String(required=False, description="Serial único del computador"),
    "persona_autoriza": fields.String(required=False, description="Nombre de quien autoriza el computador")
})

modelo_output = api.model("RegistroOutput", {
    "nombre_empleado": fields.String,
    "ingresa_computador": fields.Boolean,
    "fecha_hora_entrada": fields.String,
    "marca_computador": fields.String,
    "serial_computador": fields.String,
    "persona_autoriza": fields.String
})

@ns.route("/")
class Ingresos(Resource):
    @ns.expect(modelo_input)
    @ns.response(201, "Registro creado exitosamente")
    @ns.response(400, "Error de validación de campos")
    @ns.response(409, "Serial de computador duplicado")
    @ns.response(500, "Error interno del servidor")
    def post(self):
        try:
            data = request.json
            registro = Registro(**data)
            guardar_registro(registro)
            return {"mensaje": "Registro creado", "timestamp": registro.fecha_hora_entrada}, 201
        except ValueError as e:
            code = 409 if "Serial" in str(e) else 400
            return {"error": str(e)}, code
        except Exception as e:
            return {"error": "Error interno del servidor"}, 500

    @ns.response(200, "Lista de registros")
    @ns.param("nombre", "Filtrar por nombre del empleado")
    @ns.param("fecha", "Filtrar por fecha (YYYY-MM-DD)")
    @ns.param("limit", "Límite de registros (máx 100)")
    def get(self):
        nombre = request.args.get("nombre")
        fecha = request.args.get("fecha")
        limite = min(int(request.args.get("limit", 50)), 100)
        registros = [r.to_dict() for r in obtener_registros(nombre, fecha, limite)]
        return {"registros": registros, "total": len(registros)}

@ns.route("/<int:id>")
class IngresoPorId(Resource):
    @ns.response(200, "Registro encontrado")
    @ns.response(404, "Registro no encontrado")
    def get(self, id):
        registro = obtener_por_indice(id)
        if not registro:
            return {"error": "Registro no encontrado"}, 404
        return registro.to_dict()

if __name__ == "__main__":
    app.run(debug=True, port=5000)