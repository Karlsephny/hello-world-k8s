# Hello World на minikube — тестовое задание

Простое веб-приложение на Flask, упакованное в Docker-образ и развёрнутое в
локальном кластере Kubernetes (minikube) с 2 репликами и доступом через
`kubectl port-forward`.

## Структура репозитория

```
hello-world-devops/
├── app.py                  # приложение (Flask, порт 32777)
├── requirements.txt        # зависимости Python
├── Dockerfile               # сборка образа
├── .dockerignore
├── .gitignore
├── k8s/
│   ├── deployment.yaml     # Deployment, 2 реплики
│   └── service.yaml        # Service (ClusterIP)
├── diagrams/
│   └── architecture.drawio # схема — открыть на app.diagrams.net
└── README.md
```

## Шаг 1. Приложение "Hello World" (порт 32777)

## Шаг 2. Установка Docker

## Шаг 3. Сборка образа и публикация на Docker Hub

## Шаг 4. Установка Minikube и запуск кластера

## Шаги 5–6. Deployment (2 реплики) и Service

## Шаг 7. Проброс портов и проверка в браузере

## Шаг 8. Публикация в открытом Git-репозитории

## Шаг 9. Что приложить в качестве результата


## Полезные команды для отладки

```bash
kubectl describe pod <имя_пода>
kubectl logs <имя_пода>
kubectl get events --sort-by=.metadata.creationTimestamp
minikube dashboard          # визуальный обзор кластера
minikube delete             # снести кластер после завершения работы
```
