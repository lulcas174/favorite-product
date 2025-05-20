## Escolha de tecnologias

A escolha de tecnologia de um projeto geralmente eu vou pensar na facilidade de manutenção, em quantos devs vamos ter no time para manter, escolha futura e tal, mas no caso de um projeto menor feito para mim eu acabo escolhendo a tecnologia que eu tenho mais estudado ultimamente ou a que seria mais fácil de subir um projeto.

Eu fiquei indeciso entre Python + FastAPI ou Python + Django, ambas para projetos com esse escopo pequeno são muito boas, sendo a com FastAPI um pouco mais onerosa para configurar e etc.

Alguns levantamentos que eu fiz antes de escolher a tecnologia:

- Qual vai me fazer subir o básico do projeto em menos tempo?
- Qual é mais fácil para colocar em um container e já rodar a aplicacao?
- Qual delas é mais simples de entender e montar um design funcional?

O triste é que _todas_ as perguntas serviam tanto para o Django quanto para o FastAPI, ambos respondem bem para essas perguntas, mas o que me fez decidir e escolher o FastAPI é justamente o fato de ter "menos" abstrações, eu teria controle do ponto A ao ponto B. O ponto negativo é que justamente ter esse controle me fez perder mais tempo configurando, estruturando o projeto, porém eu tenho mão em todo código escrito, desde o setup do index até a configuração das migrations.


### Tecnologias aplicadas
- FastAPI
- Alembic
- SQLAlchemy
- Flake8
- Docker
- PostgreSQL (banco escolhido)

##### Bibliotecas auxiliares como requests foram utilizadas no projeto