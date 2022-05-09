FROM php:7.2-apache

RUN apt update \
    && apt install iproute2 -y \
    && docker-php-ext-install mysqli pdo pdo_mysql

WORKDIR /var/www/html/
COPY ./html/ .
RUN chmod -R 777 assets/users/

WORKDIR /var/www/documentation
COPY ./documentation/ .

COPY ./000-default.conf /etc/apache2/sites-available/

RUN a2enmod rewrite