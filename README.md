# 🏍️ Sistema de Controle de Motoboys

Sistema completo de gestão de entregas e motoboys desenvolvido com **Streamlit**, **Supabase** e **Google Gemini AI**.

## 📋 Funcionalidades

### Aba OPERACIONAL
- ✅ Formulário de registro com autocomplete de motoboys
- 📅 Listagem de registros do dia
- ✏️ Edição e exclusão de registros
- 🔄 Atualização em tempo real

### Aba GERENCIAL
- ⚙️ **Seção A - Configurações**: Gerenciamento de valores (Diária e Corrida)
- 📊 **Seção B - KPIs do Dia**: Métricas em tempo real
  - Total de Entregas
  - Total de Motoboys
  - Média Entregas/Motoboy
  - Custo Total
  - Custo Médio por Entrega
- 📈 **Seção C - Relatório Semanal**: Consolidação segunda-feira até hoje
  - Tabela com dados por motoboy
  - Gráficos interativos
  - Cálculo automático de valores devidos
- 🤖 **Seção D - Assistente de IA**: Chatbot com Gemini 2.5 Flash
  - Análises inteligentes
  - Sugestões de otimização
  - Perguntas pré-configuradas

## 🚀 Instalação

### 1. Pré-requisitos
- Python 3.8 ou superior
- Conta no Supabase
- API Key do Google Gemini

### 2. Clone ou baixe o projeto

```bash
cd "C:\Users\rafae\OneDrive\Desktop\Lab. de testes\Motoboys.26"
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Supabase

#### Criar tabelas no Supabase

Execute o script SQL fornecido no arquivo `schema.sql` no SQL Editor do Supabase:

1. Acesse seu projeto no [Supabase](https://app.supabase.com)
2. Vá em **SQL Editor**
3. Copie e execute o conteúdo de `schema.sql`

#### Desabilitar RLS (Row Level Security)

Como você já desabilitou o RLS, não é necessário fazer nada. Caso precise reabilitar:

1. Vá em **Authentication** > **Policies**
2. Desabilite RLS para as tabelas `registros` e `configuracoes`

### 5. Configure as credenciais

Edite o arquivo `.streamlit/secrets.toml` com suas credenciais:

```toml
[supabase]
url = "https://sttpygyknnuqrdfuzfph.supabase.co"
key = "SUA_SUPABASE_KEY_AQUI"

[google]
api_key = "SUA_GOOGLE_API_KEY_AQUI"
```

**Como obter as chaves:**

#### Supabase Key:
1. Acesse [Supabase](https://app.supabase.com)
2. Selecione seu projeto
3. Vá em **Settings** > **API**
4. Copie a chave `anon` ou `service_role`

#### Google Gemini API Key:
1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Clique em **Get API Key**
3. Crie ou selecione um projeto
4. Copie a API Key gerada

### 6. Execute a aplicação

```bash
streamlit run app-motoboys.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
Motoboys.26/
├── .streamlit/
│   └── secrets.toml          # Credenciais (NÃO versionar!)
├── app-motoboys.py           # Interface principal Streamlit
├── database.py               # Conexão e queries Supabase
├── ai_assistant.py           # Integração com Gemini AI
├── utils.py                  # Funções de formatação e cálculos
├── requirements.txt          # Dependências Python
├── schema.sql                # Script de criação das tabelas
└── README.md                 # Este arquivo
```

## 💰 Regras de Negócio

### Tipos de Motoboy
- **Fixo**: Recebe diária + valor por corrida (pago no final da semana)
- **Freelancer**: Pago no dia (não aparece em valores devidos)

### Cálculos
- **Custo Total**: `(Qtd Motoboys × Diária) + (Total Entregas × Valor Corrida)`
- **Custo Médio/Entrega**: `Custo Total ÷ Total Entregas`
- **Média Entregas/Moto**: `Total Entregas ÷ Qtd Motoboys`

### Relatório Semanal
- Período: Segunda-feira até hoje
- Consolidação por motoboy
- Valores devidos calculados automaticamente
- Apenas motoboys **Fixos** têm valores a receber

## 🎯 Como Usar

### Registrar uma Entrega
1. Vá para a aba **OPERACIONAL**
2. Preencha o formulário:
   - Selecione ou digite o nome do motoboy
   - Escolha a data (padrão: hoje)
   - Selecione o período (Manhã/Noite)
   - Escolha o tipo (Fixo/Freelancer)
   - Informe o número de entregas
3. Clique em **Registrar**

### Editar/Excluir Registro
1. Na lista de registros do dia, clique:
   - ✏️ para editar
   - 🗑️ para excluir

### Configurar Valores
1. Vá para a aba **GERENCIAL**
2. Expanda **Gerenciar Valores**
3. Digite os valores no formato brasileiro (ex: 150,50)
4. Clique em **Salvar Configurações**

### Usar o Assistente de IA
1. Na aba **GERENCIAL**, role até **Assistente de IA**
2. Use as perguntas sugeridas ou digite sua própria pergunta
3. O assistente analisará os dados reais do sistema

## 🔧 Tecnologias Utilizadas

- **Frontend**: Streamlit 1.31.0
- **Banco de Dados**: Supabase (PostgreSQL)
- **IA**: Google Gemini 2.5 Flash
- **Visualizações**: Plotly 5.18.0
- **Manipulação de Dados**: Pandas 2.1.4

## ⚠️ Observações Importantes

1. **Nunca versione** o arquivo `.streamlit/secrets.toml` (contém credenciais)
2. Certifique-se de que as tabelas foram criadas corretamente no Supabase
3. Verifique se o RLS está desabilitado nas tabelas
4. Use o formato brasileiro para valores monetários: R$ 1.234,56

## 🐛 Solução de Problemas

### Erro ao conectar com Supabase
- Verifique se a URL e Key estão corretas no `secrets.toml`
- Confirme se as tabelas foram criadas
- Verifique se o RLS está desabilitado

### Erro ao conectar com Gemini
- Confirme se a API Key está correta
- Verifique se você tem créditos/quota disponível na API

### Erro de formatação de moeda
- Use sempre o formato brasileiro: `150,50` (não `150.50`)
- O sistema converte automaticamente

## 📞 Suporte

Para questões sobre:
- **Supabase**: [Documentação Supabase](https://supabase.com/docs)
- **Streamlit**: [Documentação Streamlit](https://docs.streamlit.io)
- **Google Gemini**: [Documentação Gemini API](https://ai.google.dev/docs)

---

Desenvolvido com ❤️ usando Streamlit + Supabase + Gemini AI
