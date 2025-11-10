# Nginx — instruções de deploy para mdb-health

Esses arquivos são um template para você copiar no servidor e habilitar o Nginx como reverse-proxy
para as aplicações do projeto (FastAPI e Superset). Eles assumem que você está executando o
docker-compose localmente no servidor e que os serviços expõem portas no host (como mapeado no
`docker-compose.yml`).

Arquivos criados:

- `nginx/sites-available/mdb-health.conf` — configuração do site (edite domínios e portas).
- `nginx/nginx.conf` — exemplo de `nginx.conf` geral (opcional; distribuições já possuem o seu).

Passo-a-passo rápido

1. No servidor, instale o nginx se necessário:

```bash
sudo apt update
sudo apt install -y nginx
```

2. No arquivo `nginx/sites-available/mdb-health.conf`, substitua:

   - `api.example.com` pelo seu domínio da API (ex: `api.meudominio.com`);
   - `superset.example.com` pelo domínio do Superset;
   - as portas `127.0.0.1:8000` e `127.0.0.1:8088` pelos valores mapeados no seu `docker-compose` (variáveis FASTAPI_PORT e SUPERSET_PORT).

3. Copie o arquivo para o servidor (exemplo usando scp):

```bash
# do seu workstation
scp nginx/sites-available/mdb-health.conf usuario@meu-servidor:/tmp/

# no servidor
sudo mv /tmp/mdb-health.conf /etc/nginx/sites-available/mdb-health.conf
sudo ln -s /etc/nginx/sites-available/mdb-health.conf /etc/nginx/sites-enabled/mdb-health.conf
```

4. Crie a pasta para validar certificados (usada no conf):

```bash
sudo mkdir -p /var/www/html
sudo chown www-data:www-data /var/www/html
```

5. Teste e recarregue o nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

6. (Recomendado) Obtenha certificados Let’s Encrypt com certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.seudominio -d superset.seudominio
```

Notas de segurança e recomendações

- Não exponha o Postgres via nginx/HTTP — mantenha o Postgres na rede Docker e acessível somente pelas aplicações.
- Considere usar cabeçalhos de segurança adicionais e HSTS em produção.
- Se preferir usar path-based routing (ex: `example.com/api`), posso gerar a variante.

Se quiser, eu já gero a variante por path em vez de subdomínios, ou adapto o arquivo para incluir TLS direto (ex: configuração `server` para `listen 443` com certificados). Diga qual domínio(s) e portas você usa que eu ajusto o template.

## Uso com Docker (proxy automático)

Este repositório já inclui no `docker-compose.yml` um par de serviços que permitem ao Nginx
se configurar automaticamente com base em variáveis de ambiente dos containers:

- `nginx-proxy` (imagem `jwilder/nginx-proxy`) — observa o Docker socket e gera blocos de server
  para cada container que exporta `VIRTUAL_HOST`.
- `letsencrypt` (imagem `nginxproxy/acme-companion`) — obtém/renova certificados Let's Encrypt
  para os hosts configurados via `LETSENCRYPT_HOST` / `LETSENCRYPT_EMAIL`.

Como usar

1. No arquivo `.env` (ou no ambiente), defina as portas e segredos usados no `docker-compose.yml` (exemplo):

```
FASTAPI_PORT=8000
SUPERSET_PORT=8088
SUPERSET_ADMIN_USERNAME=admin
SUPERSET_ADMIN_PASSWORD=secret
SUPERSET_ADMIN_EMAIL=me@damatlas.cloud
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

2. Substitua os placeholders de e-mail (`you@example.com`) no `docker-compose.yml` pelas suas informações.

3. Cada serviço que deverá ficar disponível via subdomínio já vem com as variáveis para o proxy.

   - FastAPI: `api.damatlas.cloud` (env VIRTUAL_HOST/LETSENCRYPT_HOST)
   - Superset: `superset.damatlas.cloud` (env VIRTUAL_HOST/LETSENCRYPT_HOST)

4. Suba o compose no servidor (exemplo):

```bash
docker compose up -d
```

5. O `nginx-proxy` cria os blocos e o `letsencrypt` provisiona certificados. Verifique logs se algo falhar:

```bash
docker compose logs -f nginx-proxy
docker compose logs -f nginx-letsencrypt
```

Observações importantes

- Substitua os `you@example.com` pelos e-mails corretos para as notificações do Let's Encrypt.
- Se você já tem um nginx rodando no host (fora do Docker) ele pode conflitar com as portas 80/443 do `nginx-proxy`. Pare-o antes de subir o compose ou ajuste as portas.
- Em ambientes com firewall, abra as portas 80 e 443.
