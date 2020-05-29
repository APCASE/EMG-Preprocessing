# APCASE

<p align="justify">O <a href=https://www.instagram.com/apcase.ufersa/>APCASE</a> é um projeto do laboratório de instrumentação e engenharia biomédica (LIEB) da <a href=https://ufersa.edu.br/>UFERSA</a> campus Caraúbas. Seu principal objetivo é o estudo do sinal mioelétrico para análise, classificação e predição de suas principais características, com o intuito de desenvolver tecnologias para o campo da engenharia biomédica.</p>

<p align="justify">Diante desses processos, existem diversas aplicações associadas à utilização do sinal de eletromiografia. Dentre essas, a confecção de próteses miolétricas inteligentes de baixo custo, que é uma das linhas de pesquisa do projeto APCASE, objetivando facilitar a vida das pessoas.</p>

## Software
<p align="justify">Atualmente o projeto está desenvolvendo um software para aquisição, pré-processamento e classificação do sinal mioelétrico utilizando conexão com o banco de dados não relacional <em>MongoDB</em>. O software foi projetado com o objetivo de fazer todo o processo para padronização de um conjunto de movimentos de forma bem intuitiva.</p>

## Funcionalidades
<p align="justify">Atualmente o projeto conta com duas janelas de interações:</p>

1.  Aquisição;
2.  Pré-Processamento.

<p align="justify">A janela também  conta com o menu de configuração do banco de dados. É recomendável que preencha o mesmo, todas as vezes que for necessário se fazer uma aquisição ou pré-processamento.</p>

### Aquisição
<p align="justify">Na janela de aquisição, é necessário configurar as principais propriedades do software:</p>

  *  Quantidade de canais para aquisição do biosinal;
  *  Tempo de aquisição em segundos;
  *  Frequência de aquisição em Hz;
  *  Batchsize (Pacote ou lista retornado por método do microcontrolador utilizado na aquisição);
  *  Valor mínimo para exibição no eixo das abscissas;
  *  Valor máximo para exibição no eixo das abscissas.

<p align="justify">Quando os itens citados forem configurados, basta clicar no botão iniciar aquisição e a barra de porcentagem irá começar a ser preenchida até que a aquisição acabe. Caso o usuário deseje parar a aquisição, basta clicar no botão parar aquisição que irá aparecer após o botão iniciar aquisição ser clicado</p>

<p align="justify"><strong>Observações:</strong> o método <em>generateDataTest/em> da classe <em>DataAquisition</em> do arquivo <m>aquisitionData.py</em> da pasta <em>features</em> deve ser adequado ao método de onde o usuário deseja extrair os dados.</p>
  
 ```
 @staticmethod
 def generateDataTest(nChannels, batchSize):
     #TODO: Modify this method to adequate your microcontroller
 ```

### Pré-Processamento
<p align="justify">A janela de pré-processamento mostra todas aquisições realizadas pelo usuário logo, é necessário selecionar a aquisição que se deseja trabalhar em cima. A partir da seleção dos canais, a janela irá mostrar as opções de funções pré-processamento que se deseja exibir no gráfico. O <em>vertical slider</em> na janela é utilizado como ferramento para selecionar um <em>bias</em> que por sua vez tem a função de identificar um movimento, isto é, se os valores contidos nos gráficos forem menor que o <em>bias</em>, estes serão considerados como um repouso na aquisição.</p>

<p align="justify">Entre as funções de pré-processamento implementadas, têm-se:</p>

  *  <strong>IEMG</strong>;
  *  <strong>MAV</strong>;
  *  <strong>SSI</strong>;
  *  <strong>RMS</strong>;
  *  <strong>LOG</strong>;
  *  <strong>WL</strong>;
  *  <strong>AAC</strong>;
  *  <strong>DASDV</strong>.

<p align="justify">Todas essas funções estão implementadas no arquivo <em>software/features/preprocessing.py</em>.</p>

<p align="justify">Uma vez selecionada as funções que se deseja salvar, para salvar os dados em arquivos <em>csv</em>, basta clicar no botão <em>salvar dados para treinamento</em>. O programa irá gerar três arquivos:</p>

  *  signalRaw.csv
  *  signalPreprocessed.csv
  *  label.csv
  
<p align="justify">Para treinamento de um agente classificador, basta utilizar o sinal raw ou já preprocessado como <em>features</em> e o label como saída para treinamento. <strong>Observação:</strong> Não esqueça de alterar o valor do movimento</p>

#### Bibliotecas Utilizadas
  *  PyQT5;
  *  Numpy;
  *  Matplotlib;
  *  Scikit Learn;
  *  Scipy;
  *  Pandas;
  *  PyMongo.
