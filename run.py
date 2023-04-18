from src.qualis.download_qualis import import_qualis
from src.sucupira.download_sucupira import download_producoes, download_docentes
from src.xls.read_xls import read_producoes, read_docentes
from src.avaliacao.avaliar import avaliar

def main():
    print("O que deseja fazer?")
    print("Importar qualis: 1")
    print("Download XLS conferências: 2")
    print("Download XLS docentes: 3")
    print("Ler XLS conferências e gerar json com dados: 4")
    print("Ler XLS docentes e gerar json com dados: 5")
    print("Avaliar: 6")
    opcao = int(input())
    if opcao == 1:
        import_qualis()
    elif opcao == 2:
        download_producoes()
    elif opcao == 3:
        download_docentes()
    elif opcao == 4:
        read_producoes()
    #elif opcao == 5:
    #read_docentes()
    elif opcao == 6:
        avaliar()
main()