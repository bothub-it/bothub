---
id: bothub
title: About Bothub
sidebar_label: About Bothub
---

O Bothub é uma plataforma aberta para prever, treinar e compartilhar datasets de PLN (Processamento de Linguagem Natural) em vários idiomas. Ele é o Github para PLN, que permite construir, melhorar, treinar e traduzir datasets.

## Aplicações e Serviços

O projeto conta com três aplicações, distribuídos em 3 repositórios Git.

### Engine

[Github](https://github.com/Ilhasoft/bothub-engine) | [Documentação da API](/docs/pt-BR/api)

O Bothub Engine é reponsável por validar e persistir os dados do sistema no banco de dados. Esses dados podem ser usuários, bots (repositórios), sentenças (exemplos), treinamentos (modelos estatísticos) e logs.

Para a comunicação com outras aplicações, o Engine, serve um serviço HTTP com Rest API. Você pode consultar a documentação dessa API [aqui](/docs/api.html).

### NLP

[Github](https://github.com/Ilhasoft/bothub-nlp) | [Documentação do NLU](/docs/pt-BR/nlu)

O Bothub NLP integra ferramentas para treinamento de modelos estatísticos e para predição baseado neles.

#### NLU

Hoje o NLP conta apenas com um sistema de NLU (Natural Language Understanding) a principal funcionalidade do projeto.

O NLP recupera as sentenças (exemplos) alimentados pelo Engine e utilizando aprendizado de máquina gera modelos estatísticos. Após ter um modelo treinado o sistema passa a identificar intenções e consegue extrair entidades de textos.

Os usuários podem se comunicar com o NLP através de um serviço HTTP. Consulte a documentação dessa API [aqui](/docs/pt-BR/nlu).

##### Exemplo

Entrada:
```
Gostaria de comprar um carro.
```

Saída:
```
Intenção: "buy"

Entidades:
- Entidade: "car"
  Valor: "carro"
  Categoria: "vehicle"
```

### Webapp

[Github](https://github.com/Ilhasoft/bothub-webapp)

O Bothub Webapp é a interface web onde os usuários podem se comunicar de uma forma intuitíva com os demais projetos.

No Webapp é possível criar e gerenciar sua conta, bots, sentenças e treinamentos.