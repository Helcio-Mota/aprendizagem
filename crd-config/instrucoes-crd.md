---
title: "Configuração CRD – Sessão Partilhada no Ubuntu"
author: "Guia de referência"
date: "2026-05-31"
geometry: margin=2.5cm
toc: true
toc-depth: 2
---

# Configuração do Chrome Remote Desktop para Partilhar a Sessão Física

Este documento descreve a configuração exacta para que o Chrome Remote Desktop (CRD) mostre
a mesma sessão que está no monitor físico, em vez de criar uma sessão virtual isolada.
O comportamento final é semelhante ao **RDP do Windows**: a mesma sessão visível local e remotamente.

---

## 1. Instalação do Chrome Remote Desktop no Ubuntu

1. Aceda a <https://remotedesktop.google.com/access>.
2. Clique em **"Configurar acesso remoto"** e depois em **"Transferir"** para obter o pacote `.deb`.
3. Instale o pacote e resolva dependências:

```bash
sudo dpkg -i ~/Downloads/chrome-remote-desktop_*.deb
sudo apt install -f
```

4. Siga as instruções no navegador para associar a máquina à sua conta Google.

> O serviço `chrome-remote-desktop@<utilizador>.service` será criado automaticamente.

---

## 2. Activar o Login Automático (obrigatório)

> **Atenção:** Sem o login automático, o ecrã de login bloqueia o acesso remoto e local simultaneamente.

1. Edite o ficheiro de configuração do GDM:

```bash
sudo nano /etc/gdm3/custom.conf
# Se o ficheiro não existir, use: /etc/gdm/custom.conf
```

2. Na secção `[daemon]`, descomente ou adicione as seguintes linhas:

```ini
AutomaticLoginEnable = true
AutomaticLogin = <utilizador>
```

> Substitua `<utilizador>` pelo nome real (ex: `aprimoraia`).

3. Guarde com `Ctrl+O`, `Enter`, `Ctrl+X` e reinicie a máquina para testar.

---

## 3. Ficheiros a Alterar

### 3.1. `~/.chrome-remote-desktop-session`

Este ficheiro é executado pelo CRD para iniciar a sessão. O objectivo é substituí-lo por um
script que mantém a sessão viva **sem lançar um novo ambiente gráfico**.

**Conteúdo final:**

```bash
#!/bin/sh
# Manter o processo de sessão vivo, sem lançar novo ambiente gráfico
while true; do
    sleep 3600
done
```

---

### 3.2. `/opt/google/chrome-remote-desktop/chrome-remote-desktop`

Script principal do CRD (Python). As alterações são feitas na função `_launch_server`
(por volta da linha 1653).

**Antes de editar, faça um backup:**

```bash
sudo cp /opt/google/chrome-remote-desktop/chrome-remote-desktop \
        /opt/google/chrome-remote-desktop/chrome-remote-desktop.bak
```

#### a) Variável `display`

Substituir:

```python
display = self.get_unused_display_number()
```

Por:

```python
display = 0
```

#### b) Variável `x_auth_file`

Substituir:

```python
x_auth_file = os.path.expanduser("~/.Xauthority")
```

Por:

```python
x_auth_file = "/run/user/1000/gdm/Xauthority"
```

> Confirme o `uid` com `echo $XDG_RUNTIME_DIR`; normalmente é `1000`.

#### c) Bloco `xauth add` — comentar totalmente

```python
# Run "xauth add" with |child_env| so that it modifies the same XAUTHORITY
# file which will be used for the X session.
# exit_code = subprocess.call("xauth add :%d . `mcookie`" % display,
#                              env=self.child_env, shell=True)
# if exit_code != 0:
#   raise Exception("xauth failed with code %d" % exit_code)
```

#### d) Bloco de lançamento do servidor X — substituir por espera no ecrã físico

Substituir o bloco `if self.use_xvfb: ... else: ...` por:

```python
# Aguardar o ecrã físico (:0) e a autoridade X estarem prontos (máx. 30 seg)
self.server_proc = None
for _ in range(30):
    if os.path.exists("/tmp/.X11-unix/X0") and \
       os.path.exists("/run/user/1000/gdm/Xauthority"):
        break
    time.sleep(1)
else:
    raise Exception("Display :0 ou autoridade X não apareceram a tempo.")

# Não criar servidor X virtual – usar a sessão física no :0
# if self.use_xvfb:
#   self._launch_xvfb(display, x_auth_file, extra_x_args)
# else:
#   self._launch_xorg(display, x_auth_file, extra_x_args)
```

