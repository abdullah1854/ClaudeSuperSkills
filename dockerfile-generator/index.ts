
const { language, port = 3000 } = inputs;

const templates = {
  node: `FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER nodejs
EXPOSE ${port}
CMD ["node", "dist/index.js"]`,

  python: `FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
USER appuser
EXPOSE ${port}
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${port}"]`,

  go: `FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-w -s" -o /app/server .

FROM alpine:3.19
RUN adduser -D -g '' appuser
COPY --from=builder /app/server /server
USER appuser
EXPOSE ${port}
ENTRYPOINT ["/server"]`
};

console.log(templates[language] || templates.node);
