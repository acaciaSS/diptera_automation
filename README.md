# Identificação Automática de Larvas de Culicidae (Diptera)
Pipeline de identificação taxonómica automática (género e espécie) de larvas de mosquito a partir de imagens microscópicas, usando redes neuronais convolucionais (CNNs).

---

## Table of Contents
- Description of the Project
- Dataset
- Installation
- Prerequisites
- Expected Outputs
- Usage
- Run Specific Analyses
- Configuration
- Troubleshooting
- Authors and Acknowledgments
- License
- Citation

---

## Description of the Project

Este projeto é o resultado de um estágio curricular da **Licenciatura em Bioinformática** (Escola Superior de Tecnologia do Barreiro / Instituto Politécnico de Setúbal), realizado no **Instituto de Higiene e Medicina Tropical (IHMT)**, Universidade NOVA de Lisboa.

Os mosquitos (família Culicidae) incluem vetores de doenças com elevado impacto em saúde pública. A identificação taxonómica das suas larvas é tradicionalmente feita por observação morfológica ao microscópio, uma tarefa que exige treino especializado e é morosa. Este projeto explora a identificação automática de larvas a partir de imagens microscópicas de quatro estruturas morfológicas diagnósticas, usando *deep learning*.

O objetivo principal foi construir um sistema de classificação **hierárquico em dois níveis** (género, e depois espécie dentro do género), com um modelo CNN independente por estrutura morfológica, combinado por votação ponderada. O pipeline:

- Organiza as imagens da coleção entomológica do IHMT por estrutura morfológica, género e espécie
- Treina, para cada estrutura, um modelo de género e um modelo de espécie por género (transfer learning com EfficientNetB0, fine-tuning)
- Avalia cada modelo (classification report, matrizes de confusão, cobertura/accuracy seletiva)
- Deteta casos "desconhecidos" — larvas que não se assemelham a nenhuma classe vista no treino — através da distância no espaço de características da CNN
- Disponibiliza uma ferramenta de identificação para utilizador final (interface web, Gradio)

Paralelamente, e sem contribuição direta para o pipeline de identificação de larvas, foram desenvolvidos dois scripts para download automatizado de imagens de mosquitos adultos, a partir do **iNaturalist** e do **diptera.info**.

---

## Dataset

O dataset principal é uma coleção de imagens microscópicas de larvas de mosquito, adquirida no âmbito deste estágio.

**Organismo:** Culicidae — 24 espécies dos géneros *Aedes*, *Anopheles*, *Culex* e *Culiseta*
**Origem das imagens:** Coleção entomológica do IHMT (preparações permanentes em lâminas de vidro com meio de Berlese)
**Equipamento:** Microscópio Olympus BX51, câmara digital Olympus SC30, software analySIS getIT
**Ampliações:** Objetivas de 4×, 10× e 40×
**Estruturas morfológicas fotografadas:** Cápsula cefálica (cab), segmento 8 (seg8), segmento anal (segAn), sifão respiratório (sif) — *Anopheles* não possui sifão
**Organização:** Uma pasta por espécime (`AutoID-[Género]-larva-[XXXX]`), dentro de uma pasta por espécie (`Género.espécie`)
**Critério de inclusão no treino de espécie:** mínimo de 3 larvas (pastas AutoID) por espécie

**Fonte:** Coleção entomológica do IHMT (dados não públicos; acesso apenas através da pasta partilhada do projeto no Google Drive)

---

## Installation

Clonar o repositório:

```bash
git clone https://github.com/<utilizador>/diptera_automation.git
cd diptera_automation
```

Este projeto corre em notebooks Google Colab, pelo que não é necessário instalar um ambiente local — basta abrir os ficheiros `.ipynb` diretamente no Colab (`File > Upload notebook` ou a partir do Google Drive).

Verificar acesso ao dataset:

```
MyDrive/Fotos-Micro/Fotos-Micro-512
```

---

## Prerequisites

- **Conta Google** com acesso à pasta do dataset no Drive
- **Google Colab** com *runtime* GPU (T4) — `Runtime > Change runtime type > T4 GPU`
- Bibliotecas Python: TensorFlow/Keras, scikit-learn, pandas, matplotlib, seaborn (pré-instaladas no Colab) e Gradio (instalado automaticamente pelo notebook de inferência)

---

## Expected Outputs

Todos os outputs são guardados em `MyDrive/diptera_models/`.

### Modelos
- `genus_<estrutura>.keras` — um por estrutura morfológica (cab, seg8, segAn, sif)
- `species_<estrutura>_<género>.keras` — um por estrutura × género
- `genus_<estrutura>_ood.npz`, `species_<estrutura>_<género>_ood.npz` — estatísticas de deteção de "desconhecido"
- `classes.json` — nomes das classes de cada modelo

