import re
import unittest

class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas] # Copia la lista para evitar problemas con el valor por defecto

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        if not isinstance(other, (int, float)):
            raise TypeError("Solo se pueden añadir números como notas.")
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlumnos):
    """
    Lee el fichero de alumnos y devuelve un diccionario de objetos Alumno.
    La clave es el nombre del alumno y el valor es su objeto Alumno.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno_nombre in sorted(alumnos.keys()):
    ...     print(alumnos[alumno_nombre])
    ...
    171	Blanca Agirrebarrenetse	9.5
    23	Carles Balcell de Lara	4.9
    68	David Garcia Fuster	7.0
    """
    alumnos = {}
    patron = re.compile(r'^\s*(\d+)\s+([^\d\n]+?)\s+([\d\s.]+)$')

    try:
        with open(ficAlumnos, 'rt', encoding='utf-8') as f:
            for linea in f:
                match = patron.match(linea)
                if match:
                    numIden = int(match.group(1))
                    nombre = match.group(2).strip()
                    notas_str = match.group(3).split()
                    notas = [float(n) for n in notas_str]
                    alumnos[nombre] = Alumno(nombre, numIden, notas)
    except FileNotFoundError:
        print(f"Error: El fichero '{ficAlumnos}' no se encontró.")
        return {}
    except Exception as e:
        print(f"Ocurrió un error al leer el fichero de alumnos: {e}")
        return {}

    return alumnos


# --- Tests unitarios con unittest para la clase Alumno ---
class TestAlumno(unittest.TestCase):

    def test_init(self):
        alumno1 = Alumno("Juan Perez")
        self.assertEqual(alumno1.nombre, "Juan Perez")
        self.assertEqual(alumno1.numIden, -1)
        self.assertEqual(alumno1.notas, [])

        alumno2 = Alumno("Maria Lopez", 123, [7.5, 8.0, 9.0])
        self.assertEqual(alumno2.nombre, "Maria Lopez")
        self.assertEqual(alumno2.numIden, 123)
        self.assertEqual(alumno2.notas, [7.5, 8.0, 9.0])

        alumno_sin_notas = Alumno("Pedro Garcia")
        alumno_sin_notas += 6
        self.assertEqual(alumno_sin_notas.notas, [6])
        self.assertEqual(alumno1.notas, [])

    def test_add(self):
        alumno = Alumno("Ana Rodriguez", notas=[6.0, 7.0])
        alumno += 8.0
        self.assertEqual(alumno.notas, [6.0, 7.0, 8.0])

        alumno += 5
        self.assertEqual(alumno.notas, [6.0, 7.0, 8.0, 5])

        alumno_original = Alumno("Carlos Ruiz")
        alumno_nuevo = alumno_original + 9.0
        self.assertIsNot(alumno_original, alumno_nuevo)
        self.assertEqual(alumno_original.notas, [])
        self.assertEqual(alumno_nuevo.notas, [9.0])

        with self.assertRaises(TypeError):
            alumno += "nota invalida"
        with self.assertRaises(TypeError):
            alumno += [1,2]

    def test_media(self):
        alumno1 = Alumno("Elena Fernandez", notas=[7.0, 8.0, 9.0])
        self.assertAlmostEqual(alumno1.media(), 8.0)

        alumno2 = Alumno("Pablo Diaz", notas=[5.5])
        self.assertAlmostEqual(alumno2.media(), 5.5)

        alumno3 = Alumno("Laura Gomez")
        self.assertEqual(alumno3.media(), 0)

        alumno4 = Alumno("Roberto Sanz", notas=[10, 10, 10, 10, 10])
        self.assertAlmostEqual(alumno4.media(), 10.0)

        alumno5 = Alumno("Alumno Negativo", notas=[-1.0, 3.0])
        self.assertAlmostEqual(alumno5.media(), 1.0)


    def test_repr(self):
        alumno = Alumno("Sara Martin", 789, [6.5, 7.0])
        expected_repr = "Alumno(\"Sara Martin\", 789, [6.5, 7.0])"
        self.assertEqual(repr(alumno), expected_repr)

        recreated_alumno = eval(repr(alumno))
        self.assertEqual(recreated_alumno.nombre, alumno.nombre)
        self.assertEqual(recreated_alumno.numIden, alumno.numIden)
        self.assertEqual(recreated_alumno.notas, alumno.notas)
        self.assertIsNot(recreated_alumno, alumno)

        alumno_apostrofe = Alumno("O'Malley", 1, [7.0])
        self.assertEqual(repr(alumno_apostrofe), "Alumno(\"O'Malley\", 1, [7.0])")


    def test_str(self):
        alumno1 = Alumno("Diego Sanchez", 101, [7.0, 8.0])
        self.assertEqual(str(alumno1), "101\tDiego Sanchez\t7.5")

        alumno2 = Alumno("Nuria Castro", notas=[9.333])
        self.assertEqual(str(alumno2), "-1\tNuria Castro\t9.3")

        alumno3 = Alumno("Miguel Torres")
        self.assertEqual(str(alumno3), "-1\tMiguel Torres\t0.0")

        alumno4 = Alumno("Un Nombre Muy Largo Para Un Alumno", 200, [6.0])
        self.assertEqual(str(alumno4), "200\tUn Nombre Muy Largo Para Un Alumno\t6.0")


if __name__ == '__main__':
    import doctest
    print("--- Ejecutando Doctests ---")
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
    print("\n--- Ejecutando UnitTests (unittest) ---")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)