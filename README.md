# APCASE

<p style="text-align:justify">O <a href=https://www.instagram.com/apcase.ufersa/>APCASE</a> é um projeto do laboratório de instrumentação e engenharia biomédica (LIEB) da <a href=https://ufersa.edu.br/>UFERSA</a> campus Caraúbas. Seu principal objetivo é o estudo do sinal mioelétrico para análise, classificação e predição de suas principais características, com o intuito de desenvolver tecnologias para o campo da engenharia biomédica.</p>

<p style="text-align:justify">Diante desses processos, existem diversas aplicações associadas à utilização do sinal de eletromiografia. Dentre essas, a confecção de próteses miolétricas inteligentes de baixo custo, que é uma das linhas de pesquisa do projeto APCASE, objetivando facilitar a vida das pessoas.</p>

## Software
<p style="text-align:justify">Atualmente o projeto está desenvolvendo um software para aquisição, pré-processamento e classificação do sinal mioelétrico utilizando conexão com o banco de dados não relacional <em>MongoDB</em>. O software foi projetado com o objetivo de fazer todo o processo para padronização de um conjunto de movimentos de forma bem intuitiva.</p>

## Funcionalidades
<p style="text-align:justify">Atualmente o projeto conta com duas janelas de interações:</p>

1.  Aquisição;
2.  Pré-Processamento.

### Aquisição
<p style="text-align:justify">Na janela de aquisição, é necessário configurar as principais propriedades do software:</p>

  *  Quantidade de canais para aquisição do biosinal;
  *  Tempo de aquisição em segundos;
  *  Frequência de aquisição em Hz;
  *  Batchsize (Pacote ou lista retornado por método do microcontrolador utilizado na aquisição);
  *  Valor mínimo para exibição no eixo das abscissas;
  *  Valor máximo para exibição no eixo das abscissas.

<p style="text-align:justify">Quando os itens citados forem configurados, basta clicar no botão iniciar aquisição e a barra de porcentagem irá começar a ser preenchida até que a aquisição acabe. Caso o usuário deseje parar a aquisição, basta clicar no botão parar aquisição que irá aparecer após o botão iniciar aquisição ser clicado</p>

<p style="text-align:justify"><strong>Observações:</strong> o método <em>generateDataTest/em> da classe <em>DataAquisition</em> do arquivo <m>aquisitionData.py</em> da pasta <em>features</em> deve ser adequado ao método de onde o usuário deseja extrair os dados.</p>
  
 ```
 @staticmethod
 def generateDataTest(nChannels, batchSize):
     #TODO: Modify this method to adequate your microcontroller
 ```

### Pré-Processamento
