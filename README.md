# Hello World на Kubernetes — тестовое задание (System Administrator / Junior DevOps)

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

## Важный нюанс про порт 32777

По умолчанию Kubernetes выделяет NodePort из диапазона **30000–32767**.
Порт из задания, **32777, в этот диапазон не входит** (он на 10 больше
максимума), поэтому напрямую использовать его как `nodePort` не получится —
кластер отклонит такой Service с ошибкой валидации.

Из этого следует осознанный выбор архитектуры: приложение слушает `32777`
**внутри** контейнера/Service (ClusterIP), а наружу оно "выходит" через
`kubectl port-forward`, который сам создаёт локальный туннель на любой порт,
включая 32777. Это ровно то, что просит пункт 7 задания ("режим проброса
портов"), так что всё сходится. На собеседовании это отличный повод
показать, что вы не просто скопировали YAML, а понимаете, почему сделали
именно так.

## Шаг 1. Приложение "Hello World" (порт 32777)

Локальный запуск без Docker (удобно для быстрой проверки):

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Откройте `http://localhost:32777` — должна появиться страница с "Hello,
World!" и hostname контейнера/машины. Есть также `/health` — отдаёт JSON
`{"status": "ok"}`, он используется как readiness/liveness проверка в
Kubernetes.

## Шаг 2. Установка Docker

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# чтобы не писать sudo перед каждой командой docker
sudo usermod -aG docker $USER
newgrp docker
```

**macOS / Windows:** установите Docker Desktop с официального сайта
(docker.com/products/docker-desktop) и запустите его.

Проверка после установки:

```bash
docker --version
docker run hello-world
```

> Если из России Docker Hub недоступен напрямую (таймауты при `docker
> pull`/`push`), обычно помогает VPN или зеркало реестра (например, Yandex
> Container Registry как pull-through mirror). Это не блокер для задания —
> просто держите в уме на случай проблем с сетью.

## Шаг 3. Сборка образа и публикация на Docker Hub

```bash
docker login

docker build -t <DOCKERHUB_USERNAME>/hello-world:1.0.0 .

# локальная проверка перед публикацией
docker run --rm -p 32777:32777 <DOCKERHUB_USERNAME>/hello-world:1.0.0
# в другом терминале: curl http://localhost:32777

docker push <DOCKERHUB_USERNAME>/hello-world:1.0.0
```

Замените `<DOCKERHUB_USERNAME>` на свой логин везде, включая
`k8s/deployment.yaml`. Тег `1.0.0` использован намеренно вместо `latest` —
это хорошая практика: в Kubernetes образ с конкретной версией по умолчанию
скачивается с политикой `IfNotPresent`, а `latest` — с `Always`, что для
воспроизводимых деплоев хуже (можно неявно словить не ту версию).

Скриншоты для отчёта на этом шаге: вывод `docker images`, вывод `docker
push` (видно слои и digest), страница образа на Docker Hub.

## Шаг 4. Установка Minikube и запуск кластера

Официальная инструкция: https://minikube.sigs.k8s.io/docs/start/

**Linux (x86-64, бинарник):**

```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

**macOS (Homebrew):**

```bash
brew install minikube
```

**Windows (winget):**

```powershell
winget install Kubernetes.minikube
```

Если `kubectl` ещё не установлен — либо ставьте отдельно
(kubernetes.io/docs/tasks/tools/), либо используйте `minikube kubectl --`
вместо `kubectl` во всех командах ниже.

Запуск кластера (драйвер `docker` — самый простой вариант, раз Docker уже
установлен на шаге 2):

```bash
minikube start --driver=docker
minikube status
```

Скриншот: вывод `minikube status` (все компоненты `Running`).

## Шаги 5–6. Deployment (2 реплики) и Service

Перед применением подставьте свой логин Docker Hub в
`k8s/deployment.yaml` (замените `<DOCKERHUB_USERNAME>`).

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl rollout status deployment/hello-world-deployment
kubectl get deployments
kubectl get pods -o wide
kubectl get svc
```

В выводе `kubectl get pods -o wide` должно быть **2 пода** в статусе
`Running`. Это ключевой скриншот для отчёта.

## Шаг 7. Проброс портов и проверка в браузере

```bash
kubectl port-forward service/hello-world-service 32777:32777
```

Оставьте команду выполняться и откройте в браузере
`http://localhost:32777`. Обновите страницу пару раз — можно увидеть,
что hostname пода не всегда меняется при port-forward (он держит туннель к
одному поду за раз) — это нормально и тоже хороший повод для рассказа на
собеседовании про разницу между `port-forward` и настоящей балансировкой
через `kube-proxy`.

Альтернатива, чтобы увидеть балансировку между обеими репликами (не входит
в обязательные шаги, но полезно для демонстрации): временно поменять тип
сервиса на `NodePort` (порт из диапазона 30000–32767, не 32777) и открыть
через `minikube service hello-world-service`.

Скриншоты: терминал с запущенным `port-forward` + окно браузера с
открытой страницей.

## Шаг 8. Публикация в открытом Git-репозитории

```bash
git init
git add .
git commit -m "Hello world app + Docker + k8s deployment (2 replicas) + service"
git branch -M main
git remote add origin <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
git push -u origin main
```

`.gitignore` уже добавлен, чтобы в репозиторий не попали `venv/`,
`__pycache__/` и т.п. Несколько осмысленных коммитов (а не один "final")
производят более профессиональное впечатление, чем один большой пуш.

## Шаг 9. Что приложить в качестве результата

1. **Ссылка на репозиторий.**
2. **Схема (draw.io):** `diagrams/architecture.drawio` — откройте файл на
   https://app.diagrams.net (File → Open From → Device), при желании
   отредактируйте, затем экспортируйте PNG (File → Export as → PNG) и
   приложите картинку рядом со скриншотами.
3. **Скриншоты:**
   - `docker images` и `docker push` (или страница репозитория на Docker Hub);
   - `minikube status`;
   - `kubectl get pods -o wide` (видно 2 running пода);
   - `kubectl get svc`;
   - терминал с `kubectl port-forward` + окно браузера с открытым
     `http://localhost:32777`.

## На что реально смотрит интервьюер (кратко)

- Понимание **зачем**, а не только "команды сработали": будьте готовы
  объяснить каждую строчку YAML и Dockerfile.
- Осознанный выбор тега образа (`1.0.0`, не `latest`) и типа Service.
- `readinessProbe`/`livenessProbe` и `resources.requests/limits` в
  Deployment — не обязательны по заданию, но их наличие сразу поднимает
  впечатление от уровня кандидата.
- Аккуратный README и история коммитов — тоже часть работы, не
  "довесок".
- Готовность объяснить нюанс с портом 32777 и диапазоном NodePort —
  показывает, что вы реально разобрались, а не гадали.

## Полезные команды для отладки

```bash
kubectl describe pod <имя_пода>
kubectl logs <имя_пода>
kubectl get events --sort-by=.metadata.creationTimestamp
minikube dashboard          # визуальный обзор кластера
minikube delete             # снести кластер после завершения работы
```
