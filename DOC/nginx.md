    server {
        listen       80;
        server_name  farm.dsnet.ru;
        root    /home/www/farm/;

        access_log /var/log/nginx/farm.access.log;
        error_log /var/log/nginx/farm.error.log;

        #location ~ (?<URL>^.*/[^/.]+$) {
        #    return 301 http://$host$url/$is_args$args;
        #}

        location /static {
                 alias /home/www/farm/static;
        }

        location / {
                uwsgi_buffer_size 64k;
                uwsgi_buffers 8 64k;
                uwsgi_busy_buffers_size 64k;

                uwsgi_read_timeout 300;
                uwsgi_send_timeout 300;

                uwsgi_connect_timeout 60;
                uwsgi_pass              unix:/var/run/uwsgi/uwsgi-farm.sock;
                include                 uwsgi_params;

                uwsgi_param          UWSGI_CHDIR             /home/www/farm;
                uwsgi_param          UWSGI_FILE              TakedaAnalitic/wsgi.py;
                #uwsgi_param          SCRIPT_NAME             wsgi.py;
        }
    }
