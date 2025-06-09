# Indicações Iniciais

A internet faz pedidos HTTP ao Load Balancer
- Endereço Típico: http://localhost:8080/**100**
  - **Nota:** O 100 representa a precisão

Workers/Servers são do tipo HTTP_Server e têm a capacidade de responder

Load Balance é o responsável por escolher um server e cria uma espécie de túnel entre o pedido e o HTTP_Server

Todas as policies vão ter um método select_server()
- É chamado sempre que há um novo pedido

## Class Policy N2One

    def __init__(servers):
        self.servers = servers

    def select_server():                <--- Novos Pedidos
        return self.servers[0]

    def update(* arg):                  <--- Final Pedido
        pass

***Nota:*** O servers passado como argumento é a lista de endereços de servidores.

***Nota:*** O update é chamado quando um pedido termina. Depois do servidor enviar a resposta, elimina o túnel (já não tem mais nada a comunicar)

***Nota:*** Fica à espera que um pedido acabe para começar outro

## Class Policy RoundRobin
O primeiro pedido vai para o primeiro servidor, o segundo pedido para o segundo servidor e assim sucessivamente.

Acaba por definir que todos os pedidos têm a mesma carga de trabalho, o que não é verdade.

## Class Policy LeastConnections

Precisa de saber o número de conexões que existe em cada servidor
- Aumenta o número de conexões no select_server()
- Diminui o número de conexões no update()

## Class Policy LeastResponseTime
Tenta manter atualizado o menor tempo de resposta para cada servidor, o que implica saber o tempo inicial de cada servidor.

# Formas de testar    

    $./setup.sh -> 4 servidores e policy N2One
    $./setup.sh 4 RoundRobin -> 4 servidores e policy RoundRobin

***Noutro terminal:***

    $curl -s https://localhost:8080/10