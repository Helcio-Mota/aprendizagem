**Resposta curta:** Não é possível "vincular" o login da sua instalação local (via npm) à sua conta do n8n Cloud de forma direta, como se fosse um aplicativo que sincroniza automaticamente. A sua conta Cloud é para o serviço gerenciado por eles, e a instalação local é um servidor independente.

No entanto, isso não significa que você perdeu seus workflows antigos. Você pode **migrar todos os seus workflows do n8n Cloud para a sua nova máquina local** seguindo este passo a passo.

---

### 📤 1. Exportar os Workflows do n8n Cloud

Primeiro, acesse sua conta no site do n8n Cloud ([app.n8n.cloud](https://app.n8n.cloud)).

1.  No painel principal, clique em **"Admin Panel"** no canto inferior esquerdo.
2.  Vá até a aba **"Manage"**.
3.  Clique no botão **"Export"**.
4.  Uma janela será aberta. Selecione todos os workflows que você deseja transferir.
5.  Confirme e faça o download do arquivo. Ele será salvo no seu computador (provavelmente na pasta `Downloads`).

****

**Nota importante:** Por segurança, as credenciais (como chaves de API e senhas) **não são exportadas**. Você precisará recriá-las manualmente na sua instância local.

---

### 📥 2. Importar os Workflows para o n8n Local

Agora, na sua instalação local (`http://localhost:5678`):

1.  **Crie o usuário:** Se a tela de cadastro apareceu, crie seu novo usuário local. Esta será a sua nova conta de "dono" do n8n local.
2.  Após fazer o login, você verá um painel em branco.
3.  Clique no menu de três pontos (⋮) no canto superior direito e selecione **"Import from File"**.
4.  Na janela que abrir, selecione o arquivo que você baixou do Cloud.
5.  Os workflows aparecerão no seu painel local.

****

Se preferir, você também pode usar um comando no terminal para importar:

```bash
n8n import:workflow --input=caminho/para/seu/arquivo.json
```

---

### 🔧 3. Recriar as Credenciais

Após importar os workflows, você notará que eles têm um aviso, pois as credenciais (como token do Google, OpenAI, etc.) estão faltando. Para cada nó que precisar de autenticação:

1.  Abra o workflow.
2.  Clique no nó.
3.  Na aba de credenciais, clique em **"Create New"**.
4.  Preencha os dados da API e salve.

Isso precisa ser feito uma única vez para cada serviço que você usa. Depois de preenchidas, as credenciais ficam salvas na sua máquina local.

---

### 💡 Dica Extra: Sincronização Futura

Se no futuro você quiser manter uma sincronia entre ambientes, pode usar ferramentas da comunidade como o **[n8n-local](https://www.npmjs.com/package/@easynet/n8n-local)** (um pacote npm) que sincroniza workflows com uma pasta local e permite versionamento com Git. Ou então, usar o próprio n8n para criar um workflow de backup automático para o GitHub.
