# Stage 1: Build stage
FROM mcr.microsoft.com/openjdk/jdk:21-ubuntu AS builder

# Set working directory
WORKDIR /workspace

# Copy Gradle wrapper and build files
COPY java/socialapp/gradlew .
COPY java/socialapp/gradle gradle
COPY java/socialapp/build.gradle .
COPY java/socialapp/settings.gradle .

# Download dependencies (cached layer)
RUN ./gradlew dependencies --no-daemon || true

# Copy source code
COPY java/socialapp/src src

# Build the application
RUN ./gradlew bootJar --no-daemon -x test

# Stage 2: Custom JRE extraction
FROM mcr.microsoft.com/openjdk/jdk:21-ubuntu AS jre-builder

# Create custom JRE with jlink
RUN jlink \
    --add-modules java.base,java.logging,java.xml,java.desktop,java.management,java.naming,java.sql,java.security.jgss,jdk.security.jgss,jdk.unsupported,java.instrument,java.compiler \
    --strip-debug \
    --no-man-pages \
    --no-header-files \
    --compress=2 \
    --output /jre

# Stage 3: Runtime stage
FROM ubuntu:22.04

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy custom JRE from jre-builder stage
COPY --from=jre-builder /jre /opt/java/openjdk

# Set JAVA_HOME and PATH
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Create app directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application from builder stage
COPY --from=builder /workspace/build/libs/*.jar app.jar

# Create SQLite database file
RUN touch sns_api.db && \
    chown appuser:appuser sns_api.db && \
    chmod 664 sns_api.db

# Change ownership of app directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD test -f /app/app.jar || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
CMD ["--spring.datasource.url=jdbc:sqlite:sns_api.db"]
