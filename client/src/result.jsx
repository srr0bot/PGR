import React from "react";
import { useLocation } from "react-router-dom";
import imagenReceta from "../src/images/1229080980.png"; // Asegúrate de que la ruta sea correcta

function Result() {
  const location = useLocation();
  const { respuesta, mostrarImagen, mostrarTexto } = location.state || {
    respuesta: {},
    mostrarImagen: false,
    mostrarTexto: false,
  };

  return (
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
    </div>
  );
}

export default Result;