#### e) `setxkbmap` — comentar opcionalmente (evita erros inofensivos)

```python
# exit_code = subprocess.call(["setxkbmap", "-rules", "evdev"], env=self.child_env)
```

Guarde e saia com `Ctrl+O`, `Enter`, `Ctrl+X`.

---

### 3.3. Serviço systemd

**Remover overrides problemáticos** (caso existam):

```bash
sudo rm -f /etc/systemd/system/chrome-remote-desktop@.service.d/override.conf
sudo rmdir /etc/systemd/system/chrome-remote-desktop@.service.d 2>/dev/null
```

**Activar o serviço para arranque automático:**

```bash
sudo systemctl enable chrome-remote-desktop@<utilizador>.service
sudo systemctl daemon-reload
```

> Substitua `<utilizador>` pelo nome real (ex: `aprimoraia`).

---

## 4. Comandos Pós-Alteração

**Verificar a sintaxe Python:**

```bash
python3 -m py_compile /opt/google/chrome-remote-desktop/chrome-remote-desktop
```

> Se não houver saída, a sintaxe está correcta.

**Reiniciar o serviço e testar:**

```bash
sudo systemctl restart chrome-remote-desktop@<utilizador>.service
```

Aceda remotamente via Chrome Remote Desktop — deve ver a mesma sessão do monitor.
Reinicie a máquina e confirme que o CRD inicia automaticamente e partilha a sessão.

---

## 5. Verificações de Diagnóstico

Se o CRD não funcionar após o reboot, execute os seguintes comandos:

**Estado do serviço:**

```bash
sudo systemctl status chrome-remote-desktop@<utilizador>.service
```

**Logs do serviço:**

```bash
sudo journalctl -u chrome-remote-desktop@<utilizador>.service \
    --since "5 minutes ago" --no-pager
```

**Permissões do ficheiro de autoridade X:**

```bash
ls -l /run/user/1000/gdm/Xauthority
```

**Teste local de acesso ao ecrã:**

```bash
DISPLAY=:0 XAUTHORITY=/run/user/1000/gdm/Xauthority xrandr
```

---

## 6. Backup e Restauro dos Ficheiros

Os ficheiros alterados encontram-se na pasta `~/backup-crd-config`:

| Ficheiro | Descrição |
|---|---|
| `.chrome-remote-desktop-session` | Script de sessão modificado |
| `chrome-remote-desktop.modificado` | Script principal do CRD modificado |
| `chrome-remote-desktop.bak` | Cópia original do script principal |

### 6.1. Restaurar o script de sessão

```bash
cp ~/backup-crd-config/.chrome-remote-desktop-session ~/
```

### 6.2. Restaurar o script principal do CRD

```bash
# Fazer backup do ficheiro atualmente em uso
sudo cp /opt/google/chrome-remote-desktop/chrome-remote-desktop \
        /opt/google/chrome-remote-desktop/chrome-remote-desktop.bak.$(date +%F)

# Copiar a versão modificada do backup
sudo cp ~/backup-crd-config/chrome-remote-desktop.modificado \
        /opt/google/chrome-remote-desktop/chrome-remote-desktop

# Repor permissões e dono originais
sudo chown root:root /opt/google/chrome-remote-desktop/chrome-remote-desktop
sudo chmod +x /opt/google/chrome-remote-desktop/chrome-remote-desktop
```

### 6.3. Activar o serviço após restauro (se necessário)

```bash
sudo systemctl enable chrome-remote-desktop@<utilizador>.service
sudo systemctl daemon-reload
sudo systemctl restart chrome-remote-desktop@<utilizador>.service
```

---

## 7. Criar o Backup Completo

Execute os seguintes comandos a partir dos ficheiros já configurados:

```bash
mkdir -p ~/backup-crd-config
cp ~/.chrome-remote-desktop-session ~/backup-crd-config/
sudo cp /opt/google/chrome-remote-desktop/chrome-remote-desktop \
        ~/backup-crd-config/chrome-remote-desktop.modificado
sudo cp /opt/google/chrome-remote-desktop/chrome-remote-desktop.bak \
        ~/backup-crd-config/ 2>/dev/null
sudo chown -R $USER:$USER ~/backup-crd-config/
tar -czf ~/crd-backup-$(date +%F).tar.gz -C ~/ backup-crd-config
```

---

*Fim do documento.*
