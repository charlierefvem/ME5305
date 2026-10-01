# Debian bookworm-20250224-slim; package sources below are frozen separately.
FROM debian:bookworm-20250224-slim@sha256:12c396bd585df7ec21d5679bb6a83d4878bc4415ce926c9e5ea6426d23c60bdc

RUN rm -f /etc/apt/sources.list.d/debian.sources \
    && printf '%s\n' \
       'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20260930T000000Z bookworm main' \
       'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20260930T000000Z bookworm-updates main' \
       'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian-security/20260930T000000Z bookworm-security main' \
       > /etc/apt/sources.list \
    && apt-get -o Acquire::Check-Valid-Until=false update \
    && apt-get install --yes --no-install-recommends \
       ca-certificates git ghostscript pdf2svg poppler-utils librsvg2-bin \
       python3 python3-venv python3-pil \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/figure-requirements.txt
RUN python3 -m venv --system-site-packages /opt/figures \
    && /opt/figures/bin/pip install --no-cache-dir --require-hashes -r /opt/figure-requirements.txt
ENV PATH="/opt/figures/bin:${PATH}" PYTHONDONTWRITEBYTECODE=1 LANG=C.UTF-8
WORKDIR /work
