# intentBox

Multiple intent extraction from a single utterance, framed as a segmentation problem

NOTE: this library is in alpha stage and the api can not yet be considered stable

# About

- multiple intent engines may coexist
- different intent engines have different weights
- one utterance might contain multiple intents
- one utterance might trigger multiple intent engines
- one utterance might contain multiple intents from different intent engines
- one intent might trigger multiple intent engines
- one intent might require multiple intent engines (WIP)
- new intent engines can be pip installed (WIP)

## Supported engines

|   engine   | entity support | regex | auto-regex |      method      | weight | default |
|:----------:|:--------------:|:-----:|:----------:|:----------------:|:------:|:-------:|
|    [adapt](https://github.com/MycroftAI/adapt)   |       yes      |  yes  |     no     |   keyword tree   |   1.0  |   yes   |
| [palavreado](https://github.com/OpenJarbas/palavreado) |       yes      |  yes  |     yes    | keyword counting |   0.8  |    no   |
|  [nebulento](https://github.com/OpenJarbas/nebulento) |     partial    |   no  |     no     |  fuzzy matching  |   0.7  |   yes   |
|   [padaos](https://github.com/MycroftAI/padaos)   |       yes      |   no  |     yes    |       regex      |   1.0  |    no   |
|  [padacioso](https://github.com/OpenJarbas/padacioso) |       yes      |   no  |     yes    |       regex      |   0.9  |   yes   |
|  [padatious](https://github.com/MycroftAI/padatious/) |       yes      |   no  |     yes    |  neural networks |   0.8  |    no   |