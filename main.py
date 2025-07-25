import json
import datetime

def adicionar_gastos():
    descricao = input("Descrição do gasto: ")
    valor = float(input("Valor do gasto:R$ "))
    categoria = input("Categoria do gasto: ")
    data = input("Data (dd/mm/aaaa) [pressione Enter para hoje]: ")

    if not data:
        data = datetime.datetime.today().strftime('%d/%m/%Y')

    novo_gasto = {

        "descricao":descricao
        ,"valor":valor
        ,"categoria":categoria
        ,"data":data

    }
    try:
        with open('gastos.json', 'r') as f:
            gastos = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        gastos = []

    gastos.append(novo_gasto)

    with open("gastos.json", "w") as f:
        json.dump(gastos, f, indent=4)

    print("\n✅Gasto adicionado com sucesso!")

def listar_gastos():
    try:
        with open("gastos.json", "r") as f:
            gastos = json.load(f)

        if not gastos:
            print("Nenhum gasto registrado ainda.")
            return

        print("LISTA DE GASTOS:")
        print("-" * 40)
        for i, gasto in enumerate(gastos, start=1):
            print(f"{i}. {gasto['descricao']} - R$ {gasto['valor']:.2f}")
            print(f"  Categoria: {gasto['categoria']}")
            print(f"  Data: {gasto['data']}")
            print("-" * 40)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Não foi possível ler os gastos. Nenhum dado encontrado.")

def mostrar_totais_por_categoria():
    try:
        with open("gastos.json", "r") as f:
            gastos = json.load(f)

        if not gastos:
            print("Nenhum gasto registrado ainda.")
            return

        totais = {}

        for gasto in gastos:
            categoria = gasto['categoria']
            valor = gasto['valor']

            if categoria in totais:
                totais[categoria] += valor
            else:
                totais[categoria] = valor

        print("\n📊 TOTAL POR CATEGORIA:")
        print("-" * 40)
        for cat, total in totais.items():
            print(f"{cat}: {total:.2f}")
            print("-" * 40)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Erro ao ler os gastos.")

def exportar_relatorio_txt():
    try:
        with open("gastos.json", "r") as f:
            gastos = json.load(f)

        if not gastos:
            print("Nenhum gastos para exportar.")
            return
        with open("relatorio.txt", "w", encoding="utf-8") as relatorio:
            relatorio.write("=== RELATÓRIO DE GASTOS ===\n\n")
            for i, gastos in enumerate(gastos, start=1):
                relatorio.write(f"{i}. {gastos['descricao']} - R$ {gastos['valor']:.2f}\n")
                relatorio.write(f" Categoria: {gastos['categoria']}\n")
                relatorio.write(f" Data: {gastos['data']}\n")
                relatorio.write("-" * 30+ "\n")

        print("\n📄 Relatório exportado como 'relatorio.txt' com sucesso!")

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Erro ao gerar o relatório. Nenhum dado disponível.")

def filtrar_por_categoria():
    try:
        with open("gastos.json", "r") as f:
            gastos = json.load(f)

        if not gastos:
            print("Nenhum gasto registrado ainda.")
            return

        categoria_filtro = input("Digite a categoria que deseja filtrar: ")

        gastos_filtrados = [g for g in gastos if g["categoria"].lower() == categoria_filtro.lower()]

        if not gastos_filtrados:
            print(f"Nenhum gasto encontrado para a categoria '{categoria_filtro}'.")
            return

        print(f"\n📂 GASTOS NA CATEGORIA: {categoria_filtro.upper()}")
        print("-" * 40)
        for i, gasto in enumerate(gastos_filtrados, start=1):
            print(f"{i}. {gasto['descricao']}")
            print(f"  Data: {gasto['data']}")
            print("-" * 40)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Erro ao acessar os dados de gastos.")

def deletar_gasto():
    try:
        with open("gastos.json", "r") as f:
            gastos = json.load(f)

        if not gastos:
            print("Nenhum gasto registrado para excluir.")
            return

        print("\nLISTA DE GASTOS:")
        print("-" * 40)
        for i, gasto in enumerate(gastos, start=1):
            print(f"{i}. {gasto['descricao']} - R$ {gasto['valor']:.2f} ({gasto['categoria']}, {gasto['data']})")

            try:
                escolha = int(input("Digite o número do gasto que deseja excluir: "))
                if 1 <= escolha <= len(gastos):
                    gasto_removido = gastos.pop(escolha - 1)

                    with open("gastos.json", "w") as f:
                        json.dump(gastos, f, indent=4)

                    print(f"\n🗑️ Gasto '{gasto_removido['descricao']}' excluído com sucesso!")
                else:
                    print("❌ Número inválido.")
            except ValueError:
                print("❌ Entrada inválida. Digite um número.")

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Erro ao acessar o arquivo de gastos.")

