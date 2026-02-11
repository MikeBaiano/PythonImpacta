# 📚 Sistema de Notas de Alunos com Supabase

Sistema de gerenciamento de alunos com persistência de dados usando Supabase.

## 🚀 Instalação

### 1. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 2. Configurar o Supabase

#### 2.1. Criar a tabela no Supabase

1. Acesse seu projeto no [Supabase](https://supabase.com)
2. Vá em **SQL Editor**
3. Execute o seguinte SQL:

```sql
-- Criar a tabela de alunos
CREATE TABLE IF NOT EXISTS alunos (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    nota1 DECIMAL(4,2) NOT NULL,
    nota2 DECIMAL(4,2) NOT NULL,
    nota3 DECIMAL(4,2) NOT NULL,
    media DECIMAL(4,2) NOT NULL,
    situacao TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar Row Level Security (RLS)
ALTER TABLE alunos ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas operações (apenas para desenvolvimento)
CREATE POLICY "Permitir tudo para todos" ON alunos
    FOR ALL USING (true);
```

#### 2.2. Configurar as credenciais

1. No Supabase, vá em **Settings > API**
2. Copie a **URL** e a **anon public key**
3. Edite o arquivo `.env` e cole suas credenciais:

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## ▶️ Como Usar

Execute o programa:

```bash
python escola.py
```

### Funcionalidades

1. **Adicionar Aluno** - Cadastra novo aluno com 3 notas
2. **Listar Alunos** - Mostra todos os alunos cadastrados
3. **Buscar Aluno** - Busca aluno por nome
4. **Atualizar Notas** - Atualiza as notas de um aluno
5. **Excluir Aluno** - Remove um aluno do banco
6. **Estatísticas** - Mostra estatísticas da turma

### Regras de Avaliação

- **Aprovado**: Média ≥ 7.0
- **Recuperação**: 5.0 ≤ Média < 7.0
- **Reprovado**: Média < 5.0

## 📁 Arquivos do Projeto

- `escola.py` - Sistema principal com integração ao Supabase
- `study.py` - Sistema básico sem banco de dados
- `main.py` - Exemplos de algoritmos matemáticos
- `.env` - Credenciais do Supabase (não commitar!)
- `requirements.txt` - Dependências do projeto

## 🔒 Segurança

⚠️ **IMPORTANTE**: O arquivo `.env` contém suas credenciais secretas!

- Nunca commite o arquivo `.env` no Git
- O arquivo `.gitignore` já está configurado para proteger suas credenciais
- Use apenas em ambiente de desenvolvimento/estudo

## 💡 Diferenças entre os arquivos

### `study.py`

- Sistema básico sem banco de dados
- Dados perdidos ao fechar o programa
- Bom para aprender conceitos de Python

### `escola.py`

- Sistema completo com banco de dados Supabase
- Dados persistentes (não são perdidos)
- CRUD completo (Create, Read, Update, Delete)
- Bom para aprender integração com banco de dados

## 🎓 Conceitos de Programação

Este projeto ensina:

- ✅ Funções e organização de código
- ✅ Estruturas de dados (listas, dicionários)
- ✅ Integração com APIs REST
- ✅ Variáveis de ambiente
- ✅ CRUD com banco de dados
- ✅ Validação de dados
- ✅ Tratamento de erros
- ✅ Boas práticas de segurança

## 📊 Estrutura da Tabela

| Coluna     | Tipo      | Descrição                      |
| ---------- | --------- | ------------------------------ |
| id         | BIGSERIAL | ID único do aluno              |
| nome       | TEXT      | Nome do aluno                  |
| nota1      | DECIMAL   | Primeira nota                  |
| nota2      | DECIMAL   | Segunda nota                   |
| nota3      | DECIMAL   | Terceira nota                  |
| media      | DECIMAL   | Média calculada                |
| situacao   | TEXT      | Aprovado/Recuperação/Reprovado |
| created_at | TIMESTAMP | Data de cadastro               |

## 🐛 Solução de Problemas

### Erro: "Configure suas credenciais do Supabase"

- Verifique se editou o arquivo `.env` com suas credenciais reais

### Erro de conexão

- Verifique se copiou a URL e KEY corretas do Supabase
- Confirme que tem acesso à internet

### Erro ao inserir dados

- Verifique se criou a tabela no SQL Editor do Supabase
- Confirme que habilitou a política de RLS

---

Desenvolvido para estudos de Python e banco de dados 🐍
