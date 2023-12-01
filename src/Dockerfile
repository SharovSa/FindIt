FROM python

COPY . .

RUN pip install --no-cache-dir -r req.txt

RUN playwright install-deps

RUN playwright install chromium

EXPOSE 5000
