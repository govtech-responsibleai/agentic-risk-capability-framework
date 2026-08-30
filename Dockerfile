FROM gdssingapore/airbase:python-3.13
ENV PYTHONUNBUFFERED=TRUE

# Copy requirements.txt from app folder and install dependencies
COPY --chown=app:app app/requirements.txt ./
RUN pip install -r requirements.txt

# Copy the app folder
COPY --chown=app:app app/ ./app/

# Copy the ARC risk register (single source of truth for the app's data)
COPY --chown=app:app arc-risk-register/ ./arc-risk-register/

# Copy .deploy.env as .env file
COPY --chown=app:app .env ./.env

USER app
CMD ["bash", "-c", "streamlit run app/app.py --server.port=$PORT"]
