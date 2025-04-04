# Usa una imagen base de Node.js
FROM node:18-alpine

# Crea un directorio de trabajo
WORKDIR /app

# Copia package.json y package-lock.json primero para instalar dependencias
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto del código
COPY . .

# Construye la aplicación de Next.js
RUN npm run build

# Expone el puerto en el contenedor (3000 por defecto en Next.js)
EXPOSE 3000

# Arranca la aplicación en modo producción
CMD ["npm", "start"]
