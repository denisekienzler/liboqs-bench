ARG VERSION=latest

FROM alpine:$VERSION AS build

# Install prerequisites
RUN apk add --no-cache cmake build-base ninja-build git openssl-dev openssl-libs-static openssl

# Optionally build liboqs yourself
#ADD https://github.com/open-quantum-safe/liboqs.git liboqs/
#WORKDIR liboqs/
#cmake -S liboqs -B liboqs/build -DBUILD_SHARED_LIBS=ON
#cmake --build liboqs/build --parallel 8
#cmake --build liboqs/build --target install

# Download liboqs-bench
ADD https://github.com/denisekienzler/liboqs-bench.git /root/liboqs-bench/

# Install liboqs-python and liboqs (if not installed already)
RUN << EOF
apk add --no-cache python3 py3-pip
pip install --break-system-packages liboqs-python
python -c 'import oqs'
EOF

# Server stage container
FROM alpine:$VERSION AS server
EXPOSE 31021
LABEL "liboqs-bench.container"="server"
LABEL "liboqs-bench.server.version"="0.2.0"
LABEL "liboqs-bench.server.description"="Docker container for exposing liboqs-bench as server."

# Copy liboqs and liboqs-bench directories
COPY --from=build /root/_oqs /root/_oqs/
COPY --from=build /root/liboqs-bench/src/liboqs_bench/ /root/liboqs-bench/src/liboqs_bench/

# Install liboqs-python and liboqs_bench
RUN << EOF
apk add --no-cache python3 py-pip
pip install --break-system-packages liboqs-python
EOF

# Start server
WORKDIR /root/liboqs-bench/src
ENTRYPOINT ["python3", "-m", "liboqs_bench", "-sdH", "0.0.0.0"]

