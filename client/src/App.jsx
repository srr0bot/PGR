import { Box, Button, Checkbox, Container, Divider, FormControlLabel, FormGroup, Grid, ListItem, ListItemButton, ListItemText, Typography } from "@mui/material";
import React, { useState } from "react";
import { useEffect } from "react";
import imagenReceta from "../src/images/1229080980.png"

function App() {
  const [seleccion, setSeleccion] = useState({})
  const [ingrediente, setingrediente] = useState([])
  const [respuesta, setRespuesta] = useState([]);
  const [mostrarImagen, setMostrarImagen] = useState(false);
  const [mostrarTexto, setMostrarTexto] = useState(false); 

  useEffect(() => {
    async function fetchingrediente() {
      try {
        const response = await fetch('/ingredients.json')
        const data = await response.json()
        setingrediente(data)
      } catch (error) {
        console.error('Error', error)
      }
    }
    fetchingrediente()
  }, [])

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
      if (respuesta.ok) {
        console.log("Datos enviados correctamente");
      } else {
        console.error("Error al enviar datos al servidor");
      }
    } catch (error) {
      console.error("Error al realizar la solicitud:", error);
    }
  };

  return(
    <Container sx={{pt: 5}}>
        {ingrediente.map((ingrediente)=>(
            <div key={ingrediente.id}>
                <FormGroup>
                  <FormControlLabel control={<Checkbox/>} onChange={() => manejarSeleccion(ingrediente.nombre)} label={ingrediente.nombre}></FormControlLabel>
                </FormGroup>
            </div>
        ))}
      <Button variant="contained" onClick={enviarSeleccion}>Aceptar ingredientes</Button>
      <Typography variant="h1">{respuesta.titulo}</Typography>
      {mostrarTexto && <Typography variant="h3">Ingredientes:</Typography>}
      <Typography variant="body1">{respuesta.ingredientes}</Typography>
      {mostrarTexto && <Typography variant="h3">Procedimiento:</Typography>}
      <Typography variant="body1">{respuesta.procedimiento}</Typography>
      <Box component="section" sx={{ p: 2, border: '3', width: '500px', height: 'auto'}}>
      {mostrarImagen && (<img src={imagenReceta} style={{ width: "100%", height: "auto" }}/>)} 
      </Box>
    </Container>
  )
}

export default App;