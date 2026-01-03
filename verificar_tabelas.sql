-- Verificar se as tabelas foram criadas
SELECT 
    table_name,
    table_type
FROM information_schema.tables
WHERE table_name IN ('registros', 'configuracoes')
ORDER BY table_name;

-- Ver estrutura da tabela registros
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'registros'
ORDER BY ordinal_position;

-- Ver estrutura da tabela configuracoes
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'configuracoes'
ORDER BY ordinal_position;

-- Ver configuração padrão inserida
SELECT * FROM configuracoes;

-- Ver se RLS está desabilitado
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE tablename IN ('registros', 'configuracoes');
