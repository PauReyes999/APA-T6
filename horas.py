import re

"""
APA-T6 - Expresiones Regulares
Nombre y apellidos: Pau Reyes Boix
   
"""

def normalizaHoras(ficText, ficNorm):


    # Conversor de expresiones a número de minutos
    CONV_PALABRAS_MINUTO = {
        'en punto': 0,
        'y cuarto': 15,
        'y media': 30,
        'menos cuarto': 45
    }

    
    # Buscamos las expresiones que se encuentran en el texto
    RE_TIEMPO_COMPLETO = re.compile(
        r'\b('
        # Cas 1: Busca horas con "de la" o "del" o periodo.
        r'(?P<h_periodo>\d{1,2})(?::(?P<m_periodo>\d{2}))?\s+de\s+(?:la\s+(?P<p1>mañana|tarde|noche|madrugada)|del\s+(?P<p2>mediodía))\b|'
        # Cas 2: Busca hora seguida de expresiones.
        r'(?P<h_frase>\d{1,2})\s+(?P<frase>(?:en\s+punto|y\s+cuarto|y\s+media|menos\s+cuarto))\b|'
        # Cas 3: Busca formato HHh:MMm
        r'(?P<h_hm>\d{1,2})h(?:(?P<m_hm>\d{1,2})m?)?\b|'
        # Cas 4: Busca formato estándar HH:MM.
        r'(?P<h_std>\d{1,2}):(?P<m_std>\d{2})\b'
        r')', 
        re.IGNORECASE 
    )

    def sustituir_hora(match):
        h, m = None, None # Guardamos horas normalizadas.
        original_match_str = match.group(0) # Guardamos original.

        # Si se encontró Caso 1
        if match.group('h_periodo'):
            h_raw = int(match.group('h_periodo'))
            m_raw = int(match.group('m_periodo')) if match.group('m_periodo') else 0
            periodo = (match.group('p1') or match.group('p2')).lower()

            # Comprobar que la hora y los minutos estén dentro de rango (1-12, 0-59).
            if not (1 <= h_raw <= 12 and 0 <= m_raw <= 59):
                return original_match_str

            # Convertir a formato 24h según perido.
            if periodo == 'mañana':
                if not (4 <= h_raw <= 12): return original_match_str # Rango : 4 AM - 12 PM
                h = 0 if h_raw == 12 else h_raw # 12 de la mañana (medianoche) es 00:XX
            elif periodo == 'mediodía':
                if not (12 <= h_raw <= 3): return original_match_str # Rango : 12 PM - 3 PM
                h = h_raw if h_raw == 12 else h_raw + 12 # 12 PM (mediodía) es 12:XX
            elif periodo == 'tarde':
                if not (3 <= h_raw <= 8): return original_match_str # Rango : 3 PM - 8 PM
                h = h_raw + 12
            elif periodo == 'noche':
                # Rango : 8 PM - 12 AM y 1 AM - 4 AM.
                if not ((8 <= h_raw <= 12) or (1 <= h_raw <= 4)):
                    return original_match_str
                if h_raw == 12: h = 0 # 12 de la noche (medianoche) es 00:XX
                elif 1 <= h_raw <= 4: h = h_raw # 1 AM - 4 AM ya están bien en 24h
                else: h = h_raw + 12 # 8 PM - 11 PM se suman 12
            elif periodo == 'madrugada':
                if not (1 <= h_raw <= 6): return original_match_str # Rango válido: 1 AM - 6 AM
                h = 0 if h_raw == 12 else h_raw # 12 de la madrugada (medianoche) es 00:XX
            else:
                return original_match_str #ELSE no se normaliza.
            m = m_raw

        # Si se encontró Caso 2
        elif match.group('h_frase'):
            h_raw = int(match.group('h_frase'))
            frase = match.group('frase').lower()

            # La hora debe estar entre 1 y 12.
            if not (1 <= h_raw <= 12):
                return original_match_str

            m_val = CONV_PALABRAS_MINUTO.get(frase) # Obtiene los minutos de la expresion.
            
            # Ajustar la hora según cuartos.
            if 'menos cuarto' in frase:
                h_calc = h_raw - 1
                if h_calc == 0: h_calc = 12 
            else:
                h_calc = h_raw

            # Normalizar a rango 00:00-11:59 para estas expresiones.
            if h_calc == 12: 
                h = 0
            else:
                h = h_calc
            m = m_val

        # Si se encontró Caso 3
        elif match.group('h_hm'):
            h_raw = int(match.group('h_hm'))
            m_raw = int(match.group('m_hm')) if match.group('m_hm') else 0
            # Comprobar Rango.
            if 0 <= h_raw <= 23 and 0 <= m_raw <= 59:
                h, m = h_raw, m_raw
            else:
                return original_match_str # ELSE H,M imposibles.

        # Si se encontró Caso 4
        elif match.group('h_std'):
            h_raw = int(match.group('h_std'))
            m_raw = int(match.group('m_std'))
            # Comprobar Rango.
            if 0 <= h_raw <= 23 and 0 <= m_raw <= 59:
                h, m = h_raw, m_raw
            else:
                return original_match_str # Hora o minutos inválidos.

        # Una vez formateado devuelve HH:MM.
        if h is not None and m is not None:
            return f'{h:02d}:{m:02d}'
        else:
            return original_match_str # ELSE original.

    # Abre los ficheros de entrada y salida.
    with open(ficText, 'r', encoding='utf-8') as f_in, \
         open(ficNorm, 'w', encoding='utf-8') as f_out:
        # Lee el fichero línea por línea.
        for line in f_in:
            # Convierte HORAS i MINUTOS
            processed_line = RE_TIEMPO_COMPLETO.sub(sustituir_hora, line)
            f_out.write(processed_line)