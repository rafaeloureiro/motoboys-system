# 🚀 Início Rápido - Resolver Erro "ModuleNotFoundError"

## ⚠️ Erro Comum no Streamlit Cloud

Se você está vendo este erro:
```
ModuleNotFoundError: This app has encountered an error...
File "/mount/src/python/app-motoboys.py", line 16, in <module>
    import database as db
```

**Causa:** Secrets não configurados no Streamlit Cloud.

## 🔧 Solução em 3 Passos

### Passo 1: Acessar Configurações

No Streamlit Cloud, clique em:
- **⚙️ Manage app** (canto inferior direito)
- **⚙️ Settings**
- **🔐 Secrets**

### Passo 2: Adicionar Secrets

Cole o seguinte conteúdo no editor de secrets:

```toml
[supabase]
url = "https://sttpygyknnuqrdfuzfph.supabase.co"
key = "SUA_SUPABASE_ANON_KEY_AQUI"

[google]
api_key = "SUA_GOOGLE_GEMINI_API_KEY_AQUI"
```

### Passo 3: Salvar e Reiniciar

1. Clique em **Save**
2. O app será reiniciado automaticamente
3. Aguarde alguns segundos

## 🔑 Como Obter as Chaves

### Supabase Key

1. Acesse [app.supabase.com](https://app.supabase.com)
2. Selecione seu projeto
3. Vá em **Settings** > **API**
4. Copie a chave **`anon public`**

**Exemplo:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Google Gemini API Key

1. Acesse [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Clique em **Get API Key**
3. Selecione ou crie um projeto
4. Copie a API Key

**Exemplo:**
```
AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
```

## ✅ Verificar se Funcionou

Após configurar os secrets:

1. O app deve reiniciar automaticamente
2. Você deve ver a página principal do sistema
3. Se ainda houver erro, verifique se:
   - As chaves estão corretas (sem espaços extras)
   - O formato TOML está correto
   - As tabelas foram criadas no Supabase

## 🗄️ Criar Tabelas no Supabase

Se ainda não criou as tabelas:

1. Acesse [app.supabase.com](https://app.supabase.com)
2. Vá em **SQL Editor**
3. Copie o conteúdo do arquivo `schema.sql`
4. Cole e execute
5. Verifique se as tabelas `registros` e `configuracoes` foram criadas

## 🆘 Ainda com Problemas?

### Erro: "Supabase connection failed"
- ✅ Verifique se a URL do Supabase está correta
- ✅ Confirme que a API key é válida
- ✅ Certifique-se de que o RLS está desabilitado

### Erro: "Gemini API error"
- ✅ Verifique se a API key do Google está correta
- ✅ Confirme se você tem quota disponível
- ✅ Tente gerar uma nova API key

### Erro persiste
- 📧 Verifique os logs no Streamlit Cloud (**Manage app** > **Logs**)
- 🔄 Tente fazer **Reboot app**
- 📝 Verifique se todos os arquivos estão no repositório

## 📚 Documentação Completa

Para instruções detalhadas, consulte:
- `README.md` - Documentação geral
- `DEPLOY.md` - Guia completo de deploy
- `schema.sql` - Script SQL das tabelas

---

**Dica:** Salve as chaves em um local seguro para referência futura! 🔐
