# python-synthesizer
## Trabalho Final de Processamento Digital de Sinais
Sintetizador de som com Pygame e Numpy em Python. Projeto Base: https://github.com/FinFetChannel/Python_Synth

## Fazendo o sintetizador de som
### 1 - making_one_sample
A primeira coisa que deve ser considerada é a taxa de amostragem, ou seja, quantos valores precisamos definir para um segundo de som. Definimos então o valor padrão do mixer Pygame que é de 44.100 amostras por segundo.

A segunda coisa é a forma da onda, responsável pela qualidade do som, ou timbre (razão pela qual instrumentos diferentes soam tão diferentes para a mesma frequência ou tom). 

A forma de onda mais pura é a senoidal e uma das mais fáceis de gerar no numpy, por isso iniciou-se com ela, mas outros tipos serão abordados posteriormente, como a quadrada e a triangular. A onda senoidal, será gerada pela função cosseno.

Para gerar a matriz de valores de uma onda senoidal, precisamos da taxa de amostragem, 44100, a frequência, que pode ser qualquer valor inferior a 22,5 kHz pela frequência de Nyquist (a maioria das pessoas não consegue ouvir nada acima de 16 ou 17 kHz) e a duração da amostra de som.

Com a duração e a taxa de amostragem podemos calcular o número de quadros que a amostra terá. Com o número de quadros e a duração podemos gerar um array com os tempos de cada quadro, que por sua vez é alimentado na função cosseno multiplicado por 2π e a frequência, resultando em um array com todos os valores do sinal sonoro.

Por fim, para ouvi-lo, primeiro temos que transformar este array em um array de som pygame, assim, o multiplicamos pelo valor de 32767, duplicado (para mixer estéreo), transposto e transformado no tipo int16. Então podemos usar a função make_sound do pygame sndarray, o .copy() é necessário para tornar o array contíguo na memória. 

Depois disso basta executar e ouvir a amostra de som criada.

### 2 - making_samples_for_every_note
Resumidamente, as notas são frequências selecionadas que soam bem quando tocadas juntas, sendo a proporção entre elas um dos fatores mais importantes na música. A proporção/razão mais usada na música ocidental é a raiz de dois de doze.

Para gerar amostras para todas as teclas de um piano, precisamos então de uma lista com todas as notas (noteslist.txt), e definir a frequência da primeira nota (16,35160 Hz), dessa forma, as frequências restantes podem ser calculadas a partir da frequência inicial e a da proporção a ser utilizada. Assim, é possível armazenar uma amostra para cada nota em um dicionário. 

Para simular um piano, para as teclas, vamos usar os caracteres de um teclado normal, Um piano possui 108 teclas que podem ser subdivididas em três grupos de 36.

Um piano possui 108 teclas, para simular as teclas do piano utilizaremos as teclas do teclado, de forma que, subdividimos as notas em 3 grupos de 36. As teclas do teclado a serem utilizadas serão (123456789qwertyuiopasdfghjklzxcvbnm,) e a alternância entre os três grupos de  notas será feito pelas teclas (0-=).

Ao executar o arquivo será todas as notas de duração de 1,5s serão tocadas espaçadas no período de tempo de 0,1s com um fadeout de 0,1s.

### 3 - keyboard_synth
Agora que temos todas as amostras de som para cada nota, pode-se começar a utilizar o sintetizador. Para isso, foi feita uma janela pygame, para capturar as teclas digitadas e reproduzir as amostras correspondentes. Uma nota começa a tocar quando um evento keydown é registrado e para após a duração da amostra ou quando um evento keyup é registrado. 

### 4 - display_and_waveforms
Para exibir as notas na tela, foi definido uma posição e uma cor para cada uma das notas. Para as posições, as notas foram organizadas em uma grade de 12 por 9. Para as cores imitou-se um arco-íris, onde as frequências sonoras mais graves são avermelhadas, as medianas são esverdeadas e as agudas são azuladas. As posições e cores também são armazenadas no dicionário de notas. As notas são então exibidas na tela. Ao tocar, a nota atual fica destacada com uma cor branca, após o fim do evento de tecla ela retorna à cor original. Após alguns ajustes temos um sintetizador de som básico e visual.

Para este projeto, procuramos obter formas de onda quadradas e triangulares ao menos de forma aproximada. A onda quadrada pode ser aproximada multiplicando a onda senoidal por um fator "grande" (como o 10),  e cortando o resultado na faixa de -1 a 1. Já as ondas triangulares podem ser construídas em cima das ondas quadradas utilizando integração, isso é feito por meio da função cumsum do Numpy, depois disso basta dimensionar  para o intervalo -1 a 1. Esse método se aplica bem em amostras curtas, mas erros cumulativos podem ocorrer em amostras mais longas.

Vale ressaltar que poderíamos tentar criar outras formas de onda, por exemplo, somando múltiplos da frequência base, para tentar imitar o timbre de outro determinado instrumento.

## Salvando sequência de notas para replay
### 5 - saving_sequence_of_notes
Para salvar uma sequência de notas para reprodução posterior ou algo do tipo. Decidiu-se realizar a exportação das informações necessárias para um arquivo .txt.

Assim, para isso,  é necessário o registro de 3 itens principais, o tipo de evento (keyup ou keydown), a nota que foi tocada e o intervalo entre cada evento. Dessa forma, todos os eventos keydown e keyup passam a ser armazenados em uma lista como um valor binário, como a música não é apenas uma sequência de notas (o intervalo entre cada nota também é importante), armazenamos também a data e hora de cada evento, assim como a nota correspondente a tecla que foi tocada, e por último antes de salvar em um arquivo .txt, transformamos essas datas e horários em intervalos de tempo.  

O resultado final é um arquivo de texto com todas as notas que foram tocadas, quando começam e quando terminam.

### 6 - replaying_sequence_of_sound
Para reproduzir a sequência de som, a principal diferença aqui é que não há pressionamentos de tecla reais, em vez disso, o programa espera até a hora da nova nota ser tocada, então as teclas no dicionário de notas são as próprias notas. Assim, basta realizar alguns ajustes no código.

Vale destacar que utilizando este método é possível reproduzir uma sequência de som apenas criando um arquivo .txt na formatação correta. Bem como realizar edição de uma sequência de notas que foi tocada e armazenada.

Ao executar o resultado é a reprodução da sequência de notas armazenadas no arquivo soundsequence.txt.

### 7 - replaying_supermario
Ao executar o resultado é a reprodução da sequência de notas armazenadas no arquivo supermario.txt.

## Exportando o som em formato wav
### 8 - creating_soundtrack
Ao invés de tocar nota por nota, podemos gerar um array com todas as notas e tocá-lo de uma só vez ou salvar em um arquivo wav.

Para isso, fazemos alguns ajustes  na função de sintetizador. Primeiro, adicionou-se um fade a cada amostra (para replicar o fadeout usado em eventos de keyup) com uma duração de 0,1 s, portanto, nenhuma nota menor que isso é permitida. Além disso, não precisamos transformar o array em um som, mas em uma lista, pois é mais fácil adicionar uma nova amostra ao final da faixa.

Depois disso, passamos por todas as notas na sequência de som e geramos uma amostra para cada uma delas para adicionar a uma lista. As amostras são estendidas enquanto os intervalos são reduzidos em 0,1 segundo para levar em conta os fadeouts. No final, a lista é transformada novamente em um array e em um som pygame. Uma espera da duração do som é adicionada para garantir que ele seja reproduzido até o fim.

### 9 - exporting_wav
Exportamos a faixa como um arquivo wav, utilizando a biblioteca wave.
