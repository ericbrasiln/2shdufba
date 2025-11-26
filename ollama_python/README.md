# 🧠 Leitor de Documentos com Ollama  
### `read_doc.py`

Este script em Python utiliza a API local do **[Ollama](https://ollama.com)** para **ler um documento de texto (`.txt`)**, aplicar um **prompt personalizado** e **gerar uma resposta** com base no conteúdo do arquivo, usando **modelos de linguagem locais (LLMs)** como Phi, Mistral, Gemma ou Llama.

O código foi desenvolvido para fins didáticos na disciplina **IM1256 – Introdução à História Digital** (PPGIHD/UFRRJ), ministrada pelo Prof. Eric Brasil, e pode ser executado em **Windows, Linux ou macOS**.

---

## ⚙️ Funcionalidades

✅ Lê um arquivo `.txt` informado pelo usuário.  
✅ Solicita um **prompt** (instrução ou pergunta).  
✅ Lista automaticamente os **modelos Ollama** disponíveis localmente.  
✅ Permite escolher o modelo desejado (1, 2, 3…).  
✅ Envia o conteúdo do texto + prompt ao modelo e exibe a resposta.  
✅ Compatível com qualquer modelo carregado no Ollama (Phi, Mistral, Gemma, etc.).  
✅ Didático, documentado e pronto para uso em oficinas de História Digital e IA Generativa.

---

## 🧩 Estrutura do projeto

```

📁 ollama_reader/
├── read_doc.py
└── README.md

````

---

## 💻 Instalação

1. **Baixe e instale o Ollama**  
   👉 [https://ollama.com/download](https://ollama.com/download)

2. **Inicie o servidor Ollama**
   - No **Linux**, execute no terminal:
     ```bash
     ollama serve
     ```
   - No **Windows/macOS**, basta abrir o aplicativo Ollama.

3. **Baixe ao menos um modelo local (exemplo):**
   ```bash
   ollama pull phi3:mini
````

Você também pode instalar outros, como:

```bash
ollama pull mistral
ollama pull gemma
ollama pull llama3
```

4. **Garanta que o servidor Ollama está ativo**
   Verifique em [http://localhost:11434](http://localhost:11434).
   Se aparecer “404 not found”, está tudo certo — o servidor está rodando.

---

## 🚀 Execução

1. **Execute o script:**

   ```bash
   python read_doc.py
   ```

2. **Siga as instruções na tela:**

   * Informe o caminho do arquivo `.txt`;
   * Escreva seu **prompt** (a pergunta ou instrução);
   * Escolha o modelo (ex.: 1, 2, 3…).

3. **Aguarde a resposta do modelo.**

---

## 🧠 Exemplo de uso

**Arquivo de entrada:** `email_teste.txt`

```
oi prof tudo bem?

tava vendo aqui aquele negocio do artigo q o senhor falou e fiquei meio confuso pq nao entendi direito o q tem q fazer na parte da metodologia...
```

**Prompt:**

```
Reescreva o e-mail acima em tom acadêmico e formal, mantendo o sentido original.
```

**Resposta esperada (resumida):**

> Prezado professor,
> Espero que esteja bem. Gostaria de esclarecer algumas dúvidas sobre a parte metodológica do artigo mencionado...

---

## 📘 Outro exemplo

**Arquivo de entrada:** `resumo_hist_digital.txt`
(Resumo sobre História Digital e uso de ferramentas como ATLAS.ti e Hemeroteca Digital Brasileira)

**Prompt:**

```
Leia o resumo e proponha um título acadêmico e 5 palavras-chave adequadas para o artigo.
```

**Resposta esperada:**

> **Título sugerido:** Ferramentas Digitais e Práticas de Pesquisa na História
> **Palavras-chave:** História Digital; Hemeroteca Digital Brasileira; ATLAS.ti; Fontes Digitais; Metodologia Histórica

---

## 🧾 Requisitos do Sistema

* **Python:** 3.8 ou superior
* **Ollama:** instalado e em execução local
* **Pelo menos um modelo baixado (ex.: Phi-3, Mistral, Gemma, Llama)**
* **Sistema Operacional:** Windows, Linux ou macOS

---

## 🧑‍🏫 Dicas de uso didático

💡 Use este script em oficinas de **IA Generativa e Humanidades Digitais** para:

* Demonstrar leitura contextualizada de documentos históricos;
* Analisar textos curtos, resumos ou e-mails simulados;
* Ensinar boas práticas de **prompt engineering** com modelos locais;
* Garantir **privacidade total dos dados** (execução offline).

---

## 🪪 Créditos

Desenvolvido com fins educacionais por **Eric Brasil**,
com o apoio do modelo **GPT-5** (OpenAI) para documentação técnica e formatação.

📍 Curso: *IM1256 – Introdução à História Digital (PPGIHD/UFRRJ)*
📧 Contato: [profericbrasil@gmail.com](mailto:profericbrasil@gmail.com)
🌐 [ericbrasil.com.br](https://ericbrasil.com.br)
