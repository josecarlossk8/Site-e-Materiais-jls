# Status do Site e Deploy

## Projeto

- Repositorio GitHub: https://github.com/josecarlossk8/Site-e-Materiais-jls
- Projeto Vercel: `va`
- Time Vercel: `Jose Carlos - JLS`
- URL temporaria validada: https://va-jade-nu.vercel.app/
- Dominio oficial em configuracao: https://jlslog.com.br/

## Status atual

O site atual da JLS ja esta publicado na Vercel e pode ser compartilhado pelo link temporario enquanto o dominio oficial termina de apontar para o projeto.

O dominio oficial `jlslog.com.br` e o subdominio `www.jlslog.com.br` ja foram adicionados ao projeto correto da Vercel. A etapa pendente esta no DNS da Hostinger.

## Registros DNS solicitados pela Vercel

Na Hostinger, ajustar apenas os registros do site:

| Tipo | Nome | Valor |
|---|---|---|
| A | `jlslog.com.br` | `76.76.21.21` |
| A | `www.jlslog.com.br` | `76.76.21.21` |

## Regra importante

Nao apagar nem alterar registros de e-mail:

- MX
- TXT
- SPF
- DKIM
- DMARC

## Validacao apos DNS

Depois que a pessoa com acesso a Hostinger fizer os ajustes, validar:

1. `https://jlslog.com.br/`
2. `https://www.jlslog.com.br/`
3. Se ambas as URLs abrem o site novo.
4. Se o certificado SSL aparece como seguro.
5. Se o formulario e os botoes de WhatsApp, Instagram, LinkedIn e Portal do Cliente funcionam.

## Observacao comercial

Enquanto o dominio oficial propaga, usar o link temporario da Vercel apenas com time interno, parceiros proximos ou validacoes. Para divulgacao aberta, priorizar o dominio oficial quando estiver ativo.