### Avaliação
- `resumo_genero.csv`, `resumo_especie.csv` — accuracy, macro/weighted F1, cobertura e accuracy seletiva, por modelo
- `resumo_treino.csv` — épocas usadas por fase e accuracy/loss de validação final, por modelo
- Matrizes de confusão (contagens e normalizadas), heatmaps resumo, gráficos de barras comparativos

### Ferramenta de identificação
- Interface Gradio com a identificação de género e espécie por votação ponderada, e a percentagem de "desconhecido"

---

## Usage

Correr os notebooks pela seguinte ordem:

```
1. pre_processamento.ipynb
2. diptera_estruturas_v3_3.ipynb   (Passo 1 ao Passo 10)
3. diptera_inference.ipynb         (sempre que for necessário identificar uma larva nova)
```

No `diptera_estruturas_v3_3.ipynb`, correr todas as células por ordem, de cima para baixo. Ver a tabela de passos abaixo.

| Passo | O que faz |
|---|---|
| Imports | Todas as bibliotecas usadas no notebook |
| 1 | Liga ao Google Drive |
| 2 | Configuração (caminhos, hiperparâmetros) |
| 3 | Organiza as imagens por estrutura/género/espécie |
| 4 | Remove espécies com menos de 3 larvas |
| 5 | Define as funções de treino, avaliação e deteção de "desconhecido" |
| 6 | Treina os modelos de género |
| 7 | Treina os modelos de espécie |
| 8 | Avalia todos os modelos e exporta os CSVs de resumo |
| 8b | Visualizações agregadas (heatmaps, gráficos de barras) |
| 8c | Resumo do treino (épocas por fase, accuracy/loss final) |
| 9 | Confirmação de que tudo ficou guardado |
| 10 | Teste manual com fotos de uma larva nova |

---

## Run Specific Analyses

Depois de correr o `diptera_estruturas_v3_3.ipynb` até ao Passo 9, é possível identificar uma larva nova sem repetir o treino, usando apenas o `diptera_inference.ipynb`:

1. Abrir `diptera_inference.ipynb` no Colab
2. Correr as células por ordem (liga ao Drive, instala o Gradio, carrega os modelos já guardados)
3. Na interface, carregar as fotos disponíveis da larva (uma ou mais estruturas)
4. Ler o resultado: percentagem de cada género/espécie candidato, mais a percentagem de "Desconhecido"

---

## Configuration

Editar as constantes no **Passo 2** de `diptera_estruturas_v3_3.ipynb`:

```python
DATASET_PATH = '/content/drive/MyDrive/Fotos-Micro/Fotos-Micro-512'
STRUCTURES   = ['cab', 'seg8', 'segAn', 'sif']
MIN_LARVAE   = 3      # minimo de larvas por especie para treinar essa especie
IMG_SIZE     = 224
BATCH_SIZE   = 16
EPOCHS_FASE1 = 20      # epocas maximas - fase 1 (classificador)
EPOCHS_FASE2 = 10      # epocas maximas - fase 2 (fine-tuning)
VAL_SPLIT    = 0.2
UNKNOWN_THRESHOLD = 0.55
```

---

## Troubleshooting

**Problema:** `OSError: [Errno 107] Transport endpoint is not connected`
**Solução:**
```
Runtime > Desconectar e eliminar o runtime, depois Connect outra vez
e correr o notebook desde o Passo 1.
```

**Problema:** O link do `diptera_inference.ipynb` (Gradio) deixou de funcionar
**Solução:**
Isto acontece sempre que o *runtime* do Colab desliga (inatividade, fecho do
separador, limite de sessão). Os modelos guardados no Drive não são afetados —
basta correr o notebook outra vez para obter um novo link.

**Problema:** GPU não disponível / treino muito lento
**Solução:**
```
Runtime > Change runtime type > T4 GPU
```

**Problema:** Espécie/género não aparece no `classes.json`
**Solução:**
Confirmar que existem pelo menos `MIN_LARVAE` larvas (pastas AutoID) para
essa espécie — ver o resumo impresso no Passo 3/4.

---

## Authors and Acknowledgments

**Autor:**
- Acácia Santos LBINF nº202200054

**Orientadores:**
- Prof. Luís Filipe Lopes (IHMT)
- Prof. Teresa Novo (IHMT)

---

## License

[]

---

## Citation

```text
Acácia Santos  (2026).
Identificação Automática de Larvas de Culicidae (Diptera) por Deep Learning.
Relatório de Estágio, Licenciatura em Bioinformática, ESTB/IPS.
Instituto de Higiene e Medicina Tropical, Universidade NOVA de Lisboa.
```
