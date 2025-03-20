# frontend/Dockerfile

FROM nginx:alpine

# Copy your static site content into /usr/share/nginx/html
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80
