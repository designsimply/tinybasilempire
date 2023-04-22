# ------------------------------------------------------------------------ #
# Base Image
# ------------------------------------------------------------------------ #

FROM python:3

# ------------------------------------------------------------------------ #
# App
# ------------------------------------------------------------------------ #

ENV APPDIR=/app \
    ENVDIR=/app/env

WORKDIR ${APPDIR}

COPY requirements.txt .
RUN python -m venv ${ENVDIR} \
    && pip install --no-cache -r requirements.txt

# ------------------------------------------------------------------------ #
# Reverse Proxy with nginx to handle client requests
# ------------------------------------------------------------------------ #

FROM nginx:1.23.4-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# ------------------------------------------------------------------------ #
# Source Files
# ------------------------------------------------------------------------ #

ENV SOURCEDIR=${APPDIR}/src
ENV PATH=${PATH}:${SOURCEDIR}/bin:${ENVDIR}/bin \
    PYTHONPATH=${SOURCEDIR}

WORKDIR ${SOURCEDIR}

COPY bin bin/
COPY db db/
COPY static static/
COPY templates templates/
COPY app.py .
COPY config.py .

EXPOSE 8000
CMD [ "run.sh" ]
