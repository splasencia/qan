const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

module.exports = app; // Esto permite que supertest inicie el servidor para las pruebas

// Usar la cadena de conexión desde las variables de entorno
const mongoConnectionString = process.env.MONGODB_CONNECTION_STRING;

// Conexión a MongoDB
mongoose.connect(mongoConnectionString, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
}).then(() => console.log("MongoDB connected"))
  .catch(err => console.log(err));

// Modelo para los enlaces
const Link = mongoose.model('Link', new mongoose.Schema({
    title: String,
    url: String,
    thumbnail: String,
    description: String
}));

// Endpoint para obtener los enlaces
app.get('/links', async (req, res) => {
    const links = await Link.find();
    res.json(links);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
