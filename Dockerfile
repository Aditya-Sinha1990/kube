FROM python:3.7-alpine

USER root
# Create User Directory
RUN adduser -D aditya
WORKDIR /home/aditya

# expect a build-time variable name "APP_FILES_PASSED"
ARG APP_FILES_PASSED
ENV APP_FILES_PASSED_ARG=${APP_FILES_PASSED}

# Copy package files in Image
COPY requirements.txt \
    entrypoint.sh ./
COPY ${APP_FILES_PASSED_ARG} app_files

# Meet Dependencies and Executables
RUN chmod +x entrypoint.sh \
    && echo `python3 --version` \
    && python3 -m pip install -r requirements.txt \
    && ls -lsa /home/aditya/
RUN apk --no-cache add curl
RUN apk add --update sudo

#Give Ownership to Image Runtime User
RUN chown -R aditya:aditya ./
#Make Image runtime user as aditya
USER aditya
ENTRYPOINT ["./entrypoint.sh"]