# 🚀 Guia de Deploy no Kubernetes - mdb-health FHIR Server

## 📋 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet / Load Balancer                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Ingress Controller (NGINX)                  │
│                   - SSL Termination                          │
│                   - Rate Limiting                            │
│                   - Load Balancing                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              FastAPI Service (ClusterIP)                     │
│              - Internal Load Balancing                       │
└────┬──────────────┬──────────────┬──────────────┬───────────┘
     │              │              │              │
┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
│FastAPI  │   │FastAPI  │   │FastAPI  │   │FastAPI  │
│ Pod 1   │   │ Pod 2   │   │ Pod 3   │   │ Pod N   │
│100 users│   │100 users│   │100 users│   │100 users│
└────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│          PostgreSQL (RDS/Cloud SQL/StatefulSet)             │
│          - Managed Database Service                          │
│          - 500+ connections                                  │
│          - Automatic backups                                 │
│          - High Availability                                 │
└─────────────────────────────────────────────────────────────┘

HPA (Horizontal Pod Autoscaler):
- Min: 3 pods
- Max: 10 pods
- Trigger: CPU > 70% OR Memory > 80%
```

---

## 🎯 Benefícios do Kubernetes vs Docker Compose

| Recurso                | Docker Compose    | Kubernetes              |
| ---------------------- | ----------------- | ----------------------- |
| **Auto-scaling**       | ❌ Manual         | ✅ Automático (HPA)     |
| **Self-healing**       | ❌ Não            | ✅ Reinicia pods falhos |
| **Rolling updates**    | ⚠️ Limitado       | ✅ Zero-downtime        |
| **Load balancing**     | ⚠️ Manual (NGINX) | ✅ Nativo               |
| **Health checks**      | ⚠️ Básico         | ✅ Avançado             |
| **Resource limits**    | ⚠️ Básico         | ✅ Requests/Limits      |
| **Service discovery**  | ⚠️ DNS            | ✅ DNS + Endpoints      |
| **Secrets management** | ⚠️ .env files     | ✅ Secrets API          |
| **Multi-region**       | ❌ Não            | ✅ Sim                  |
| **Monitoring**         | ⚠️ Manual         | ✅ Prometheus/Grafana   |

---

## 🛠️ Pré-requisitos

### 1. Cluster Kubernetes

**Opções:**

**A) Managed Kubernetes (RECOMENDADO)**

```bash
# AWS EKS
eksctl create cluster \
  --name mdb-health \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 3 \
  --nodes-max 10

# Google GKE
gcloud container clusters create mdb-health \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 3 \
  --max-nodes 10

# Azure AKS
az aks create \
  --resource-group mdb-health-rg \
  --name mdb-health \
  --node-count 3 \
  --enable-cluster-autoscaler \
  --min-count 3 \
  --max-count 10 \
  --node-vm-size Standard_DS2_v2
```

**B) Local (Desenvolvimento)**

```bash
# Minikube
minikube start --cpus=4 --memory=8192

# Kind
kind create cluster --name mdb-health

# k3s (Lightweight)
curl -sfL https://get.k3s.io | sh -
```

### 2. Ferramentas

```bash
# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# helm (opcional mas recomendado)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# kustomize (opcional)
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
```

### 3. Container Registry

```bash
# Docker Hub (público)
docker login

# AWS ECR
aws ecr create-repository --repository-name mdb-health-fastapi
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Google GCR
gcloud auth configure-docker

# Azure ACR
az acr login --name mdbhealth
```

---

## 📦 Passo 1: Build e Push da Imagem

```bash
# 1. Build da imagem
cd /home/anderson/projects/RNDS/mdb-health
docker build -t mdb-health-fastapi:v1.0.0 ./fastapi

# 2. Tag para o registry
# Docker Hub
docker tag mdb-health-fastapi:v1.0.0 seuusuario/mdb-health-fastapi:v1.0.0

# AWS ECR
docker tag mdb-health-fastapi:v1.0.0 <account-id>.dkr.ecr.us-east-1.amazonaws.com/mdb-health-fastapi:v1.0.0

# Google GCR
docker tag mdb-health-fastapi:v1.0.0 gcr.io/<project-id>/mdb-health-fastapi:v1.0.0

# 3. Push
docker push seuusuario/mdb-health-fastapi:v1.0.0
```

---

## 🚀 Passo 2: Deploy no Kubernetes

### Método 1: kubectl apply (Simples)

```bash
# 1. Criar namespace
kubectl apply -f k8s/namespace.yaml

# 2. Criar secrets (IMPORTANTE: Mudar valores!)
kubectl create secret generic mdb-health-secret \
  --from-literal=POSTGRES_USER=fhir_admin \
  --from-literal=POSTGRES_PASSWORD=SUA-SENHA-SEGURA \
  --from-literal=API_TOKEN=seu-token-api \
  --from-literal=SUPERSET_SECRET_KEY=sua-chave-secreta \
  --from-literal=SUPERSET_ADMIN_PASSWORD=senha-admin \
  --from-literal=SUPERSET_DB_USER=superset_admin \
  --from-literal=SUPERSET_DB_PASS=senha-superset \
  -n mdb-health

