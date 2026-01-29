# Guia de Implantação e Configuração Técnica 🛠️

Este documento descreve os passos para configurar o ambiente de backend na Vercel e integrar as simulações PHET ao CircuitosEdu.

## 1. Configuração do Ambiente (Vercel)
1. Conecte seu repositório GitHub à **Vercel**.
2. Nas configurações do projeto (**Project Settings > Environment Variables**), adicione a chave:
   - `GEMINI_API_KEY`: Sua chave obtida no Google AI Studio.
3. Realize o deploy com a opção "Redeploy with clean build cache" se houver alterações de dependências.

## 2. Integração com PHET Interactive Simulations
O simulador é carregado via `<iframe>` utilizando o locale em português para melhor experiência do aluno:
`https://phet.colorado.edu/sims/html/circuit-construction-kit-ac/latest/circuit-construction-kit-ac_all.html?locale=pt`.

## 3. Estrutura de Ativos (Assets)
Para o correto funcionamento do site, a pasta `/assets` deve conter:
- `roteiro_pratica.pdf`: Guia de atividades para o aluno.
- `aluno1.jpg` a `aluno4.jpg`: Registros fotográficos da aplicação prática.

## 4. Coleta de Logs de Pesquisa
O sistema utiliza o ID de rastreio `G-676V40J9RX` para monitorar a interação dos estudantes e validar a eficácia da ferramenta para a dissertação.
