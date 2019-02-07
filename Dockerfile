FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN ./install_software.sh

# Set the python path
ENV PYTHONPATH /app/lib/python3.5/site-packages/:/app/lib/

# Create a user that does not have root privileges 
ARG username=physicist
ENV MY_UID 1000
RUN useradd --create-home --home-dir /home/${username} --uid ${MY_UID} ${username}
ENV HOME /home/${username}

# Set the cwd to /home/{username}
WORKDIR /home/${username}

# Switch to our newly created user
USER ${username}


COPY . ${HOME}
USER root
RUN chown -R ${MY_UID} ${HOME}
USER ${username}



# Allow incoming connections on port 8888
EXPOSE 8888

# Run notebook when the container launches
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--allow-root"]
