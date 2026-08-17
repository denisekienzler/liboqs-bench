ARG VERSION=latest

FROM alpine:$VERSION AS build

# Download liboqs-bench
ADD  https://github.com/denisekienzler/liboqs-bench.git /root/liboqs-bench/

# Client stage

FROM alpine:$VERSION AS client

LABEL "liboqs-bench.container"="client"
LABEL "liboqs-bench.client.version"="0.1.1"
LABEL "liboqs-bench.client.description"="Docker container for connecting to liboqs-bench server as client."
LABEL "liboqs-bench.client.warning"="Only test functionality."

# Install python
RUN apk add --no-cache python3

# Copy client package
COPY --from=build --parents /root/liboqs-bench/src/liboqs_bench_client/ .

# Start client
WORKDIR /root/liboqs-bench/src
ENTRYPOINT ["python3", "-m", "liboqs_bench_client", "-dH", "172.17.0.2", "Decapsulation", "ML-KEM-512"]

