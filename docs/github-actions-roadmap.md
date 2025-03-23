# Roadmap de Estudo: GitHub Actions

> Baseado no projeto Lilica Automator

## Conceitos Já Aplicados 🎯

### 1. Estrutura Básica do Workflow

- Triggers configurados:
  - push (branch: main)
  - pull_request
  - workflow_dispatch
- Jobs múltiplos:
  - build-windows
  - build-linux
  - create-release
- Dependências entre jobs usando `needs`
- Condicionais com `if` statements

### 2. Gerenciamento de Ambientes

- Runners em diferentes sistemas:
  - windows-latest
  - ubuntu-latest
- Setup de ambiente Python:
  - actions/setup-python@v5
  - python-version: "3.10"
- Instalação de dependências:
  - Sistema (apt-get no Linux)
  - Python (pip, requirements.txt)
  - PyInstaller para builds

### 3. Artifacts e Assets

- Upload de artifacts com actions/upload-artifact@v4
- Download de artifacts para release
- Criação de releases automáticas
- Upload de assets específicos por plataforma
- Versionamento usando run_number e SHA

### 4. Segurança

- Uso de secrets para tokens
- Configuração de permissões (contents: write)
- Tokens de acesso para releases

## Roadmap de Estudo 📚

### Semana 1: Fundamentos

- [ ] GitHub Actions YAML syntax
- [ ] Eventos e triggers
- [ ] Expressões e contextos
- [ ] Variáveis e secrets

#### Projeto Prático:

```yaml
# Criar workflow básico que:
- Responde a diferentes eventos
- Usa variáveis de ambiente
- Trabalha com secrets
```

### Semana 2: Jobs e Steps

- [ ] Configuração de runners
- [ ] Dependências entre jobs
- [ ] Condicionais e matrizes
- [ ] Outputs e inputs

#### Projeto Prático:

```yaml
# Expandir workflow para:
- Usar múltiplos jobs
- Adicionar condicionais
- Implementar matrix builds
```

### Semana 3: Ambientes e Runners

- [ ] Windows vs Linux runners
- [ ] Setup de ambientes
- [ ] Containers
- [ ] Cache de dependências

#### Projeto Prático:

```yaml
# Criar workflows para:
- Testar em diferentes sistemas
- Usar containers
- Implementar caching
```

### Semana 4: Artifacts e Releases

- [ ] Upload/Download de artifacts
- [ ] Criação de releases
- [ ] Versionamento
- [ ] Assets e tags

#### Projeto Prático:

```yaml
# Aprofundar em:
- Gestão de artifacts
- Automação de releases
- Versionamento semântico
```

### Semana 5: Segurança

- [ ] Tokens e PATs
- [ ] Permissões e escopos
- [ ] Secrets management
- [ ] Best practices

#### Projeto Prático:

```yaml
# Focar em:
- Segurança do workflow
- Permissões granulares
- Auditoria e logs
```

## Recursos de Estudo 📖

### Documentação Oficial

- [Workflow Syntax](https://docs.github.com/pt/actions/using-workflows/workflow-syntax-for-github-actions)
- [Security Guides](https://docs.github.com/pt/actions/security-guides)
- [Creating Actions](https://docs.github.com/pt/actions/creating-actions)

### Ferramentas

- [act](https://github.com/nektos/act) - Teste local de workflows
- [actionlint](https://github.com/rhysd/actionlint) - Validação de syntax
- [GitHub CLI](https://cli.github.com/) - Interface de linha de comando

### Exemplos e Templates

- [Starter Workflows](https://github.com/actions/starter-workflows)
- [GitHub Actions Samples](https://github.com/actions/actions-workflow-samples)

## Melhorias Futuras para o Projeto 🚀

### 1. Otimizações

```yaml
- Implementar cache de dependências
- Usar matrix builds para diferentes versões do Python
- Adicionar testes automatizados
```

### 2. Segurança

```yaml
- Revisar permissões
- Implementar scanning de segurança
- Adicionar validações de inputs
```

### 3. CI/CD Avançado

```yaml
- Adicionar ambientes (dev, staging, prod)
- Implementar deploy automático
- Adicionar notificações
```

## Dicas de Estudo 💡

1. Comece pelos fundamentos e avance gradualmente
2. Pratique com projetos reais
3. Explore o GitHub Actions Marketplace
4. Participe da comunidade
5. Documente seus aprendizados
6. Revise workflows de projetos populares

## Links Úteis 🔗

- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [GitHub Skills](https://skills.github.com/)
- [GitHub Community](https://github.community/)
- [GitHub Actions Community](https://github.com/topics/github-actions)
- [Awesome GitHub Actions](https://github.com/sdras/awesome-actions)
