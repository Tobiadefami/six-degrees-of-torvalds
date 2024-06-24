# Use an official Nginx runtime as a parent image
FROM nginx:alpine

# Copy the custom Nginx configuration file to the container
COPY default.conf /etc/nginx/conf.d/default.conf

# Expose the port Nginx will run on
EXPOSE 8080

# Command to run Nginx
CMD ["nginx", "-g", "daemon off;"]
