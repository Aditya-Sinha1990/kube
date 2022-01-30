FROM python:3.9-alpine

USER root
# Create User Directory
RUN adduser -D aditya
WORKDIR /home/aditya

# Copy package files in Image
COPY requirements.txt \
    entrypoint.sh ./
COPY app2_files app_files

# Exposing tcp port 9092
EXPOSE 9092/tcp

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