# 3. Aplicar ConfigMap
kubectl apply -f k8s/configmap.yaml

# 4. Deploy PostgreSQL (APENAS PARA DEV - Use RDS em produção)
kubectl apply -f k8s/postgres-statefulset.yaml

# 5. Deploy FastAPI
kubectl apply -f k8s/fastapi-deployment.yaml
kubectl apply -f k8s/fastapi-service.yaml

# 6. Configurar Ingress
kubectl apply -f k8s/ingress.yaml

# 7. Configurar Auto-scaling
kubectl apply -f k8s/hpa.yaml

# 8. Configurar PodDisruptionBudget
kubectl apply -f k8s/pdb.yaml

# 9. (Opcional) Network Policy
kubectl apply -f k8s/network-policy.yaml
```

### Método 2: Kustomize (Recomendado)

```bash
# Aplicar tudo de uma vez
kubectl apply -k k8s/

# Verificar o que será aplicado antes
kubectl kustomize k8s/
```

---

## ✅ Passo 3: Verificação

```bash
# 1. Verificar namespace
kubectl get namespace mdb-health

# 2. Verificar pods
kubectl get pods -n mdb-health
# Deve mostrar: postgres-0, fastapi-xxx, fastapi-yyy, fastapi-zzz

# 3. Verificar services
kubectl get svc -n mdb-health

# 4. Verificar ingress
kubectl get ingress -n mdb-health

# 5. Verificar HPA
kubectl get hpa -n mdb-health

# 6. Logs dos pods
kubectl logs -n mdb-health -l app=fastapi --tail=50 -f

# 7. Descrever pod (troubleshooting)
kubectl describe pod -n mdb-health <pod-name>

# 8. Exec no pod (debug)
kubectl exec -it -n mdb-health <pod-name> -- /bin/bash
```

---

## 🧪 Passo 4: Testar a API

### Port-Forward (Desenvolvimento)

```bash
# Port-forward do service
kubectl port-forward -n mdb-health svc/fastapi-service 8080:80

# Testar
curl -H "Authorization: Bearer troque-essa-chave" http://localhost:8080/health
```

### Via Ingress (Produção)

```bash
# Obter IP externo do Ingress
kubectl get ingress -n mdb-health

# Testar (substitua pelo seu domínio ou IP)
curl -H "Authorization: Bearer troque-essa-chave" https://api.mdb-health.example.com/health

# Testar POST
curl -X POST https://api.mdb-health.example.com/fhir/Patient \
  -H "Authorization: Bearer troque-essa-chave" \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "Patient",
    "name": [{"family": "Silva", "given": ["João"]}],
    "gender": "male"
  }'
```

---

## 📊 Passo 5: Teste de Carga no Kubernetes

```bash
# 1. Deploy de pod de teste
kubectl run load-test -n mdb-health --image=python:3.12-slim --rm -it -- bash

# Dentro do pod:
pip install requests faker
python3 << 'EOF'
import requests
import concurrent.futures
import time

BASE_URL = "http://fastapi-service.mdb-health.svc.cluster.local"
TOKEN = "troque-essa-chave"

def make_request():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}/health", headers=headers)
    return response.status_code

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    start = time.time()
    futures = [executor.submit(make_request) for _ in range(1000)]
    results = [f.result() for f in futures]
    end = time.time()

print(f"Total: {len(results)} requests")
print(f"Success: {results.count(200)}")
print(f"Time: {end - start:.2f}s")
print(f"RPS: {len(results) / (end - start):.2f}")
EOF
```

### Observar Auto-scaling

```bash
# Monitorar HPA em tempo real
watch kubectl get hpa -n mdb-health

# Monitorar pods
watch kubectl get pods -n mdb-health

# Ver eventos
kubectl get events -n mdb-health --sort-by='.lastTimestamp'
```

---

## 📈 Monitoramento e Observabilidade

### 1. Instalar Metrics Server (necessário para HPA)

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verificar
kubectl top nodes
kubectl top pods -n mdb-health
```

### 2. Prometheus + Grafana (Recomendado)

```bash
# Usando Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# Acessar Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# User: admin, Password: prom-operator
```

### 3. Dashboards importantes

- **Kubernetes Cluster Monitoring**: ID 7249
- **PostgreSQL**: ID 9628
- **NGINX Ingress**: ID 9614
- **FastAPI**: Criar custom ou usar ID 7039 (Python)

---

## 🔒 Segurança

### 1. Usar Secrets External (Produção)

```bash
# AWS Secrets Manager + External Secrets Operator
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  -n external-secrets-system \
  --create-namespace

# Azure Key Vault, GCP Secret Manager similar
```

