import { useState, useEffect } from "react";
import imagenReceta from "../src/images/1229080980.png";
import imagenSecreta from '../src/images/poio.png'

function App() {
  const [seleccion, setSeleccion] = useState({});
  const [ingrediente, setIngrediente] = useState([]);
  const [respuesta, setRespuesta] = useState([]);
  const [mostrarImagen, setMostrarImagen] = useState(false);
  const [mostrarTexto, setMostrarTexto] = useState(false);

  useEffect(() => {
    async function fetchIngredientes() {
      try {
        const response = await fetch("/ingredients.json");
        const data = await response.json();
        setIngrediente(data);
      } catch (error) {
        console.error("Error", error);
      }
    }
    fetchIngredientes();
  }, []);

  const manejarSeleccion = (nombre) => {
    setSeleccion((prevSeleccion) => ({
      ...prevSeleccion,
      [nombre]: !prevSeleccion[nombre],
    }));
  };

  const enviarSeleccion = async () => {
    const datos = { ingredientesSeleccionados: seleccion };
    try {
      const response = await fetch("http://localhost:5000/api/openai", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datos),
      });
      const data = await response.json();
      console.log(data);
      setRespuesta(data);
      setMostrarImagen(true);
      setMostrarTexto(true);
      if (response.ok) {
        console.log("Datos enviados correctamente");
      } else {
        console.error("Error al enviar datos al servidor");
      }
    } catch (error) {
      console.error("Error al realizar la solicitud:", error);
    }
  };

  return (
    <div className="flex flex-col m-10">
      <div className="grid grid-cols-3 gap-4 p-10">
        {ingrediente.map((ingrediente) => (
          <div key={ingrediente.id}>
            <label className="flex items-center">
              <input
                type="checkbox"
                onChange={() => manejarSeleccion(ingrediente.nombre)}
                className="mr-2"
              />
              {ingrediente.nombre}
            </label>
          </div>
        ))}
      </div>
      <button
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
        onClick={enviarSeleccion}
      >
        Aceptar ingredientes
      </button>
      <div className="px-10 py-2">
        <h1 className="text-3xl font-bold mt-4">{respuesta.titulo}</h1>
        {mostrarTexto && <h3 className="text-2xl mt-4">Ingredientes:</h3>}
        <p className="p-5">{respuesta.ingredientes}</p>
        {mostrarTexto && <h3 className="text-2xl mt-">Procedimiento:</h3>}
        <p className="p-5 text-pretty">{respuesta.procedimiento}</p>
        <div className="flex p-10 justify-center align-middle">
          {mostrarImagen && (
            <img src={imagenReceta} className="size-96" alt="Receta" />
          )}
        </div>
        <div className="flex justify-end m-10 p-2">
          <img src={imagenSecreta} alt="imagenSecreta" className="size-10 opacity-50" />
        </div>
      </div>
    </div>
  );
}

export default App;
