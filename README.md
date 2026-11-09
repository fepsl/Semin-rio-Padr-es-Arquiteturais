# Event Sourcing: exemplo simples de estoque

O sistema controla a quantidade de um único produto: cadernos.
Usa apenas Python 3 e sua biblioteca padrão. Não precisa instalar pacotes.

## Executar

Extraia o ZIP, abra um terminal na pasta que contém `app.py` e execute:

```sh
python app.py
```

No Windows, também é possível usar `py app.py` se o comando `python` não estiver disponível.

## Demonstrar na apresentação

Comece com uma pasta sem `eventos.jsonl` para obter os valores abaixo.

1. Escolha **1**, informe **10**: registra uma entrada.
2. Escolha **2**, informe **3**: registra uma saída.
3. Escolha **3**: mostra os dois eventos.
4. Escolha **4**: reconstrói o saldo **7**.
5. Escolha **0** e execute o programa novamente.
6. Escolha **4**: o saldo continua **7**, pois o programa relê os eventos salvos.
7. Tente retirar **100**: o sistema rejeita a operação e não salva um novo evento.

Para uma demonstração automática, que sempre começa do zero em um arquivo temporário:

```sh
python app.py --demo
```

Saída esperada:

```text
Entrada de 10 registrada.
Saída de 3 registrada.
1. EntradaRegistrada: 10
2. SaidaRegistrada: 3
Saldo reconstruído: 7
Saída de 100 rejeitada: Estoque insuficiente.
Total de eventos salvos: 2
```

## Estrutura e responsabilidades

```text
event-sourcing-estoque/
  app.py          # Menu e coordenação das operações
  estoque.py      # Regras e reconstrução do saldo
  event_store.py  # Leitura e acréscimo de eventos no arquivo
  README.md
  eventos.jsonl   # Surge depois da primeira operação no menu
```

O arquivo de eventos terá este conteúdo após uma entrada de 10 e uma saída de 3:

```json
{"tipo": "EntradaRegistrada", "quantidade": 10}
{"tipo": "SaidaRegistrada", "quantidade": 3}
```

Cada linha é um JSON independente. O saldo 7 não fica salvo em outro arquivo.
O programa calcula o saldo aplicando os eventos, na ordem em que foram gravados.

## Componentes e conectores

- **Interface e coordenação:** `app.py` recebe a opção e chama as funções.
- **Domínio:** `estoque.py` verifica quantidades e impede saídas superiores ao saldo.
- **Event Store:** `event_store.py` guarda o histórico em `eventos.jsonl`.
- **Conectores:** chamadas de funções dentro do processo e leitura/escrita de arquivo.
- **Comunicação:** síncrona e local. Uma operação termina antes de o menu aceitar a próxima.

## Onde aparece o padrão

Em `salvar_evento`, o modo `"a"` acrescenta eventos ao final do arquivo.
Em `reconstruir_saldo`, o sistema reaplica os eventos para obter o estado atual.
Em `registrar`, o sistema reconstrói o estado e valida a operação antes de gravar o fato.

Uma solicitação de saída pode falhar. O evento `SaidaRegistrada` só existe depois da validação.
O replay apenas calcula o estado e não repete efeitos externos.

## Limites do exemplo

Exemplo didático para um único processo e um único produto. Não execute dois menus
ao mesmo tempo usando o mesmo arquivo: não há controle de concorrência.
O programa não oferece operações para editar ou apagar eventos, mas alguém com
acesso ao arquivo pode alterá-lo. Uma aplicação real também precisaria tratar falhas
de gravação, permissões, backups e evolução do formato dos eventos.

CQRS, filas, microsserviços e snapshots ficam fora deste exemplo.
