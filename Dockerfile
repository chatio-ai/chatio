FROM python:3.12 AS build

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV TERM=xterm-256color
ENV FORCE_COLOR=1

RUN pip install --upgrade pip

WORKDIR /app/

COPY ./requirements.txt .

RUN pip install --break-system-packages --upgrade -r requirements.txt

FROM build AS devel

COPY ./requirements.dev.txt .

RUN pip install --break-system-packages --upgrade -r requirements.dev.txt

COPY ./src ./src
COPY ./bin ./bin

COPY ./pyproject.toml ./

COPY ./lints ./lints

ARG LINTS=1

RUN --mount=type=cache,target=.mypy_cache \
	if test $LINTS -ne 0; then ./lints/run.sh; fi;

FROM build AS final

COPY --from=devel /app/src /app/src
COPY --from=devel /app/bin /app/bin

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src/

RUN useradd -d /app/var -m chatio

WORKDIR /app/var

USER chatio

ENTRYPOINT ["/app/bin/streamer.py"]
