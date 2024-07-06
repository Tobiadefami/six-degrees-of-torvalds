FROM openresty/openresty:1.21.4.1-0-alpine-apk

# Copy the custom Nginx configuration file to the container
COPY default.conf /usr/local/openresty/nginx/conf/nginx.conf
# Expose the port Nginx will run on
EXPOSE 8080

# Command to run Nginx
CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]
STOPSIGNAL SIGQUIT