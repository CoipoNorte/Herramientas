def eliminar_saltos_de_linea(archivo_entrada, archivo_salida):
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as entrada:
            texto = entrada.read()
            # Reemplazar saltos de línea por un solo espacio
            texto_sin_saltos = texto.replace('\n', ' ')
            # Reemplazar espacios dobles o múltiples por un solo espacio
            texto_sin_saltos = ' '.join(texto_sin_saltos.split())

        with open(archivo_salida, 'w', encoding='utf-8') as salida:
            salida.write(texto_sin_saltos)
        
        print("Saltos de línea y espacios dobles/múltiples eliminados. Texto guardado en", archivo_salida)

    except FileNotFoundError:
        print("El archivo de entrada no existe.")

# Nombre de tu archivo de entrada y de salida
archivo_entrada = "TEXTO LARGO.txt"
archivo_salida = "TEXTO_LARGO_sin_saltos.txt"

# Llamada a la función para eliminar los saltos de línea y espacios dobles/múltiples
eliminar_saltos_de_linea(archivo_entrada, archivo_salida)
