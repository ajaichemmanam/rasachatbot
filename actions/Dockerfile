FROM rasa/rasa-sdk:1.10.2
ADD . /app/actions
ENTRYPOINT []

# In case of any dependency in actions.py
# We can install the libraries in docker by 
# Add a custom system library (e.g. git)
# RUN apt-get update && \
#     apt-get install -y git

# Add a custom python library (e.g. jupyter)
# RUN pip install --no-cache-dir jupyter

# Start the actions server
CMD python3 -m rasa-sdk --actions actions -p $PORT