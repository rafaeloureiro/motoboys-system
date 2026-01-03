# 🚀 Guia de Deploy - Streamlit Cloud 2026

Este guia mostra como fazer deploy do Sistema de Controle de Motoboys no Streamlit Cloud.

## ✅ Pré-requisitos

- [ ] Conta no [GitHub](https://github.com)
- [ ] Conta no [Streamlit Cloud](https://streamlit.io/cloud)
- [ ] Projeto Supabase configurado (tabelas criadas)
- [ ] API Key do Google Gemini

## 📦 Preparação do Código

### 1. Criar repositório no GitHub

```bash
cd "C:\Users\rafae\OneDrive\Desktop\Lab. de testes\Motoboys.26"

# Inicializar Git
git init

# Adicionar arquivos
git add .

# Primeiro commit
git commit -m "Initial commit - Sistema de Motoboys v2026"

# Adicionar remote (substitua com seu repositório)
git remote add origin https://github.com/SEU_USUARIO/motoboys-sistema.git

# Push para GitHub
git branch -M main
git push -u origin main
```

### 2. Verificar arquivos essenciais

Certifique-se de que estes arquivos estão no repositório:

- ✅ `app-motoboys.py` (arquivo principal)
- ✅ `requirements.txt` (dependências)
- ✅ `database.py` (conexão Supabase)
- ✅ `ai_assistant.py` (integração Gemini)
- ✅ `utils.py` (funções auxiliares)
- ✅ `.streamlit/config.toml` (configurações)
- ✅ `.gitignore` (proteção de secrets)

⚠️ **IMPORTANTE:** O arquivo `.streamlit/secrets.toml` NÃO deve estar no repositório!

## 🌐 Deploy no Streamlit Cloud

### Passo 1: Acessar Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em **"New app"**

### Passo 2: Configurar App

Preencha os campos:

```
Repository: SEU_USUARIO/motoboys-sistema
Branch: main
Main file path: app-motoboys.py
App URL (opcional): motoboys-sistema
```

### Passo 3: Adicionar Secrets

Antes de fazer deploy, clique em **"Advanced settings"** > **"Secrets"**

Cole o seguinte conteúdo (substitua com suas chaves reais):

```toml
[supabase]
url = "https://sttpygyknnuqrdfuzfph.supabase.co"
key = "SUA_SUPABASE_KEY_AQUI"

[google]
api_key = "SUA_GOOGLE_API_KEY_AQUI"
```

### Passo 4: Deploy

1. Clique em **"Deploy!"**
2. Aguarde alguns minutos para o build completar
3. Seu app estará disponível em `https://SEU_APP.streamlit.app`

## 🔧 Configuração do Banco de Dados

### Supabase - Verificações Finais

1. **Acesse seu projeto no Supabase:**
   - [https://app.supabase.com](https://app.supabase.com)

2. **Verifique se as tabelas existem:**
   - Vá em **Database** > **Tables**
   - Confirme que `registros` e `configuracoes` estão criadas

3. **Verifique RLS (Row Level Security):**
   - Para cada tabela, vá em **Authentication** > **Policies**
   - Certifique-se de que RLS está **desabilitado** ou com políticas corretas

4. **Teste a conexão:**
   - Execute uma query simples no SQL Editor:
   ```sql
   SELECT COUNT(*) FROM registros;
   SELECT * FROM configuracoes WHERE ativa = true;
   ```

## 🔑 Obter API Keys

### Google Gemini API Key

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Clique em **"Get API Key"**
3. Selecione ou crie um projeto
4. Copie a API Key gerada
5. Cole no campo `api_key` dos secrets do Streamlit Cloud

### Supabase Keys

1. Acesse [Supabase Dashboard](https://app.supabase.com)
2. Selecione seu projeto
3. Vá em **Settings** > **API**
4. Copie:
   - **URL**: Project URL
   - **Key**: `anon` (public) ou `service_role` (privada)
5. Cole nos campos `url` e `key` dos secrets

## 🔄 Atualizar App Depois do Deploy

Sempre que fizer mudanças no código:

```bash
# Commit suas mudanças
git add .
git commit -m "Descrição da mudança"

# Push para GitHub
git push origin main
```

O Streamlit Cloud detectará automaticamente e fará redeploy!

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"

**Causa:** Falta dependência no `requirements.txt`

**Solução:**
1. Adicione a dependência em `requirements.txt`
2. Faça commit e push
3. O app será redeployado automaticamente

### Erro: "Failed to connect to Supabase"

**Causa:** Secrets não configurados ou incorretos

**Solução:**
1. Vá em **App Settings** > **Secrets** no Streamlit Cloud
2. Verifique se as chaves estão corretas
3. Clique em **"Save"** e **"Reboot app"**

### Erro: "Gemini API Error"

**Causa:** API Key inválida ou sem quota

**Solução:**
1. Verifique se a API Key está correta
2. Confirme se há quota disponível no Google AI Studio
3. Tente gerar uma nova API Key

### App está lento

**Solução:**
1. Verifique se os decoradores `@st.cache_resource` e `@st.cache_data` estão aplicados
2. Considere otimizar queries do banco de dados
3. Verifique o plano do Streamlit Cloud (limite de recursos)

## 📊 Monitoramento

### Ver Logs do App

1. Acesse seu app no Streamlit Cloud
2. Clique em **"Manage app"** (ícone ⚙️)
3. Vá em **"Logs"** para ver erros em tempo real

### Métricas de Uso

1. No Streamlit Cloud, vá em **Analytics**
2. Monitore:
   - Número de visitantes
   - Tempo de resposta
   - Uso de recursos

## 🔐 Segurança

### Boas Práticas

1. ✅ **Nunca** faça commit de `secrets.toml`
2. ✅ Use a chave `anon` do Supabase (não `service_role`) para produção
3. ✅ Configure políticas RLS no Supabase para acesso controlado
4. ✅ Monitore uso da API do Gemini para evitar custos excessivos
5. ✅ Use HTTPS (Streamlit Cloud já fornece)

### Rotação de Chaves

Periodicamente, atualize suas chaves:

1. Gere novas chaves no Supabase e Google
2. Atualize os secrets no Streamlit Cloud
3. Clique em **"Reboot app"**
4. Revogue as chaves antigas

## 📱 Compartilhamento

### Link Público

Seu app estará disponível em:
```
https://SEU_APP.streamlit.app
```

### Domínio Customizado (Plano Pago)

Se tiver plano pago, pode configurar domínio customizado:
1. Vá em **Settings** > **General**
2. Configure seu domínio
3. Adicione registros DNS conforme instruções

## 🎯 Checklist Final

Antes de compartilhar o app, verifique:

- [ ] App está online e funcionando
- [ ] Formulário de registro funciona
- [ ] Registros aparecem corretamente
- [ ] KPIs são calculados
- [ ] Relatório semanal exibe dados
- [ ] Assistente de IA responde (Gemini)
- [ ] Valores em R$ estão formatados corretamente
- [ ] Gráficos aparecem sem erros
- [ ] Não há mensagens de erro nos logs

## 📞 Suporte

- **Streamlit Cloud:** [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- **Supabase:** [supabase.com/docs](https://supabase.com/docs)
- **Google Gemini:** [ai.google.dev/docs](https://ai.google.dev/docs)

---

🎉 **Parabéns!** Seu sistema está no ar e pronto para uso!
