# Legendas - Naked and Afraid Apocalypse PT-BR

Este repositório contém legendas em inglês para "Naked and Afraid Apocalypse" Temporada 1, e scripts para traduzi-las para português brasileiro (pt-BR).

## Arquivos

### Legendas Originais (Inglês)
- Naked.and.Afraid.Apocalypse.S01E01.1080p.HEVC.x265-MeGusta.srt
- Naked.and.Afraid.Apocalypse.S01E02.720p.WEB.H264-JFF.srt
- Naked.and.Afraid.Apocalypse.S01E03.720p.WEB.H264-JFF.srt
- Naked.and.Afraid.Apocalypse.S01E04.Stormageddon.720p.WEB.h264-CBFM.srt
- Naked.and.Afraid.Apocalypse.S01E05.1080p.HEVC.x265-MeGusta.srt
- Naked.and.Afraid.Apocalypse.S01E06.1080p.HEVC.x265-MeGusta.srt
- Naked.and.Afraid.Apocalypse.S01E07.720p.WEB.H264-JFF.srt
- Naked.and.Afraid.Apocalypse.S01E08.1080p.HEVC.x265-MeGusta.srt

### Scripts de Tradução

1. **translate_with_deep_translator.py** (RECOMENDADO)
   - Script completo e funcional para tradução automática
   - Usa a biblioteca `deep-translator`
   - Requer conexão com a internet

2. **translate_subtitles.py**
   - Framework básico para tradução
   - Suporta múltiplos backends de tradução

3. **direct_translate.py**
   - Script para tradução direta/manual
   - Útil para integração com outras ferramentas

## Como Traduzir

### Método 1: Tradução Automática (Recomendado)

Em uma máquina com acesso à internet:

```bash
# Instalar dependências
pip install deep-translator

# Executar tradução
python3 translate_with_deep_translator.py
```

Isso irá:
- Encontrar todos os arquivos .srt no diretório
- Traduzir cada um para português brasileiro
- Salvar com sufixo `.pt-BR.srt`
- Pular arquivos já traduzidos

### Método 2: Usando Ferramentas Profissionais

Ferramentas recomendadas:
- **Subtitle Edit** - Editor gratuito com tradução integrada
- **Aegisub** - Editor avançado de legendas
- Serviços profissionais de tradução de legendas

### Método 3: Tradução Manual com IA

Use ferramentas como ChatGPT ou Claude para traduzir em lotes.

## Formato dos Arquivos

As legendas seguem o formato SRT padrão:

```
1
00:00:11,000 --> 00:00:12,960
I don't know how anything
can survive out here.

2
00:00:17,260 --> 00:00:20,600
This is, like, the
end of the world.
```

Após a tradução, os arquivos terão o formato:

```
1
00:00:11,000 --> 00:00:12,960
Eu não sei como qualquer coisa
pode sobreviver aqui fora.

2
00:00:17,260 --> 00:00:20,600
Isto é, tipo,
o fim do mundo.
```

## Autorização

O arquivo `Auth.pdf` contém a documentação de autorização para este trabalho de tradução.

## Contribuindo

Pull requests são bem-vindos! Por favor:
1. Mantenha o formato SRT original
2. Preserve timestamps
3. Use português brasileiro (pt-BR)
4. Teste as legendas com o vídeo correspondente

## Licença

Veja o arquivo de autorização (Auth.pdf) para detalhes sobre direitos e uso.