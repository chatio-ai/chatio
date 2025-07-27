FROM python:3.12 AS build

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV TERM=xterm-256color
ENV FORCE_COLOR=1

RUN pip install --break-system-packages --root-user-action ignore --upgrade pip

WORKDIR /app/

COPY ./requirements.txt .

RUN pip install --break-system-packages --root-user-action ignore --upgrade -r requirements.txt

FROM build AS devel

COPY ./requirements.dev.txt .

RUN pip install --break-system-packages --root-user-action ignore --upgrade -r requirements.dev.txt

COPY ./src ./src

COPY ./setup.py ./

COPY ./pyproject.toml ./

COPY ./.pre-commit-config.yaml ./

ARG LINTS=1

RUN git init --quiet . && git add --all

RUN --mount=type=cache,target=.mypy_cache \
	if test $LINTS -ne 0; then pre-commit run --all-files --color=always; fi

FROM build AS final

COPY --from=devel /app/src ./build/src
COPY --from=devel /app/setup.py ./build/

RUN pip install --break-system-packages --root-user-action ignore --upgrade ./build && rm -rf ./build

ENV PYTHONDEVMODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src/

RUN useradd -d /app/var -m chatio

WORKDIR /app/var

USER chatio

ENTRYPOINT ["chatio"]
