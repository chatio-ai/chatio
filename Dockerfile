FROM python:3.12-alpine AS build

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV TERM=xterm-256color
ENV FORCE_COLOR=1

RUN --mount=type=cache,target=/root/.cache/pip \
	pip install --break-system-packages --root-user-action ignore --upgrade pip

WORKDIR /app

FROM build AS devel

COPY ./requirements.txt .
COPY ./requirements.tools.txt .

RUN --mount=type=cache,target=/root/.cache/pip pip wheel -w ./wheels -r ./requirements.txt -r ./requirements.tools.txt

COPY ./src ./src
COPY ./share ./share
COPY ./setup.cfg .

RUN --mount=type=cache,target=/root/.cache/pip touch ./pyproject.toml && pip wheel -w ./wheels .

FROM build AS final

RUN --mount=type=cache,target=/root/.cache/pip \
	--mount=type=bind,from=devel,source=/app/wheels,target=/app/wheels \
	pip install --break-system-package --root-user-action=ignore --upgrade \
		--no-index --find-links=./wheels ./wheels/*.whl

COPY ./entrypoint.sh ./entrypoint.sh

RUN adduser -D chatio

USER chatio

WORKDIR /app/var

ENV PYTHONDEVMODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/app/entrypoint.sh"]
