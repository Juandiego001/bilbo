# Billos Orders - Frontend

Frontend del proyecto `Billos Orders` basado en la siguiente plantilla: [https://dribbble.com/shots/22371252-Bitepoint-Restaurant-POS-System-Orders-Payment](https://dribbble.com/shots/22371252-Bitepoint-Restaurant-POS-System-Orders-Payment)

## ¿Cómo ejecutar el frontend?

```bash
# Clonar el repositorio
git clone https://github.com/Juandiego001/billos-orders # Con HTTP
git clone git@github.com:Juandiego001/billos-orders.git # Con SSH

# Dirigrse al frontend
cd billos-orders/frontend

# Instalar los paquetes con Yarn 
yarn

# Agregar variable de entorno de comunicación con el backend
$env:API_URL='http://localhost:5000' # En Windows
echo "API_URL='http://localhost:5000'" > .env # En Linux

# Ejecutar frontend
yarn dev
```


