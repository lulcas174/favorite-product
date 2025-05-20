## Arquitetura e filosofia de design do projeto.

Como dito no tópico de tecnologia (se não viu, é [este aqui](/docs/tecnologias.md)), toda a escolha vai passar por certos critérios — a arquitetura e o design do projeto também. Veja, esse é um projeto de escopo simples. É assustador dizer que poderia ser apenas um grande `index.py` com centenas de linhas. É mentira? Muito provavelmente não. Isso poderia ser aplicado. É bom? Tem fácil manutenção? Com certeza não.

### A final, qual arquitetura você escolheu?

Eu me baseei muito no conceito de *clean arch*. Eu acho que fica fácil quando separamos cada responsabilidade. Óbvio, não é um espelho do conceito original do *clean arch*. Eu acabo optando por não seguir à risca e tomar minhas próprias decisões, muito pelo fato de estar acostumado a atuar com certas abstrações ou formas de aplicar determinado conceito.

### Beleza, mas e o padrão de design?

Falar sobre design é interessante. O *pattern* que eu geralmente acabo utilizando é o DDD. Eu acho muito cômodo utilizar o DDD junto de um *clean arch* ou até mesmo hexagonal. A ideia de separar e o projeto rodar em cima do domínio, para mim, é muito boa. Facilita demais debugar, resolver problemas, essas coisas do dia a dia.