### 2. Network Policies

```bash
# Já incluído em network-policy.yaml
kubectl apply -f k8s/network-policy.yaml
```

### 3. Pod Security Standards

```yaml
# Adicionar ao namespace
apiVersion: v1
kind: Namespace
metadata:
  name: mdb-health
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions (Exemplo)

```yaml
# .github/workflows/deploy-k8s.yml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: |
          docker build -t ${{ secrets.REGISTRY }}/mdb-health-fastapi:${{ github.sha }} ./fastapi

      - name: Push to registry
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USER }} --password-stdin
          docker push ${{ secrets.REGISTRY }}/mdb-health-fastapi:${{ github.sha }}

      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v1
        with:
          manifests: |
            k8s/fastapi-deployment.yaml
          images: |
            ${{ secrets.REGISTRY }}/mdb-health-fastapi:${{ github.sha }}
          namespace: mdb-health
```

---

## 💰 Estimativa de Custos (Managed Kubernetes)

### AWS EKS

```
EKS Control Plane:              $72/mês
3× t3.medium nodes (8h/day):   $45/mês
RDS db.t3.medium:              $110/mês
Load Balancer:                  $20/mês
──────────────────────────────────────
Total:                         $247/mês
Capacidade: ~300 usuários simultâneos
```

### Google GKE

```
GKE Control Plane:              $0 (grátis)
3× n1-standard-2 nodes:         $90/mês
Cloud SQL db-n1-standard-2:    $120/mês
Load Balancer:                  $20/mês
──────────────────────────────────────
Total:                         $230/mês
Capacidade: ~300 usuários simultâneos
```

### Azure AKS

```
AKS Control Plane:              $0 (grátis)
3× Standard_DS2_v2 nodes:       $95/mês
Azure Database PostgreSQL:     $130/mês
Load Balancer:                  $20/mês
──────────────────────────────────────
Total:                         $245/mês
Capacidade: ~300 usuários simultâneos
```

---

## 🎯 Capacidade e Performance

### Configuração Atual (3 pods)

| Métrica              | Valor                 |
| -------------------- | --------------------- |
| Pods mínimos         | 3                     |
| Pods máximos         | 10                    |
| Usuários/pod         | ~100                  |
| **Capacidade total** | **300-1000 usuários** |
| RPS estimado         | 220-730               |
| Latência P95         | < 20ms                |
| Auto-scale trigger   | CPU > 70%             |

### Escalabilidade

```
3 pods:    300 users, ~220 RPS
5 pods:    500 users, ~360 RPS
10 pods:  1000 users, ~730 RPS
```

---

## 🔧 Troubleshooting

### Pods não iniciam

```bash
# Ver eventos
kubectl describe pod -n mdb-health <pod-name>

# Ver logs
kubectl logs -n mdb-health <pod-name>

# Verificar recursos
kubectl top pods -n mdb-health
```

### HPA não escala

```bash
# Verificar metrics-server
kubectl get apiservice v1beta1.metrics.k8s.io

# Ver métricas
kubectl top pods -n mdb-health

# Debug HPA
kubectl describe hpa -n mdb-health fastapi-hpa
```

### Ingress não funciona

```bash
# Verificar Ingress Controller
kubectl get pods -n ingress-nginx

# Ver logs do Ingress
kubectl logs -n ingress-nginx <ingress-controller-pod>

# Testar service diretamente
kubectl port-forward -n mdb-health svc/fastapi-service 8080:80
```

---

## 📚 Próximos Passos

1. **Implementar Observabilidade Completa**

   - Prometheus + Grafana
   - Alertas (PagerDuty, Slack)
   - Distributed tracing (Jaeger)

2. **Otimizar Performance**

   - Redis para cache
   - Connection pooling
   - Read replicas PostgreSQL

3. **Melhorar Segurança**

   - External Secrets Operator
   - Service Mesh (Istio/Linkerd)
   - mTLS entre serviços

4. **Disaster Recovery**
   - Backups automáticos (Velero)
   - Multi-region deployment
   - Chaos engineering (Chaos Mesh)

---

## 📖 Comandos Úteis

```bash
# Escalar manualmente
kubectl scale deployment fastapi -n mdb-health --replicas=5

# Atualizar imagem (rolling update)
kubectl set image deployment/fastapi fastapi=mdb-health-fastapi:v2.0.0 -n mdb-health

# Rollback
kubectl rollout undo deployment/fastapi -n mdb-health

# Ver histórico de deployments
kubectl rollout history deployment/fastapi -n mdb-health

# Deletar tudo
kubectl delete namespace mdb-health

# Reiniciar deployment
kubectl rollout restart deployment/fastapi -n mdb-health
```

---

**Pronto para produção!** 🚀

Este guia cobre todos os aspectos necessários para deploy profissional no Kubernetes.
