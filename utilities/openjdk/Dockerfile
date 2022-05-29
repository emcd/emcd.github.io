FROM openjdk:jdk-bullseye

ENV KOTLIN_RELEASE="349"
ENV KOTLIN_VERSION="1.6.21"

RUN set -eux \
    && mkdir -p /opt/kotlin \
    && cd /opt/kotlin \
    && kotlin_directory="kotlin-native-linux-x86_64-${KOTLIN_VERSION}-${KOTLIN_RELEASE}" \
    && kotlin_tarball="${kotlin_directory}.tar.gz" \
    && curl --location --remote-name \
        "https://github.com/JetBrains/kotlin/releases/download/v${KOTLIN_VERSION}/${kotlin_tarball}" \
    && tar --extract --gzip --file="${kotlin_tarball}" --strip-components=1 \
    && rm "${kotlin_tarball}" \
    && cd -

ENV PATH="/opt/kotlin/bin:${PATH}"
