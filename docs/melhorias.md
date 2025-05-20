## Pontos de melhorias percebidos

Um ponto importante de melhoria que percebi está relacionado ao consumo do serviço externo de produtos. Em um projeto real, depender diretamente de uma API externa pode se tornar um grande problema. Diversos fatores estão envolvidos nisso: é necessário confiar constantemente nos dados recebidos, garantir que a API esteja sempre disponível, que os dados não sofram alterações inesperadas, entre outros riscos.

Por conta do tempo, não consegui estruturar uma solução mais robusta para esse caso, mas tenho algumas ideias em mente, e vou destacar uma delas abaixo:

### Utilizar um cron job para sincronização de produtos

Considerando um cenário de produção, é fundamental garantir que os produtos estejam atualizados do lado do consumidor — mesmo que não em tempo real, pelo menos com uma frequência razoável. Também é importante estarmos preparados para lidar com eventuais falhas na API externa.

Uma abordagem prática e de baixo custo seria implementar um **cron job** que executa diariamente (por exemplo, pela manhã), consome os dados da API e os armazena localmente. Isso traria maior previsibilidade e resiliência ao sistema.

No entanto, mesmo com essa estratégia, ainda precisaríamos tratar algumas questões específicas, como o controle de mudanças nos produtos. Nem sempre um `ID` igual significa que o produto permanece inalterado. Por isso, o modelo `Produto` poderia conter campos auxiliares como:

- `external_id`: para guardar o identificador vindo da API externa.
- `internal_id`: identificador interno, usado pelo nosso sistema.
- `updated`: um campo booleano indicando se o dado foi alterado em relação à última atualização.
- `last_synced_at`: (opcional) para saber quando a última sincronização ocorreu.

Com esses dados, conseguimos manter um controle mais fino sobre o estado dos produtos, garantindo consistência e reduzindo a dependência em tempo real da API externa.
