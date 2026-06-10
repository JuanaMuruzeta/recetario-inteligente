#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 13:52:58 2026

@author: giuliamaniotti
"""

def validar_ingredientes(texto):
    """
    Valida que el usuario haya ingresado al menos un ingrediente.

    Parámetro:
        texto (str): texto ingresado por el usuario.

    Retorna:
        bool: True si es válido, False si está vacío.
    """
    if texto.strip() == "":
        return False
    return True


def validar_opcion_menu(opcion):
    """
    Valida que la opción del menú sea correcta.

    Parámetro:
        opcion (str): opción ingresada.

    Retorna:
        bool: True si la opción está entre 1 y 4.
    """
    if opcion in ["1", "2", "3", "4"]:
        return True
    return False


def validar_numero_receta(opcion, cantidad_recetas):
    """
    Valida que el número elegido corresponda a una receta existente.

    Parámetros:
        opcion (str): número ingresado por el usuario.
        cantidad_recetas (int): cantidad total de recetas.

    Retorna:
        bool: True si el número es válido.
    """
    if not opcion.isdigit():
        return False

    numero = int(opcion)

    if numero < 0 or numero > cantidad_recetas:
        return False

    return True