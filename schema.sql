-- ================================================
-- SCHEMA DO BANCO DE DADOS - SISTEMA DE MOTOBOYS
-- ================================================
-- Execute este script no SQL Editor do Supabase
-- para criar as tabelas necessárias
-- ================================================

-- Tabela de Registros de Entregas
CREATE TABLE IF NOT EXISTS registros (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    data DATE NOT NULL,
    periodo VARCHAR(50) NOT NULL CHECK (periodo IN ('Manhã', 'Noite')),
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('Fixo', 'Freelancer')),
    entregas INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_registros_data ON registros(data);
CREATE INDEX IF NOT EXISTS idx_registros_nome ON registros(nome);
CREATE INDEX IF NOT EXISTS idx_registros_tipo ON registros(tipo);
CREATE INDEX IF NOT EXISTS idx_registros_created_at ON registros(created_at DESC);

-- Tabela de Configurações
CREATE TABLE IF NOT EXISTS configuracoes (
    id BIGSERIAL PRIMARY KEY,
    valor_diaria DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    valor_corrida DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    ativa BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para buscar configuração ativa
CREATE INDEX IF NOT EXISTS idx_configuracoes_ativa ON configuracoes(ativa, created_at DESC);

-- Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_registros_updated_at
    BEFORE UPDATE ON registros
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Inserir configuração padrão (caso não exista)
INSERT INTO configuracoes (valor_diaria, valor_corrida, ativa, created_at)
SELECT 150.00, 5.00, TRUE, NOW()
WHERE NOT EXISTS (SELECT 1 FROM configuracoes WHERE ativa = TRUE);

-- Comentários das tabelas
COMMENT ON TABLE registros IS 'Registros diários de entregas dos motoboys';
COMMENT ON TABLE configuracoes IS 'Configurações de valores (diária e corrida)';

COMMENT ON COLUMN registros.nome IS 'Nome do motoboy';
COMMENT ON COLUMN registros.data IS 'Data do registro';
COMMENT ON COLUMN registros.periodo IS 'Período do dia (Manhã ou Noite)';
COMMENT ON COLUMN registros.tipo IS 'Tipo de motoboy (Fixo ou Freelancer)';
COMMENT ON COLUMN registros.entregas IS 'Número de entregas realizadas';

COMMENT ON COLUMN configuracoes.valor_diaria IS 'Valor da diária em reais';
COMMENT ON COLUMN configuracoes.valor_corrida IS 'Valor por corrida em reais';
COMMENT ON COLUMN configuracoes.ativa IS 'Indica se é a configuração ativa';

-- ================================================
-- VERIFICAÇÃO DAS TABELAS CRIADAS
-- ================================================
-- Execute as queries abaixo para verificar se tudo foi criado corretamente

-- Verificar estrutura da tabela registros
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'registros'
ORDER BY ordinal_position;

-- Verificar estrutura da tabela configuracoes
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'configuracoes'
ORDER BY ordinal_position;

-- Verificar índices criados
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename IN ('registros', 'configuracoes')
ORDER BY tablename, indexname;

-- Verificar se há configuração ativa
SELECT * FROM configuracoes WHERE ativa = TRUE;

-- ================================================
-- QUERIES ÚTEIS PARA MANUTENÇÃO
-- ================================================

-- Ver todos os registros de hoje
SELECT * FROM registros
WHERE data = CURRENT_DATE
ORDER BY created_at DESC;

-- Ver total de entregas por motoboy (semana atual)
SELECT
    nome,
    tipo,
    COUNT(DISTINCT data) as dias_trabalhados,
    SUM(entregas) as total_entregas
FROM registros
WHERE data >= date_trunc('week', CURRENT_DATE)
GROUP BY nome, tipo
ORDER BY total_entregas DESC;

-- Ver histórico de configurações
SELECT
    id,
    valor_diaria,
    valor_corrida,
    ativa,
    created_at
FROM configuracoes
ORDER BY created_at DESC;

-- Backup dos registros (caso necessário)
-- SELECT * FROM registros ORDER BY created_at;

-- Limpar registros antigos (CUIDADO!)
-- DELETE FROM registros WHERE data < '2025-01-01';

-- ================================================
-- POLÍTICA DE RLS (Row Level Security)
-- ================================================
-- O sistema atual funciona com RLS DESABILITADO
-- Caso queira habilitar RLS no futuro, use:

-- ALTER TABLE registros ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE configuracoes ENABLE ROW LEVEL SECURITY;

-- CREATE POLICY "Permitir todas as operações" ON registros
--     FOR ALL USING (true) WITH CHECK (true);

-- CREATE POLICY "Permitir todas as operações" ON configuracoes
--     FOR ALL USING (true) WITH CHECK (true);
