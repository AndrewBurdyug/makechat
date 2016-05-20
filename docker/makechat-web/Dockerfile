FROM nginx:latest
MAINTAINER Andrew Burdyug <buran83@gmail.com>

RUN mkdir -pv /etc/nginx/makechat
RUN mkdir -pv /usr/share/nginx/html/makechat/default

WORKDIR /usr/share/nginx/html/makechat/default

ADD https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.3/jquery.min.js .
ADD https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.map .
ADD https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js .
ADD https://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.3.3/backbone-min.map .
ADD https://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.3.3/backbone-min.js .
ADD https://cdnjs.cloudflare.com/ajax/libs/normalize/4.1.1/normalize.min.css .
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/semantic.min.css .
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/semantic.min.js .
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/basic/assets/fonts/icons.eot ./themes/basic/assets/fonts/icons.eot
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/basic/assets/fonts/icons.svg ./themes/basic/assets/fonts/icons.svg
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/basic/assets/fonts/icons.ttf ./themes/basic/assets/fonts/icons.ttf
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/basic/assets/fonts/icons.woff ./themes/basic/assets/fonts/icons.woff
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/default/assets/fonts/icons.eot ./themes/default/assets/fonts/icons.eot
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/default/assets/fonts/icons.otf ./themes/default/assets/fonts/icons.otf
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/default/assets/fonts/icons.svg ./themes/default/assets/fonts/icons.svg
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/default/assets/fonts/icons.ttf ./themes/default/assets/fonts/icons.ttf
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/default/assets/fonts/icons.woff ./themes/default/assets/fonts/icons.woff
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/default/assets/fonts/icons.woff2 ./themes/default/assets/fonts/icons.woff2
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/default/assets/images/flags.png ./themes/default/assets/images/flags.png
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/github/assets/fonts/octicons-local.ttf ./themes/github/assets/fonts/octicons-local.ttf
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/github/assets/fonts/octicons.svg ./themes/github/assets/fonts/octicons.svg
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/github/assets/fonts/octicons.ttf ./themes/github/assets/fonts/octicons.ttf
ADD https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.1.8/themes/github/assets/fonts/octicons.woff ./themes/github/assets/fonts/octicons.woff
ADD https://cdnjs.cloudflare.com/ajax/libs/nunjucks/2.4.2/nunjucks.min.js .

RUN find -type f -exec chmod +r {} \;

COPY html/ .
COPY js/ .


ADD makechat_vhost.conf /etc/nginx/makechat/
ADD makechat_maintenance_vhost.conf /etc/nginx/makechat/
ADD maintenance /usr/local/sbin/

RUN ln -s  /etc/nginx/makechat/makechat_vhost.conf /etc/nginx/conf.d/makechat_vhost.conf

VOLUME /usr/share/nginx/html/makechat/custom
