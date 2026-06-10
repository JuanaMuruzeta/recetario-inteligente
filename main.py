#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:23:15 2026

@author: giuliamaniotti
"""

from src.api_recetas import buscar_recetas_por_ingrediente, obtener_detalle_receta
from src.procesamiento import convertir_texto_a_lista_ingredientes
from src.procesamiento import armar_recetas_procesadas
from src.procesamiento import filtrar_recetas_por_pais
from src.procesamiento import ordenar_recetas_por_coincidencia
from src.historial import guardar_busqueda, mostrar_historial
from src.validaciones import validar_ingredientes, validar_opcion_menu, validar_numero_receta
from src.graficos import generar_todos_los_graficos


def mostrar_menu():
    """
    Muestra el menú principal del programa.
    """
    print("\nBIENVENIDA AL BUSCADOR DE RECETAS")
    print("1. Buscar recetas por ingredientes")
    print("2. Ver historial de búsquedas")
    print("3. Ver gráficos")
    print("4. Salir")


def mostrar_ranking_recetas(recetas):
    """
    Muestra el ranking de recetas ordenadas por porcentaje de coincidencia.
    """
    print(f"\nRECETAS ENCONTRADAS: {len(recetas)}")

    for i in range(len(recetas)):
        receta = recetas[i]
        print(f"{i + 1}. {receta['nombre']}")
        print(f"   País: {receta['pais']}")
        print(f"   Categoría: {receta['categoria']}")
        print(f"   Ingredientes coincidentes: {receta['coincidencias']}")
        print(f"   Porcentaje de coincidencia: {receta['porcentaje']}%")


def mostrar_detalle_receta(receta):
    """
    Muestra el detalle completo de una receta elegida.
    """
    print("\nDETALLE DE LA RECETA")
    print("Nombre:", receta["nombre"])
    print("País:", receta["pais"])
    print("Categoría:", receta["categoria"])

    print("\nIngredientes:")
    for ingrediente in receta["ingredientes_receta"]:
        print("-", ingrediente)

    print("\nInstrucciones:")
    print(receta["instrucciones"])


def pedir_pais():
    """
    Pregunta si el usuario quiere filtrar recetas por país.
    """
    respuesta = input("\n¿Desea filtrar recetas por país? (si/no): ")

    if respuesta.lower() == "si":
        pais = input("Ingrese el país en inglés, por ejemplo Italian, Mexican, Canadian: ")
        return pais

    return ""


def ejecutar_busqueda():
    """
    Ejecuta el proceso completo de búsqueda de recetas.
    """
    texto_ingredientes = input("\nIngrese ingredientes separados por coma: ")

    if not validar_ingredientes(texto_ingredientes):
        print("Debe ingresar al menos un ingrediente.")
        return

    ingredientes_usuario = convertir_texto_a_lista_ingredientes(texto_ingredientes)

    if len(ingredientes_usuario) == 0:
        print("Debe ingresar ingredientes válidos.")
        return

    pais = pedir_pais()
    ingrediente_principal = ingredientes_usuario[0]

    print("\nBuscando recetas...")
    recetas_api = buscar_recetas_por_ingrediente(ingrediente_principal)

    if len(recetas_api) == 0:
        print("No se encontraron recetas con ese ingrediente.")
        guardar_busqueda(ingredientes_usuario, pais, 0, 0)
        return

    recetas_procesadas = armar_recetas_procesadas(
        recetas_api,
        ingredientes_usuario,
        obtener_detalle_receta
    )

    recetas_filtradas = filtrar_recetas_por_pais(recetas_procesadas, pais)
    recetas_ordenadas = ordenar_recetas_por_coincidencia(recetas_filtradas)

    if len(recetas_ordenadas) == 0:
        print("No se encontraron recetas con ese filtro.")
        guardar_busqueda(ingredientes_usuario, pais, 0, 0)
        return

    mostrar_ranking_recetas(recetas_ordenadas)

    mejor_porcentaje = recetas_ordenadas[0]["porcentaje"]
    guardar_busqueda(ingredientes_usuario, pais, len(recetas_ordenadas), mejor_porcentaje)

    opcion = input("\nIngrese el número de una receta para ver el detalle o 0 para volver al menú: ")

    if not validar_numero_receta(opcion, len(recetas_ordenadas)):
        print("Número inválido.")
        return

    numero = int(opcion)

    if numero == 0:
        return

    receta_elegida = recetas_ordenadas[numero - 1]
    mostrar_detalle_receta(receta_elegida)


def mostrar_graficos():
    """
    Genera todos los gráficos definidos para la opción 3 del menú.
    """
    generar_todos_los_graficos()


def main():
    """
    Función principal del programa.
    """
    salir = False

    while salir == False:
        mostrar_menu()
        opcion = input("\nIngrese una opción: ")

        if not validar_opcion_menu(opcion):
            print("Opción inválida. Ingrese un número del 1 al 4.")

        elif opcion == "1":
            ejecutar_busqueda()

        elif opcion == "2":
            mostrar_historial()

        elif opcion == "3":
            mostrar_graficos()

        elif opcion == "4":
            print("Gracias por usar el buscador de recetas.")
            salir = True


main()