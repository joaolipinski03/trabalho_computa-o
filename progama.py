"""
Sistema de Manutenção de Máquinas
Arquivo: main.py
Descrição: Código base + módulo extra "Busca / Filtro" (Opção 4).
Uso: python main.py
Autor: (grupo) - gerado/organizado para entrega
"""

from datetime import datetime

# ---------------------------
# Dados iniciais (exemplo)
# ---------------------------
maquinas = [
    ["Torno CNC", "operando", 72.5, "05/11/2025"],
    ["Prensa Hidráulica", "parada", 30.0, "01/11/2025"],
    ["Compressor de Ar", "operando", 45.0, "04/11/2025"],
    ["Retífica", "operando", 60.0, "02/11/2025"],
]

historico = {
    "Torno CNC": ["Troca de óleo - 01/11/2025", "Limpeza - 03/11/2025"],
    "Prensa Hidráulica": ["Troca de mangueira - 02/11/2025"],
}

# ---------------------------
# Funções básicas do sistema
# ---------------------------

def imprimir_maquinas(lista):
    """Imprime uma lista de máquinas formatada."""
    if not lista:
        print("Nenhuma máquina encontrada.")
        return
    for m in lista:
        print(f"Nome: {m[0]} | Status: {m[1]} | Temp: {m[2]:.1f} °C | Última: {m[3]}")

def registrar_medicao(linha):
    """
    Entrada: string no formato "Nome, temperatura, status"
    Atualiza a máquina correspondente se encontrada.
    """
    try:
        partes = linha.split(",")
        nome = partes[0].strip()
        temperatura = float(partes[1].strip())
        status = partes[2].strip()
    except Exception as e:
        print("Formato inválido. Use: Nome, temperatura, status")
        return

    for m in maquinas:
        if m[0].lower() == nome.lower():
            m[1] = status
            m[2] = temperatura
            if status.lower() == "em manutenção":
                m[3] = datetime.now().strftime("%d/%m/%Y")
            print(f"Medicao registrada para {m[0]}")
            return

    print("Máquina não encontrada. Considere adicioná-la antes.")

def adicionar_manutencao(nome_maquina, descricao):
    """Adiciona um evento de manutenção no histórico."""
    if nome_maquina not in historico:
        historico[nome_maquina] = []
    historico[nome_maquina].append(f"{descricao} - {datetime.now().strftime('%d/%m/%Y')}")
    print(f"Manutenção registrada em {nome_maquina}.")

def salvar_dados_maquinas(lista_maquinas, nome_arquivo="dados_maquinas.txt"):
    """Salva a lista de máquinas em arquivo .txt (formato ; separado)."""
    with open(nome_arquivo, "w", encoding="utf-8") as arq:
        for m in lista_maquinas:
            linha = f"{m[0]};{m[1]};{m[2]};{m[3]}\n"
            arq.write(linha)
    print("Dados salvos em", nome_arquivo)

def carregar_dados_maquinas(nome_arquivo="dados_maquinas.txt"):
    """Carrega máquinas do arquivo e retorna uma lista (vazia se não existir)."""
    maquinas_lidas = []
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                if len(partes) < 4:
                    continue  # pula linhas incompletas
                nome = partes[0]
                status = partes[1]
                try:
                    temperatura = float(partes[2])
                except ValueError:
                    temperatura = 0.0
                ultima = partes[3]
                maquinas_lidas.append([nome, status, temperatura, ultima])
    except FileNotFoundError:
        print("Arquivo não encontrado. Salve primeiro.")
    return maquinas_lidas

def gerar_relatorio(nome_arquivo="relatorio_final.txt"):
    """Gera um relatório simples em texto sobre o estado atual das máquinas."""
    if not maquinas:
        print("Nenhuma máquina para gerar relatório.")
        return

    maquina_quente = max(maquinas, key=lambda x: x[2])

    with open(nome_arquivo, "w", encoding="utf-8") as arq:
        arq.write("RELATÓRIO DE MÁQUINAS\n\n")
        arq.write(f"Máquina mais quente: {maquina_quente[0]} ({maquina_quente[2]:.1f} °C)\n\n")

        arq.write("Máquinas em manutenção ou paradas:\n")
        for m in maquinas:
            if m[1].lower() in ["em manutenção", "parada"]:
                arq.write(f"- {m[0]} (última manutenção: {m[3]})\n")

        arq.write("\nQuantidade de manutenções registradas:\n")
        for nome, eventos in historico.items():
            arq.write(f"- {nome}: {len(eventos)} registro(s)\n")

    print("Relatório gerado em", nome_arquivo)

# ---------------------------
# Módulo Extra: Busca / Filtro
# ---------------------------

def buscar_por_nome_parcial(termo):
    """
    Retorna lista de máquinas cujo nome contém 'termo' (case-insensitive).
    Ex: termo = "torno" encontra "Torno CNC"
    """
    termo = termo.strip().lower()
    resultados = [m for m in maquinas if termo in m[0].lower()]
    return resultados

def listar_por_status(status):
    """
    Retorna lista de máquinas com o status exato (case-insensitive).
    Exemplos de status: "operando", "parada", "em manutenção"
    """
    status = status.strip().lower()
    resultados = [m for m in maquinas if m[1].lower() == status]
    return resultados

def modulo_extra_busca():
    """Menu simples para usar as funções de busca/filtro."""
    while True:
        print("\n=== MÓDULO EXTRA: BUSCA / FILTRO ===")
        print("1 - Buscar por nome parcial")
        print("2 - Listar por status")
        print("3 - Voltar ao menu principal")
        opc = input("Escolha: ").strip()
        if opc == "1":
            termo = input("Digite parte do nome (ex: torno): ")
            res = buscar_por_nome_parcial(termo)
            imprimir_maquinas(res)
        elif opc == "2":
            status = input("Digite o status (operando / parada / em manutenção): ")
            res = listar_por_status(status)
            imprimir_maquinas(res)
        elif opc == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")

# ---------------------------
# Menu principal (ponto de entrada)
# ---------------------------

def main():
    global maquinas, historico
    while True:
        print("\n=== Sistema de Manutenção de Máquinas ===")
        print("1 - Listar máquinas")
        print("2 - Registrar medição")
        print("3 - Adicionar manutenção")
        print("4 - Salvar dados")
        print("5 - Carregar dados")
        print("6 - Gerar relatório")
        print("7 - Rodar módulo extra (Busca / Filtro)")
        print("8 - Listar histórico")
        print("0 - Sair")
        opc = input("Escolha: ").strip()

        if opc == "1":
            imprimir_maquinas(maquinas)
        elif opc == "2":
            linha = input("Digite: nome, temperatura, status: ")
            registrar_medicao(linha)
        elif opc == "3":
            nome = input("Nome da máquina: ")
            desc = input("Descrição da manutenção: ")
            adicionar_manutencao(nome, desc)
        elif opc == "4":
            salvar_dados_maquinas(maquinas)
        elif opc == "5":
            carregadas = carregar_dados_maquinas()
            if carregadas:
                maquinas = carregadas
                print("Dados carregados e substituídos na sessão atual.")
        elif opc == "6":
            gerar_relatorio()
        elif opc == "7":
            modulo_extra_busca()
        elif opc == "8":
            if not historico:
                print("Histórico vazio.")
            else:
                for nome, eventos in historico.items():
                    print(f"\nHistórico da máquina {nome}:")
                    for ev in eventos:
                        print(" -", ev)
        elif opc == "0":
            print("Saindo... até logo.")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa apenas quando rodar diretamente
if __name__ == "__main__":
    main()
