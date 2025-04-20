# Usa una imagen base de Node.js
FROM node:18-alpine

# Establece el directorio de trabajo
WORKDIR /app

# 🛠️ Previene errores de oxide en Alpine
ENV TAILWIND_DISABLE_PREBUILD=true

# Copia los archivos de dependencias
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto del código fuente
COPY . .

# Compila la aplicación
RUN npm run build

# Expone el puerto de Next.js
EXPOSE 3000

# Comando por defecto al iniciar el contenedor
CMD ["npm", "start"]