def editar_gasto():
    try:
        with open("gastos.json", "r") as f:
            gastos = json.load(f)

        if not gastos:
            print("Nenhum gasto registrado para editar.")
            return

        print("\nLISTA DE GASTOS:")
        print("-" * 40)
        for i, gasto in enumerate(gastos, start=1):
            print(f"{i}. {gasto['descricao']} - R$ {gasto['valor']:.2f} ({gasto['categoria']}), ({gasto['data']})")

        try:
            escolha = int(input("Digite o número do gasto que deseja editar: "))
            if 1 <= escolha <= len(gastos):
                gasto_editado = gastos[escolha - 1]

                print("\nPressione Enter para manter o valor atual.")

                nova_descricao = input(f"Descrição [{gasto_editado['descricao']}]: ") or gasto_editado['descricao']
                novo_valor = input(f"Valor [{gasto_editado['valor']}]: ")
                nova_categoria = input(f"Categoria [{gasto_editado['categoria']}]: ") or gasto_editado['categoria']
                nova_data = input(f"Data [{gasto_editado['data']}]: ") or gasto_editado['data']

                try:
                    novo_valor = float(novo_valor) if novo_valor else gasto_editado['valor']
                except ValueError:
                    print("❌ Valor inválido. Mantido valor original.")
                    nova_data = gasto_editado['valor']

                gasto_editado.update({
                    "descricao": nova_descricao,
                    "valor": novo_valor,
                    "categoria": nova_categoria,
                    "data": nova_data
                })
                with open("gastos.json", "w") as f:
                    json.dump(gastos, f, indent=4)

                print("\n✏️ Gasto atualizado com sucesso!")
            else:
                print("❌ Número inválido.")
        except ValueError:
            print("❌ Entrada inválida. Digite um número.")
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Erro ao acessar os dados de gastos.")

def filtrar_por_data():
    try:
        with open("gastos.json", "r") as f:
            gastos = json.load(f)

        if not gastos:
            print("Nenhum gasto registrado.")
            return

        data_inicio = input("Data de início (dd/mm/aaaa): ")
        data_fim = input("Data de fim (dd/mm/aaaa): ")

        try:
            data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
            data_fim = datetime.strptime(data_fim, "%d/%m/%Y")

        except ValueError:
            print("❌ Formato de data inválido. Use dd/mm/aaaa.")
            return

        print(f"\n📅 GASTOS ENTRE {data_inicio} E {data_fim}:")
        print("-" * 40)
        gastos_encontados = False

        for gasto in gastos:
            data_gasto = datetime.strptime(gasto['data'], "%d/%m/%Y")
            if data_inicio <= data_gasto and data_gasto <= data_fim:
                print(f"{gasto['descricao']} - R$ {gasto['valor']:.2f}")
                print(f"  Categoria: {gasto['categoria']}")
                print(f"  Data: {gasto['data']}")
                print("-" * 40)
                gastos_encontrados = True

        if not gastos_encontados:
            print("Nenhum gasto encontrado nesse intervalo.")

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Erro ao acessar os dados de gastos.")

if __name__ == "__main__":
    print("\n=== FinanZen 🧘 MENU ===")
    print("1. Adicionar gasto")
    print("2. Listar gastos")
    print("3. Mostar totais por categoria")
    print("4. Exportar relatorio em .txt")
    print("5. Filtrar por categoria")
    print("6. Deletar gasto")
    print("7. Editar gasto")
    print("8. Filtrar por intervalo de datas")
    opcao = input("Escolha uma opção (1 a 8): ")

    if opcao == "1":
        adicionar_gastos()
    elif opcao == "2":
        listar_gastos()
    elif opcao == "3":
        mostrar_totais_por_categoria()
    elif opcao == "4":
        exportar_relatorio_txt()
    elif opcao == "5":
        filtrar_por_categoria()
    elif opcao == "6":
        deletar_gasto()
    elif opcao == "7":
        editar_gasto()
    elif opcao == "8":
        filtrar_por_data()
    else:
        print("❌ Opção inválida.")